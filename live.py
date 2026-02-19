import os
import requests
from bs4 import BeautifulSoup
import time
from PIL import Image, ImageDraw
import threading

def download_files():
    music_url = "https://github.com/viruna123/Match-live-/releases/download/v1.0/Sri.Lankan.Cricket.Papare.-.Vol.1.mp3"
    if not os.path.exists('papare.mp3'):
        print("Downloading Papare...")
        r = requests.get(music_url)
        with open('papare.mp3', 'wb') as f: f.write(r.content)
    
    img = Image.new('RGB', (1280, 720), color=(2, 12, 48))
    img.save('bg.jpg')

def get_match_data():
    try:
        # ඔයා එවපු Direct Google Match ලින්ක් එක
        url = "https://www.google.com/search?q=sl+vs+zim+live+score#sie=m;/g/11yq8r3_sg;5;/m/026y268;dt;fp;1;;;;"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # 1. Google Title එකෙන් ලකුණු ගැනීම (මේක තමයි ෂුවර්ම ක්‍රමය)
        # Title එක සාමාන්‍යයෙන් තියෙන්නේ "SL 150/3 vs ZIM (18.4) - Google Search" වගේ
        raw_title = soup.title.text
        clean_score = raw_title.replace(" - Google Search", "").replace("Google සෙවුම", "").strip()
        
        # 2. Match Status එක ගන්න බලමු
        status = ""
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc:
            status = meta_desc['content'].split('.')[0] # පළවෙනි වාක්‍යය විතරක් ගමු

        return f"T20 WORLD CUP 2026\n\n{clean_score}\n\n{status}"
    except Exception as e:
        return "SL vs ZIM\nLive Score Updating...\n(Check YouTube Description)"

def update_image_loop():
    while True:
        text = get_match_data()
        try:
            img = Image.open('bg.jpg')
            d = ImageDraw.Draw(img)
            # ලස්සන Design එකක් - Neon Border
            d.rectangle([50, 150, 1230, 550], fill=(0, 0, 0, 220), outline=(0, 255, 255), width=5)
            
            y_pos = 220
            for i, line in enumerate(text.split('\n')):
                color = (0, 255, 255) if i == 0 else (255, 255, 255)
                # අකුරු ටික මැදට ගන්න
                d.text((100, y_pos), line, fill=color)
                y_pos += 90
            
            img.save('status.png')
        except:
            pass
        time.sleep(20) # තත්පර 20න් 20ට Score update වේ

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    
    download_files()
    
    # පින්තූරය update කරන එක වෙනම thread එකක දුවනවා
    img_thread = threading.Thread(target=update_image_loop)
    img_thread.daemon = True
    img_thread.start()
    
    print("Stream starting with Direct Google Link! 🎺🏏")
    
    # FFmpeg settings - Bitrate 1200k (Stable)
    cmd = (
        f'ffmpeg -re -loop 1 -i status.png -stream_loop -1 -i papare.mp3 '
        f'-c:v libx264 -preset ultrafast -b:v 1200k -maxrate 1200k -bufsize 2400k '
        f'-pix_fmt yuv420p -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 '
        f'-f flv {YOUTUBE_URL}/{STREAM_KEY}'
    )
    os.system(cmd)
