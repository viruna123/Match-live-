import os
import requests
from bs4 import BeautifulSoup
import time
from PIL import Image, ImageDraw

def download_files():
    music_url = "https://github.com/viruna123/Match-live-/releases/download/v1.0/Sri.Lankan.Cricket.Papare.-.Vol.1.mp3"
    bg_url = "https://images.unsplash.com/photo-1531415074968-036ba1b575da?q=80&w=1280&h=720&auto=format&fit=crop"
    
    if not os.path.exists('papare.mp3'):
        print("Downloading Papare Music...")
        r = requests.get(music_url)
        with open('papare.mp3', 'wb') as f: f.write(r.content)

    if not os.path.exists('bg.jpg'):
        img = Image.new('RGB', (1280, 720), color=(0, 20, 60))
        img.save('bg.jpg')

def get_match_data():
    try:
        # Google eken score eka ganna widiya update kala
        url = "https://www.google.com/search?q=sl+vs+zim+live+score"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Score eka thiyෙන තැන හරියටම අල්ලගන්න
        score = soup.find("div", class_="BNeawe iBp4i AP7Wnd").text if soup.find("div", class_="BNeawe iBp4i AP7Wnd") else "Live Updating..."
        match_info = soup.find("div", class_="BNeawe tS7h1t AP7Wnd").text if soup.find("div", class_="BNeawe tS7h1t AP7Wnd") else ""
        
        return f"SRI LANKA vs ZIMBABWE\n\n{score}\n\n{match_info}"
    except:
        return "Match Starting Soon / Score Updating..."

def create_image():
    while True:
        text = get_match_data()
        try:
            img = Image.open('bg.jpg').resize((1280, 720))
        except:
            img = Image.new('RGB', (1280, 720), color=(0, 20, 60))
            
        d = ImageDraw.Draw(img)
        d.rectangle([50, 150, 1230, 550], fill=(0, 0, 0, 180))
        
        y_pos = 200
        for line in text.split('\n'):
            if line.strip():
                d.text((100, y_pos), line, fill=(255, 255, 255))
                y_pos += 80
        
        img.save('status.png')
        time.sleep(30) # තත්පර 30න් 30ට image එක update වෙනවා

import threading
if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    
    download_files()
    
    # Image එක වෙනම thread එකක update වෙන්න දානවා
    img_thread = threading.Thread(target=create_image)
    img_thread.daemon = True
    img_thread.start()
    
    time.sleep(5) # Image එක හැදෙනකම් පොඩ්ඩක් ඉන්න

    print("Live Stream Starting... Stable Bitrate + Full Papare Loop")
    
    # FFmpeg Bitrate eka 1500k ta adu kala stable wenna
    # stream_loop -1 dala thiyenne papare eka iwara unaama aye loop wenna
    cmd = (
        f'ffmpeg -re -loop 1 -i status.png -stream_loop -1 -i papare.mp3 '
        f'-c:v libx264 -preset ultrafast -b:v 1500k -maxrate 1500k -bufsize 3000k '
        f'-pix_fmt yuv420p -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 '
        f'-f flv {YOUTUBE_URL}/{STREAM_KEY}'
    )
    
    os.system(cmd)
