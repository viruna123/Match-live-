import os
import requests
import time

def download_music():
    # පින්තූරය Repo එකේ තියෙන නිසා ඒක download කරන්න ඕනේ නැහැ
    music_url = "https://github.com/viruna123/Match-live-/releases/download/v1.0/Sri.Lankan.Cricket.Papare.-.Vol.1.mp3"
    
    if not os.path.exists('papare.mp3'):
        print("Downloading Papare Music from GitHub...")
        try:
            r = requests.get(music_url, timeout=60)
            with open('papare.mp3', 'wb') as f: f.write(r.content)
            print("Music Downloaded!")
        except Exception as e:
            print(f"Music download failed: {e}")

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    
    # පින්තූරය තිබේදැයි බලමු (ඔයා bg.png කියලා upload කරලා තියෙන්න ඕනේ)
    if not os.path.exists('bg.png'):
        print("ERROR: bg.png not found in repository! Please upload your image as bg.png")
    else:
        download_music()
        
        while True:
            print("Starting Live Stream... 🎺")
            
            # YouTube Settings
            cmd = (
                f'ffmpeg -re -loop 1 -i bg.png -stream_loop -1 -i papare.mp3 '
                f'-c:v libx264 -preset ultrafast -tune stillimage '
                f'-b:v 2500k -maxrate 2500k -bufsize 5000k -g 60 -keyint_min 60 -sc_threshold 0 '
                f'-pix_fmt yuv420p -c:a aac -b:a 128k -ar 44100 -map 0:v:0 -map 1:a:0 '
                f'-f flv {YOUTUBE_URL}/{STREAM_KEY}'
            )
            
            os.system(cmd)
            print("Stream connection lost. Restarting in 5 seconds...")
            time.sleep(5)
