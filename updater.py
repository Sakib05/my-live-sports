import re
import requests

# ১. টোকেন স্ক্র্যাপ করার সোর্স ইউআরএল
SOURCE_URL = "https://iptvfunproject.pages.dev/" 

# ২. আপনার কাঙ্ক্ষিত সব চ্যানেলের লিস্ট (এখানে Fox ও Sony যুক্ত করা হয়েছে)
CHANNELS = {
    # Fifa sports Net
    "Fifa + (FIFA+)": "https://37b4c228.wurl.com/manifest/f36d25e7e52f1ba8d7e56eb859c636563214f541/UmFrdXRlblRWLWZyX0ZJRkFQbHVzRnJlbmNoX0hMUw/6f5437c5-e015-4754-8476-c8c6d27d3a55/1.m3u8",
    
    # T Sports Net
    "T Sports": "https://tvsen7.aynaott.com/tsports-hd/tracks-v1a1/mono.ts.m3u8",
    
    # Ptv Sports Net
    "Ptv Sports": "https://tvsen5.aynaott.com/PtvSports/tracks-v1a1/mono.ts.m3u8?e=1779283784&token=db1789e36c278bf538489fac263e0ffb&u=78be6644-0a65-48ec-81a4-089ac65a2619",
    
    # TSN Sports Net
    "TSN 1 (TSN1)": "https://tvsen7.aynaott.com/tsn1/tracks-v1a1/mono.ts.m3u8?e=1779283805&token=e5ce886378c54bd381b9833b5d57649a&u=78be6644-0a65-48ec-81a4-089ac65a2619",
    "TSN 2 (TSN2)": "https://tvsen7.aynaott.com/tsn2/tracks-v1a1/mono.ts.m3u8?e=1779283793&token=636d9b8b83d4316193c2d1c9aad8951c&u=78be6644-0a65-48ec-81a4-089ac65a2619",
    "TSN 3 (TSN3)": "https://tvsen7.aynaott.com/tsn3/tracks-v1a1/mono.ts.m3u8?e=1779283805&token=fd3b5d71227f183da51caba4325cee10&u=78be6644-0a65-48ec-81a4-089ac65a2619",
    
    # Fox Sports Net
    "Fox Sports 1 (FS1)": "http://tvsen5.aynaott.com/fs1/tracks-v1a1/mono.ts.m3u8",
    "Fox Sports 2 (FS2)": "http://tvsen5.aynaott.com/fs2/tracks-v1a1/mono.ts.m3u8",
    "Fox Sports (Main)": "http://tvsen5.aynaott.com/foxsports/tracks-v1a1/mono.ts.m3u8",
    
    # Sony Sports Network
    "Sony Sports Ten 1": "http://tvsen5.aynaott.com/sonysports1/tracks-v1a1/mono.ts.m3u8",
    "Sony Sports Ten 2": "http://tvsen5.aynaott.com/sonysports2/tracks-v1a1/mono.ts.m3u8",
    "Sony Sports Ten 3": "http://tvsen5.aynaott.com/sonysports3/tracks-v1a1/mono.ts.m3u8",
    "Sony Sports Ten 5": "http://tvsen5.aynaott.com/sonysports5/tracks-v1a1/mono.ts.m3u8"
}

def get_fresh_token():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        html_content = response.text
        
        # HTML থেকে কারেন্ট ডায়নামিক টোকেন পার্টটুকু স্ক্র্যাপ করা
        match = re.search(r'mono\.ts\.m3u8\?e=(\d+)&token=([a-zA-Z0-9]+)', html_content)
        if match:
            return f"?e={match.group(1)}&token={match.group(2)}"
    except Exception as e:
        print(f"Error scraping token: {e}")
    return ""

def generate_m3u():
    token = get_fresh_token()
    if not token:
        print("Failed to get fresh token. Skipping update.")
        return

    worker_base = "https://throbbing-wildflower-3b14.sakibhossain6111.workers.dev/?url="

    m3u_content = "#EXTM3U\n\n"
    
    for channel_name, base_stream_url in CHANNELS.items():
        # বেজ ইউআরএল + একদম তাজা টোকেন
        final_stream = base_stream_url + token
        # ক্লাউডফ্লেয়ার ওয়ার্কারের প্রক্সি ইউআরএল দিয়ে মোড়ানো
        proxied_url = worker_base + final_stream
        
        # ক্যাটাগরি গ্রুপিং (Fox হলে USA/International, Sony হলে South Asia)
        group = "South Asia (Sony)" if "Sony" in channel_name else "International (Fox)"
        
        m3u_content += f'#EXTINF:-1 tvg-id="{channel_name.replace(" ", "")}" group-title="{group}",{channel_name}\n'
        m3u_content += f'{proxied_url}\n\n'

    with open("sports.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content.strip())
    print("Playlist updated with Fox and Sony channels!")

if __name__ == "__main__":
    generate_m3u()
