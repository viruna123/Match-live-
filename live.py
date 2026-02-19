import os
import requests
from bs4 import BeautifulSoup
import time
from PIL import Image, ImageDraw, ImageFont

def get_score():
    try:
        url = "https://www.google.com/search?q=sl+vs+zim+live+score"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Google score widget එකෙන් score එක ගන්නවා
        score = soup.find("div", class_="dfS7ee").text 
        return score
    except:
        return "Score Updating..."

def setup_files():
    # ලස්සන ක්‍රිකට් Background එකක් ගන්නවා
    bg_url = "https://images.unsplash.com/photo-1531415074968-036ba1b575da?q=80&w=1280&h=720&auto=format&fit=crop"
    with open('bg.jpg', 'wb') as f: f.write(requests.get(bg_url).content)

def create_image(text):
    img = Image.open('bg.jpg').resize((1280, 720))
    d = ImageDraw.Draw(img)
    # මැද කළු කොටුවක් (Text එක පැහැදිලි වීමට)
    d.rectangle([250, 250, 1030, 470], fill=(0, 0, 0, 180))
    # මෙතනින් ස්කෝර් එක ලියනවා
    d.text((350, 320), f"SL vs ZIM T20 LIVE\n\n{text}", fill=(255, 255, 255))
    img.save('status.png')

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    setup_files()
    
    # No-Copyright Music එකක් (Audio Library එකකින්)
    audio_url = "https://www.bensound.com/bensound-music/bensound-energy.mp3" 
    
    start_time = time.time()
    while time.time() - start_time < 14400: # පැය 4ක් රන් වෙනවා
        score_text = get_score()
        create_image(score_text)
        # පින්තූරය සහ Audio එක එකතු කරලා YouTube එකට යවනවා
        cmd = f'ffmpeg -re -loop 1 -t 60 -i status.png -i {audio_url} -c:v libx264 -preset veryfast -b:v 2000k -c:a aac -b:a 128k -shortest -f flv {YOUTUBE_URL}/{STREAM_KEY}'
        os.system(cmd)
