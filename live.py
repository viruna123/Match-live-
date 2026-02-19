import os
import requests
from bs4 import BeautifulSoup
import time
from PIL import Image, ImageDraw

def download_files():
    # සින්දුව සහ පසුබිම් පින්තූරය ඩවුන්ලෝඩ් කිරීම
    music_url = "https://github.com/viruna123/Match-live-/releases/download/v1.0/Sri.Lankan.Cricket.Papare.-.Vol.1.mp3"
    bg_url = "https://images.unsplash.com/photo-1531415074968-036ba1b575da?q=80&w=1280&h=720&auto=format&fit=crop"
    
    if not os.path.exists('papare.mp3'):
        print("Downloading Papare Music...")
        r = requests.get(music_url)
        with open('papare.mp3', 'wb') as f: f.write(r.content)

    if not os.path.exists('bg.jpg'):
        print("Downloading Background...")
        r = requests.get(bg_url)
        with open('bg.jpg', 'wb') as f: f.write(r.content)

def get_match_data():
    try:
        # ගූගල් එකෙන් ලකුණු සහ බැටින් විස්තර ගැනීම
        url = "https://www.google.com/search?q=sl+vs+zim+live+score"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # ලකුණු පුවරුවේ ප්‍රධාන විස්තර
        score_box = soup.find_all("div", class_="BNeawe")
        main_score = score_box[0].text if len(score_box) > 0 else "Updating..."
        details = score_box[1].text if len(score_box) > 1 else ""
        
        return f"{main_score}\n\n{details}"
    except:
        return "Waiting for Match Data..."

def create_image(text):
    # පින්තූරය නිර්මාණය කිරීම
    img = Image.open('bg.jpg').resize((1280, 720))
    d = ImageDraw.Draw(img)
    
    # මැද කොටුව
    d.rectangle([50, 200, 1230, 520], fill=(0, 0, 0, 180))
    
    title = "SL VS ZIM T20 LIVE SCORE"
    d.text((480, 230), title, fill=(255, 215, 0)) # රන්වන් පැහැය
    
    # ලකුණු සහ බැට් කරන අයගේ විස්තර
    y_pos = 300
    for line in text.split('\n'):
        if line.strip():
            d.text((100, y_pos), line, fill=(255, 255, 255))
            y_pos += 50

    img.save('status.png')

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    
    download_files()
    
    print("Live Stream is Starting with Papare Music! 🎺")
    
    start_time = time.time()
    while time.time() - start_time < 14400: # පැය 4ක්
        score_data = get_match_data()
        create_image(score_data)
        
        # FFmpeg Command - සින්දුව loop වෙන විදිහට සෙට් කර ඇත
        cmd = f'ffmpeg -re -loop 1 -t 60 -i status.png -stream_loop -1 -i papare.mp3 -c:v libx264 -preset veryfast -b:v 2500k -pix_fmt yuv420p -c:a aac -map 0:v:0 -map 1:a:0 -shortest -f flv {YOUTUBE_URL}/{STREAM_KEY}'
        os.system(cmd)
        
        time.sleep(2)
