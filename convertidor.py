import os
import threading
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import yt_dlp


def download_thread(url, folder, file_format, download_subs, progress_bar, status_label, download_btn):
    """Εκτελεί τη λήψη σε ξεχωριστό thread για να μην 'παγώνει' το GUI."""
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            # Υπολογισμός ποσοστού %
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes > 0:
                percentage = int((downloaded_bytes / total_bytes) * 100)
                progress_bar['value'] = percentage
                status_label.config(text=f"Descargando... {percentage}%")
        elif d['status'] == 'finished':
            progress_bar['value'] = 100
            status_label.config(text="Procesando archivo...")

    # Ρυθμίσεις για το yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'noplaylist': 'playlist' not in url.lower(),  # Κατεβάζει playlist if the URL exists!
    }

    if file_format == "MP3 (Audio)":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:  # MP4 Video
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })

    if download_subs:
        ydl_opts.update({
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['es', 'en'],
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        status_label.config(text="¡Descarga completada!")
        messagebox.showinfo("Éxito", "La descarga ha finalizado correctamente.")
    except Exception as e:
        status_label.config(text="Error en la descarga")
        messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
    finally:
        download_btn.config(state=tk.NORMAL)


def iniciar_descarga():
    url = entrada_url.get().strip()
    formato = combo_formato.get()
    descargar_sub = var_subs.get()

    if not url:
        messagebox.showerror("Error", "Por favor ingresa una URL válida.")
        return

    carpeta = filedialog.askdirectory(title="Selecciona la carpeta de destino")
    if not carpeta:
        return

    # Απενεργοποίηση κουμπιού κατά τη διάρκεια της λήψης
    boton_descargar.config(state=tk.DISABLED)
    barra['value'] = 0
    estado_var.set("Iniciando...")

    # Εκκίνηση σε ξεχωριστό Thread
    t = threading.Thread(
        target=download_thread,
        args=(url, carpeta, formato, descargar_sub, barra, label_estado, boton_descargar),
        daemon=True
    )
    t.start()


# --- GUI (Tkinter) ---
ventana = tk.Tk()
ventana.title("YouTube Downloader Pro")
ventana.geometry("480x360")
ventana.resizable(False, False)

# URL Label & Entry
label_url = tk.Label(ventana, text="URL del video o Playlist:", font=("Arial", 10, "bold"))
label_url.pack(pady=(15, 5))

entrada_url = tk.Entry(ventana, width=55)
entrada_url.pack(pady=5)

# Formato Combobox
combo_formato = ttk.Combobox(ventana, values=["MP4 (Video)", "MP3 (Audio)"], state="readonly")
combo_formato.set("MP4 (Video)")
combo_formato.pack(pady=10)

# Checkbox Subtítulos
var_subs = tk.BooleanVar()
check_subs = tk.Checkbutton(ventana, text="Descargar subtítulos (ES/EN)", variable=var_subs)
check_subs.pack(pady=5)

# Botón Descargar
boton_descargar = tk.Button(ventana, text="Descargar", command=iniciar_descarga, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), px=10, py=5)
boton_descargar.pack(pady=15)

# Barra de progreso
barra = ttk.Progressbar(ventana, length=380, mode='determinate')
barra.pack(pady=5)

# Estado
estado_var = tk.StringVar(value="Esperando URL...")
label_estado = tk.Label(ventana, textvariable=estado_var, font=("Arial", 9, "italic"))
label_estado.pack(pady=5)

ventana.mainloop()
