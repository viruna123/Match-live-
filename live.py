import os
import requests
from bs4 import BeautifulSoup
import time
from PIL import Image, ImageDraw

def get_score():
    try:
        # Google එකෙන් ලයිව් ස්කෝර් එක ගන්නවා
        url = "https://www.google.com/search?q=sl+vs+zim+live+score"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Google widget එකේ score එක තියෙන තැන
        score = soup.find("div", class_="dfS7ee").text 
        return score
    except:
        return "Score Updating..."

def setup_files():
    # Background Image එක අන්තර්ජාලයෙන් ගන්නවා
    bg_url = "https://images.unsplash.com/photo-1531415074968-036ba1b575da?q=80&w=1280&h=720&auto=format&fit=crop"
    try:
        with open('bg.jpg', 'wb') as f: f.write(requests.get(bg_url).content)
    except:
        # පින්තූරය ගන්න බැරි වුණොත් නිල් පාට පසුබිමක් හදනවා
        img = Image.new('RGB', (1280, 720), color = (0, 32, 96))
        img.save('bg.jpg')

def create_image(text):
    img = Image.open('bg.jpg').resize((1280, 720))
    d = ImageDraw.Draw(img)
    # මැද කොටුව සහ ස්කෝර් එක
    d.rectangle([250, 250, 1030, 470], fill=(0, 0, 0, 180))
    d.text((350, 320), f"SL vs ZIM T20 LIVE\n\n{text}", fill=(255, 255, 255))
    img.save('status.png')

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    setup_files()
    
    start_time = time.time()
    # පැය 4ක් දුවනවා
    while time.time() - start_time < 14400:
        score_text = get_score()
        create_image(score_text)
        # කිසිම Error එකක් එන්නේ නැති සරල FFmpeg Command එක
        cmd = f'ffmpeg -re -loop 1 -t 60 -i status.png -c:v libx264 -preset veryfast -b:v 2000k -f flv {YOUTUBE_URL}/{STREAM_KEY}'
        os.system(cmd)
