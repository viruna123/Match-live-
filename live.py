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
        r = requests.get(music_url)
        with open('papare.mp3', 'wb') as f: f.write(r.content)
    
    # Dark blue background එකක් හදමු World Cup එකට ගැලපෙන්න
    img = Image.new('RGB', (1280, 720), color=(2, 12, 48))
    img.save('bg.jpg')

def get_match_data():
    try:
        # ඔයා එවපු World Cup 2026 ලින්ක් එක
        url = "https://www.cricbuzz.com/live-cricket-scores/139329/sl-vs-zim-38th-match-group-b-icc-mens-t20-world-cup-2026"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # ලකුණු සහ ඕවර්
        score = soup.find("span", class_="cb-font-20 text-bold").text if soup.find("span", class_="cb-font-20 text-bold") else "Updating..."
        
        # මැච් එකේ තත්ත්වය (Status)
        status = soup.find("div", class_="cb-scrcrd-status").text if soup.find("div", class_="cb-scrcrd-status") else ""
        
        # දැනට බැට් කරන අයගේ විස්තර (Batters)
        batters = soup.find_all("div", class_="cb-col cb-col-50")
        batter_info = ""
        if len(batters) >= 2:
            batter1 = batters[0].text.strip()
            batter2 = batters[1].text.strip()
            batter_info = f"Batting: {batter1} | {batter2}"

        return f"ICC T20 WORLD CUP 2026\nSRI LANKA vs ZIMBABWE\n\nScore: {score}\n{batter_info}\n\n{status}"
    except:
        return "SL vs ZIM - Score Updating..."

def update_image_loop():
    while True:
        text = get_match_data()
        img = Image.open('bg.jpg')
        d = ImageDraw.Draw(img)
        
        # Score board box
        d.rectangle([40, 100, 1240, 620], outline=(255, 215, 0), width=3) # Gold border
        d.rectangle([50, 110, 1230, 610], fill=(0, 0, 0, 220)) # Dark transparent background
        
        y_pos = 180
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line.strip():
                # මුල් පේළි දෙක රත්තරන් පාටින්
                color = (255, 215, 0) if i < 2 else (255, 255, 255)
                d.text((100, y_pos), line, fill=color)
                y_pos += 85
        
        img.save('status.png')
        time.sleep(20) # තත්පර 20න් 20ට Score එක Update වේ

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    
    download_files()
    
    img_thread = threading.Thread(target=update_image_loop)
    img_thread.daemon = True
    img_thread.start()
    
    print("World Cup Live Stream Starting... 🎺🏏")

    cmd = (
        f'ffmpeg -re -loop 1 -i status.png -stream_loop -1 -i papare.mp3 '
        f'-c:v libx264 -preset ultrafast -b:v 1500k -maxrate 1500k -bufsize 3000k '
        f'-pix_fmt yuv420p -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 '
        f'-f flv {YOUTUBE_URL}/{STREAM_KEY}'
    )
    
    os.system(cmd)
