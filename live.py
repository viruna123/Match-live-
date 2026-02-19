import os
import requests
from bs4 import BeautifulSoup
import time
from PIL import Image, ImageDraw, ImageFont

def get_match_data():
    try:
        # Cricbuzz live score page (මේ URL එක මැච් එක අනුව වෙනස් වෙන්න පුළුවන්, දැනට පොදු සෙවුමක් පාවිච්චි කරමු)
        url = "https://www.google.com/search?q=sl+vs+zim+live+score+cricbuzz"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # මෙතනින් සරලව ලකුණු සහ බැටින් කරන අයගේ විස්තර ගන්නවා
        # Google Snippet එකේ තියෙන විස්තර අපි ටාගට් කරමු
        score_box = soup.find_all("div", class_="BNeawe")
        
        main_score = score_box[0].text if len(score_box) > 0 else "Updating..."
        details = score_box[1].text if len(score_box) > 1 else ""
        
        return f"{main_score}\n\n{details}"
    except:
        return "Waiting for Match Data..."

def create_image(text):
    # ලස්සන පසුබිමක් හදමු
    img = Image.new('RGB', (1280, 720), color = (10, 10, 40))
    d = ImageDraw.Draw(img)
    
    # Border එකක් අඳිමු
    d.rectangle([20, 20, 1260, 700], outline=(255, 215, 0), width=5)
    
    # මැද තියෙන විස්තර කොටුව
    title = "SL VS ZIM T20 LIVE SCORE"
    
    # සිංහලෙන් දාන්න බැරි නිසා ඉංග්‍රීසියෙන් ලොකුවට දාමු
    d.text((450, 100), title, fill=(255, 255, 255))
    
    # ප්‍රධාන විස්තර පේළි කිහිපයකට බෙදා ලියමු
    lines = text.split('\n')
    y_pos = 300
    for line in lines:
        d.text((150, y_pos), line, fill=(0, 255, 0)) # කොළ පාටින් ලකුණු සහ බැටර්ස්ලා
        y_pos += 60

    img.save('status.png')

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    # GitHub Secrets වලින් ගන්නා Key එක
    STREAM_KEY = os.getenv("STREAM_KEY")
    
    print("Starting Scoreboard Stream...")
    
    start_time = time.time()
    while time.time() - start_time < 14400: # පැය 4ක්
        score_data = get_match_data()
        create_image(score_data)
        
        # FFmpeg Command - Audio සහ Video Format නිවැරදි කර ඇත
        cmd = f'ffmpeg -re -loop 1 -t 30 -i status.png -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -c:v libx264 -preset veryfast -b:v 2500k -pix_fmt yuv420p -c:a aac -shortest -f flv {YOUTUBE_URL}/{STREAM_KEY}'
        os.system(cmd)
        
        time.sleep(2) # පොඩි විවේකයක්
