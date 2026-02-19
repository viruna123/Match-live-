import os
import requests
import time

def download_files():
    img_url = "https://files.catbox.moe/lnz8su.png"
    music_url = "https://github.com/viruna123/Match-live-/releases/download/v1.0/Sri.Lankan.Cricket.Papare.-.Vol.1.mp3"
    
    if not os.path.exists('bg.png'):
        print("Downloading Background Image...")
        r = requests.get(img_url)
        with open('bg.png', 'wb') as f: f.write(r.content)

    if not os.path.exists('papare.mp3'):
        print("Downloading Papare Music...")
        r = requests.get(music_url)
        with open('papare.mp3', 'wb') as f: f.write(r.content)

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    
    # ෆයිල් ටික මුලින්ම ලෑස්ති කරගන්නවා
    download_files()
    
    print("Live Stream Starting... (Fixed Keyframes & 2500k Bitrate) 🎺")
    
    # -g 60 සහ -keyint_min 60 දැම්මම YouTube එක ඉල්ලන තත්පර 2 Keyframe එක හරියටම යනවා
    # -b:v 2500k නිසා කොලිටි එක සුපිරියට තියෙයි
    cmd = (
        f'ffmpeg -re -loop 1 -i bg.png -stream_loop -1 -i papare.mp3 '
        f'-c:v libx264 -preset ultrafast -tune stillimage '
        f'-b:v 2500k -maxrate 2500k -bufsize 5000k -g 60 -keyint_min 60 -sc_threshold 0 '
        f'-pix_fmt yuv420p -c:a aac -b:a 128k -ar 44100 -map 0:v:0 -map 1:a:0 '
        f'-f flv {YOUTUBE_URL}/{STREAM_KEY}'
    )
    
    # ස්ට්‍රීම් එක එක දිගටම දුවනවා
    os.system(cmd)
