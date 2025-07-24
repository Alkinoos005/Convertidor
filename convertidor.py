import os
from pytube import YouTube, Playlist
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

def actualizar_progreso(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_descargados = total_size - bytes_remaining
    porcentaje = int((bytes_descargados / total_size) * 100)
    barra['value'] = porcentaje
    ventana.update_idletasks()

def descargar_video(yt, carpeta, formato, descargar_sub):
    yt.register_on_progress_callback(actualizar_progreso)
    titulo = yt.title
    if formato == "MP4 (video)":
        stream = yt.streams.get_highest_resolution()
        archivo = stream.download(output_path=carpeta)
    elif formato == "MP3 (audio)":
        stream = yt.streams.filter(only_audio=True).first()
        archivo = stream.download(output_path=carpeta)
        base, _ = os.path.splitext(archivo)
        nuevo_archivo = base + ".mp3"
        os.rename(archivo, nuevo_archivo)
        archivo = nuevo_archivo
    else:
        return None

    if descargar_sub and yt.captions:
        caption = yt.captions.get_by_language_code("es") or yt.captions.get_by_language_code("en")
        if caption:
            subs = caption.generate_srt_captions()
            sub_path = os.path.splitext(archivo)[0] + ".srt"
            with open(sub_path, "w", encoding="utf-8") as f:
                f.write(subs)

    return archivo

def descargar():
    url = entrada_url.get().strip()
    formato = combo_formato.get()
    descargar_sub = var_subs.get()

    if not url:
        messagebox.showerror("Error", "Por favor ingresa una URL de Youtube o una playlist.")
        return
    try:
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta de destino")
        if not carpeta:
            return
        barra['value'] = 0
        estado.set("Preparando descarga...")
        ventana.update_idletasks()

        if "playlist" in url.lower():
            playlist = Playlist(url)
            for video_url in playlist.video_urls:
                yt = YouTube(video_url)
                descargar_video(yt, carpeta, formato, descargar_sub)
        else:
            yt = YouTube(url)
            descargar_video(yt, carpeta, formato, descargar_sub)

        estado.set("Descarga completada")
        messagebox.showinfo("Completado", "La descarga ha finalizado.")
    except Exception as e:
        estado.set("Error al descargar")
        messagebox.showerror("Error", str(e))

# GUI
ventana = tk.Tk()
ventana.title("Convertidor de Youtube")
ventana.geometry("450x320")

entrada_url = tk.Entry(ventana, width=50)
entrada_url.pack(pady=10)

combo_formato = ttk.Combobox(ventana, values=["MP4 (video)", "MP3 (audio)"])
combo_formato.set("MP4 (video)")
combo_formato.pack(pady=5)

var_subs = tk.BooleanVar()
check_subs = tk.Checkbutton(ventana, text="Descargar subtítulos (si hay)", variable=var_subs)
check_subs.pack()

boton_descargar = tk.Button(ventana, text="Descargar", command=descargar)
boton_descargar.pack(pady=10)

barra = ttk.Progressbar(ventana, length=300)
barra.pack(pady=10)

estado = tk.StringVar()
estado.set("Esperando URL...")
label_estado = tk.Label(ventana, textvariable=estado)
label_estado.pack()

ventana.mainloop()
