import os
import requests
import time
from PIL import Image, ImageDraw
import threading
import xml.dom.minidom

def download_files():
    music_url = "https://github.com/viruna123/Match-live-/releases/download/v1.0/Sri.Lankan.Cricket.Papare.-.Vol.1.mp3"
    if not os.path.exists('papare.mp3'):
        print("Downloading Papare...")
        r = requests.get(music_url)
        with open('papare.mp3', 'wb') as f: f.write(r.content)
    
    img = Image.new('RGB', (1280, 720), color=(5, 10, 45))
    img.save('bg.jpg')

def get_match_data():
    try:
        # ලෝකෙම තියෙන ලයිව් ස්කෝර් RSS එක
        url = "https://static.cricinfo.com/rss/livescores.xml"
        r = requests.get(url, timeout=10)
        xmldoc = xml.dom.minidom.parseString(r.text)
        items = xmldoc.getElementsByTagName('description')
        
        match_text = "Live Cricket Updating..."
        for item in items:
            score_val = item.firstChild.nodeValue
            # ශ්‍රී ලංකාව හෝ සිම්බාබ්වේ සම්බන්ධ මැච් එක හොයමු
            if "Sri Lanka" in score_val or "Zimbabwe" in score_val or "SL" in score_val:
                match_text = score_val
                break
        
        return f"T20 WORLD CUP 2026\n\n{match_text}"
    except:
        return "T20 WORLD CUP 2026\nSL vs ZIM - Score Updating..."

def update_image_loop():
    while True:
        text = get_match_data()
        try:
            img = Image.open('bg.jpg')
            d = ImageDraw.Draw(img)
            # ලස්සන ස්කෝර් බෝඩ් එකක් (Glass look)
            d.rectangle([50, 150, 1230, 550], fill=(0, 0, 50, 200), outline=(0, 255, 255), width=4)
            
            y_pos = 220
            lines = text.split('\n')
            for i, line in enumerate(lines):
                # පළවෙනි පේළිය Cyan පාටින්, අනිත්වා සුදු පාටින්
                color = (0, 255, 255) if i == 0 else (255, 255, 255)
                # අකුරු මැදට ගන්න (Center align)
                d.text((100, y_pos), line, fill=color)
                y_pos += 100
            
            img.save('status.png')
        except Exception as e:
            print(f"Img Error: {e}")
        time.sleep(15)

if __name__ == "__main__":
    YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
    STREAM_KEY = os.getenv("STREAM_KEY")
    
    download_files()
    
    img_thread = threading.Thread(target=update_image_loop)
    img_thread.daemon = True
    img_thread.start()
    
    print("Stream starting... Papare + RSS Score")
    
    # FFmpeg settings (Bitrate ekath thawa poddak adu kala fix wenna)
    cmd = (
        f'ffmpeg -re -loop 1 -i status.png -stream_loop -1 -i papare.mp3 '
        f'-c:v libx264 -preset ultrafast -b:v 1200k -maxrate 1200k -bufsize 2400k '
        f'-pix_fmt yuv420p -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 '
        f'-f flv {YOUTUBE_URL}/{STREAM_KEY}'
    )
    os.system(cmd)
