import os
import requests
from bs4 import BeautifulSoup
import time
from PIL import Image, ImageDraw
import threading

def download_files():
    music_url = "https://github.com/viruna123/Match-live-/releases/download/v1.0/Sri.Lankan.Cricket.Papare.-.Vol.1.mp3"
    if not os.path.exists('papare.mp3'):
        print("Downloading Papare Music...")
        try:
            r = requests.get(music_url)
            with open('papare.mp3', 'wb') as f: f.write(r.content)
        except: print("Music download failed!")
    
    img = Image.new('RGB', (1280, 720), color=(2, 12, 48))
    img.save('bg.jpg')

def get_match_data():
    try:
        url = "https://www.cricbuzz.com/live-cricket-scores/139329/sl-vs-zim-38th-match-group-b-icc-mens-t20-world-cup-2026"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # ක්‍රමය 1: ප්‍රධාන ස්කෝර් එක (cb-font-20 පන්තිය යටතේ ඇති සියල්ල බලමු)
        score_tags = soup.find_all(class_="cb-font-20")
        score_list = [t.text.strip() for t in score_tags if "SRI" in t.text or "ZIM" in t.text or "/" in t.text]
        
        score = " ".join(score_list) if score_list else ""

        # ක්‍රමය 2: බැට්ස්මන්ලා සහ තත්ත්වය (Status)
        status_tag = soup.find(class_="cb-scrcrd-status")
        status = status_tag.text.strip() if status_tag else ""
        
        # කිසිවක් නැත්නම් සරලව සර්ච් එන්ජින් එකේ පේන විස්තරය ගමු
        if not score:
            score = soup.title.text.split("|")[0].replace("Live Score", "").strip()

        return f"ICC T20 WORLD CUP 2026\n\n{score}\n\n{status}"
    except Exception as e:
        return "SRI LANKA vs ZIMBABWE\n\nLive Score Updating..."

def update_image_loop():
    while True:
        text = get_match_data()
        try:
            img = Image.open('bg.jpg')
            d = ImageDraw.Draw(img)
            # Board design
            d.rectangle([50, 100, 1230, 620], fill=(0, 0, 0, 230), outline=(255, 215, 0), width=5)
            
            y_pos = 180
            for i, line in enumerate(text.split('\n')):
                if line.strip():
                    color = (255, 215, 0) if i < 2 else (255, 255, 255)
                    d.text((100, y_pos), line, fill=color)
                    y_pos += 90
            
            img.save('status.png')
        except:
            pass
        time.sleep(15)

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    download_files()
    
    img_thread = threading.Thread(target=update_image_loop)
    img_thread.daemon = True
    img_thread.start()
    
    print("Stream Restarting... Checking score patterns.")
    
    cmd = (
        f'ffmpeg -re -loop 1 -i status.png -stream_loop -1 -i papare.mp3 '
        f'-c:v libx264 -preset veryfast -b:v 1500k -maxrate 1500k -bufsize 3000k '
        f'-pix_fmt yuv420p -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 '
        f'-f flv {YOUTUBE_URL}/{STREAM_KEY}'
    )
    os.system(cmd)
