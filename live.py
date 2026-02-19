import os
import requests
from bs4 import BeautifulSoup
import time
from PIL import Image, ImageDraw

def get_score():
    try:
        url = "https://www.google.com/search?q=sl+vs+zim+live+score"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        score = soup.find("div", class_="dfS7ee").text 
        return score
    except:
        return "Match Starting Soon..."

def setup_files():
    bg_url = "https://images.unsplash.com/photo-1531415074968-036ba1b575da?q=80&w=1280&h=720&auto=format&fit=crop"
    try:
        with open('bg.jpg', 'wb') as f: f.write(requests.get(bg_url).content)
    except:
        img = Image.new('RGB', (1280, 720), color = (0, 32, 96))
        img.save('bg.jpg')

def create_image(text):
    img = Image.open('bg.jpg').resize((1280, 720))
    d = ImageDraw.Draw(img)
    d.rectangle([250, 250, 1030, 470], fill=(0, 0, 0, 180))
    # මෙතන text එක මැදට එන්න පොඩ්ඩක් හැදුවා
    d.text((300, 320), f"SL VS ZIM T20 LIVE SCORE\n\n{text}", fill=(255, 255, 255))
    img.save('status.png')

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    setup_files()
    
    start_time = time.time()
    while time.time() - start_time < 14400:
        score_text = get_score()
        create_image(score_text)
        # මෙන්න මේ Command එක තමයි වැදගත්ම. මේකේ Audio සහ හරි Video Format එක තියෙනවා.
        cmd = f'ffmpeg -re -loop 1 -t 60 -i status.png -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -c:v libx264 -preset veryfast -b:v 2000k -pix_fmt yuv420p -c:a aac -shortest -f flv {YOUTUBE_URL}/{STREAM_KEY}'
        os.system(cmd)
