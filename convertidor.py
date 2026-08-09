import os
import threading
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import yt_dlp

def download_thread(url, folder, file_format, download_subs, progress_bar, status_label, download_btn):
    """Starts the download process in a separate thread to prevent the GUI from freezing."""
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            # Calculate download percentage %
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes > 0:
                percentage = int((downloaded_bytes / total_bytes) * 100)
                progress_bar['value'] = percentage
                status_label.config(text=f"Downloading... {percentage}%")
        elif d['status'] == 'finished':
            progress_bar['value'] = 100
            status_label.config(text="Processing file...")

    # Configuration options for yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'noplaylist': 'playlist' not in url.lower(),  # Downloads playlist if detected in URL
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
            'subtitleslangs': ['en', 'es'],
        })

    try:   with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        status_label.config(text="Download complete!")
        messagebox.showinfo("Success", "The download has completed successfully.")
    except Exception as e:
        status_label.config(text="Download error")
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    finally:
        download_btn.config(state=tk.NORMAL)

def start_download():
    url = url_entry.get().strip()
    file_format = format_combo.get()
    download_subs = subs_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    folder = filedialog.askdirectory(title="Select Destination Folder")
    if not folder:
        return

    # Disable download button while downloading
    download_button.config(state=tk.DISABLED)
    progress_bar['value'] = 0
    status_var.set("Starting...")

    # Start to download in a separate thread
    t = threading.Thread(
        target=download_thread,
        args=(url, folder, file_format, download_subs, progress_bar, status_label, download_button),
        daemon=True
    )
    t.start()

# GUI (Tkinter)
window = tk.Tk()
window.title("YouTube Downloader Pro")
window.geometry("480x360")
window.resizable(False, False)

# URL Label & Entry
url_label = tk.Label(window, text="Video or Playlist URL:", font=("Arial", 10, "bold"))
url_label.pack(pady=(15, 5))

url_entry = tk.Entry(window, width=55)
url_entry.pack(pady=5)

# Format Combobox
format_combo = ttk.Combobox(window, values=["MP4 (Video)", "MP3 (Audio)"], state="readonly")
format_combo.set("MP4 (Video)")
format_combo.pack(pady=10)

# Subtitles Checkbox
subs_var = tk.BooleanVar()
subs_check = tk.Checkbutton(window, text="Download Subtitles (EN/ES)", variable=subs_var)
subs_check.pack(pady=5)

# Download Button
download_button = tk.Button(window, text="Download", command=start_download, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
download_button.pack(pady=15)

# Progress Bar
progress_bar = ttk.Progressbar(window, length=380, mode='determinate')
progress_bar.pack(pady=5)

# Status Label
status_var = tk.StringVar(value="Waiting for URL...")
status_label = tk.Label(window, textvariable=status_var, font=("Arial", 9, "italic"))
status_label.pack(pady=5)

window.mainloop()
