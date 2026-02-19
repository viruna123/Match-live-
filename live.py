import os
import requests
from bs4 import BeautifulSoup  # Error එක ආවේ මේක නැති නිසා
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
        except:
            print("Music download error!")
    
    # පිරිසිදු තද නිල් පසුබිමක්
    img = Image.new('RGB', (1280, 720), color=(0, 25, 70))
    img.save('bg.jpg')

def get_match_data():
    try:
        # Cricinfo එකෙන් ලකුණු ගන්නා ක්‍රමය
        url = "https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2026-1419731/sri-lanka-vs-zimbabwe-38th-match-group-b-1420108/live-cricket-score"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Title එකෙන් ලකුණු ටික වෙන් කර ගැනීම
        full_title = soup.title.text
        # "SL vs ZIM, 38th Match..." වගේ කොටස විතරක් ගමු
        score_part = full_title.split("|")[0].strip()
        
        return f"T20 WORLD CUP 2026 LIVE\n\n{score_part}"
    except Exception as e:
        return f"SRI LANKA vs ZIMBABWE\nScore Updating...\n(Please Wait)"

def update_image_loop():
    while True:
        text = get_match_data()
        try:
            img = Image.open('bg.jpg')
            d = ImageDraw.Draw(img)
            
            # Score Board Box - Neon Blue Outline
            d.rectangle([60, 160, 1220, 560], fill=(0, 0, 0, 200), outline=(0, 210, 255), width=8)
            
            y_pos = 240
            lines = text.split('\n')
            for i, line in enumerate(lines):
                # පළමු පේළිය රන්වන් පැහැයෙන්, අනෙක්වා සුදු පැහැයෙන්
                color = (255, 215, 0) if i == 0 else (255, 255, 255)
                d.text((120, y_pos), line, fill=color)
                y_pos += 110
            
            img.save('status.png')
        except:
            pass
        time.sleep(20)

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    
    download_files()
    
    # Background එකේ ලකුණු update කරන එක පටන් ගන්නවා
    img_thread = threading.Thread(target=update_image_loop)
    img_thread.daemon = True
    img_thread.start()
    
    # Image එක මුලින්ම හැදෙනකම් පොඩ්ඩක් ඉන්න
    time.sleep(5)
    
    print("Live Stream is Starting... 🎺🏏")
    
    # FFmpeg stable settings (1200k Bitrate)
    cmd = (
        f'ffmpeg -re -loop 1 -i status.png -stream_loop -1 -i papare.mp3 '
        f'-c:v libx264 -preset ultrafast -b:v 1200k -maxrate 1200k -bufsize 2400k '
        f'-pix_fmt yuv420p -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 '
        f'-f flv {YOUTUBE_URL}/{STREAM_KEY}'
    )
    os.system(cmd)
