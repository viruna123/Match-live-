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
    
    img = Image.new('RGB', (1280, 720), color=(0, 20, 60))
    img.save('bg.jpg')

def get_match_data():
    try:
        # Google search results එකෙන් කෙලින්ම ලකුණු ගන්නවා
        url = "https://www.google.com/search?q=sl+vs+zim+t20+world+cup+live+score"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Google එකේ ලකුණු තියෙන පන්තිය (class) නිතරම වෙනස් වෙන නිසා title එකෙන් සහ span tags වලින් බලමු
        all_spans = soup.find_all('span')
        score_text = ""
        for span in all_spans:
            if "SL" in span.text or "ZIM" in span.text:
                if "/" in span.text or "won" in span.text.lower():
                    score_text = span.text
                    break
        
        if not score_text:
            score_text = "SRI LANKA vs ZIMBABWE\nScore Updating..."

        return f"ICC T20 WORLD CUP 2026\n\n{score_text}"
    except:
        return "SRI LANKA vs ZIMBABWE\nLive Score Updating..."

def update_image_loop():
    while True:
        text = get_match_data()
        try:
            img = Image.open('bg.jpg')
            d = ImageDraw.Draw(img)
            # ලස්සන ස්කෝර් බෝඩ් එකක්
            d.rectangle([50, 150, 1230, 550], fill=(0, 0, 0, 200), outline=(255, 215, 0), width=5)
            
            y_pos = 220
            for i, line in enumerate(text.split('\n')):
                color = (255, 215, 0) if i == 0 else (255, 255, 255)
                d.text((100, y_pos), line, fill=color)
                y_pos += 100
            
            img.save('status.png')
        except: pass
        time.sleep(15)

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    download_files()
    
    img_thread = threading.Thread(target=update_image_loop)
    img_thread.daemon = True
    img_thread.start()
    
    # FFmpeg stable settings
    cmd = (
        f'ffmpeg -re -loop 1 -i status.png -stream_loop -1 -i papare.mp3 '
        f'-c:v libx264 -preset ultrafast -b:v 1500k -maxrate 1500k -bufsize 3000k '
        f'-pix_fmt yuv420p -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 '
        f'-f flv {YOUTUBE_URL}/{STREAM_KEY}'
    )
    os.system(cmd)
