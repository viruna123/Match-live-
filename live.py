import os
import requests
import time

def download_music():
    music_url = "https://github.com/viruna123/Match-live-/releases/download/v1.0/Sri.Lankan.Cricket.Papare.-.Vol.1.mp3"
    if not os.path.exists('papare.mp3'):
        print("Downloading Papare Music...")
        try:
            r = requests.get(music_url, timeout=60)
            with open('papare.mp3', 'wb') as f: f.write(r.content)
            print("Music Downloaded!")
        except Exception as e:
            print(f"Music download failed: {e}")

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    
    download_music()
    
    # පින්තූරය bg.png නමින් තිබිය යුතුය
    if not os.path.exists('bg.png'):
        print("ERROR: bg.png not found! Please upload your image as bg.png to the repo.")
    else:
        while True:
            print("Starting Live Stream... (Auto-scaling to 720p) 🎺")
            
            # -vf "scale=1280:720,format=yuv420p" කියන කෑල්ලෙන් අර Error එක සම්පූර්ණයෙන්ම නැති වෙනවා
            # පින්තූරය මොන සයිස් එකක් වුණත් ඒක 1280x720 වලට හැඩගස්වනවා
            cmd = (
                f'ffmpeg -re -loop 1 -i bg.png -stream_loop -1 -i papare.mp3 '
                f'-vf "scale=1280:720,format=yuv420p" '
                f'-c:v libx264 -preset ultrafast -tune stillimage '
                f'-b:v 2500k -maxrate 2500k -bufsize 5000k -g 60 -keyint_min 60 -sc_threshold 0 '
                f'-c:a aac -b:a 128k -ar 44100 -map 0:v:0 -map 1:a:0 '
                f'-f flv {YOUTUBE_URL}/{STREAM_KEY}'
            )
            
            os.system(cmd)
            print("Stream restarted...")
            time.sleep(5)
