# YouTube Converter and also a Downloader Pro

A clean, user-friendly desktop application built in Python that allows you to download YouTube videos or extract audio tracks with ease. Designed with a Tkinter GUI and powered by "yt-dlp",it features multi-threading to ensure the application interface remains smooth and responsive throughout the download process.

# Features:

- High-Quality Downloads: Fetch videos in highest available quality (MP4) or extract crisp audio files (MP3).
- Playlist Support: Automatically detects playlist links and downloads all contained tracks sequentially.
- Subtitle Extraction: Option to download available embedded or auto-generated subtitles (English/Spanish).
- Non-Blocking UI: It utilizes Python’s "threading" module so the app never freezes or becomes unresponsive during large downloads.
- Real-Time Progress Tracking:** View download percentage,status updates and progress bar feedback in real time.

# Requirements and Prerequisites:

-Python: 3.8 or higher installed on your system.
-FFmpeg (Optional but highly Recommended): Required by `yt-dlp` for advanced audio conversion and post-processing.

# Python Dependencies:

Install the required library via `pip`, go to the bash and type this command:
  pip install yt-dlp

 Note: Tkinter is included by default with standard Python installations on Windows and macOS.Linux users may need to install it via their package manager (e.g.,sudo apt install python3-tk).

Installation & Setup:
  Clone or Download the Repository:

  Bash:
        git clone [https://github.com/YOUR_USERNAME/Convertidor-.git](https://github.com/YOUR_USERNAME/Convertidor-.git)
        cd Convertidor-
        Run the Application:

  Bash:
        python convertidor.py
        How to Use
        Enter URL: Paste a valid YouTube video or playlist link into the input field.

Select Format: Choose between MP4 (Video) or MP3 (Audio) from the drop-down menu.

Subtitles (Optional): Check the Download Subtitles option if you want to save available subtitle files.

Download: Click the Download button and select your destination folder when prompted.

Track Progress: Watch the progress bar for real-time download status.A confirmation popup will notify you when finished.

  Project's Structure:
  
  convertidor.py   -------->     # Main Python script containing GUI and download logic
  README.md        -------->     # Documentation and guide
  LICENSE          -------->     # MIT License

Licensing Right's:
This app is distributed under the MIT License. See the LICENSE file for more information.
