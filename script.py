from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import math, os, urllib.request, time, json
import tweepy

# customize
screen_name='AniketTeredesai'
target = 100
primary_arc_color = '#d2d2d2'
secondary_arc_color = '#2e2e2e'

# load cached followers count
with open('data.json', 'r') as f:
    data = json.load(f)
cached_count = data['followers_count']

# load environment variables
load_dotenv()
APP_KEY = os.environ['API_KEY']
APP_SECRET = os.environ['API_SECRET_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# change user-agent (just a precaution)
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

# API connection
auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def get_followers_count(screen_name):
    user = api.get_user(screen_name=screen_name, include_entities=False)
    followers_count = user.followers_count
    print('fetched followers count')
    return followers_count

def calculate_progress(followers, target):
    percentage = (followers/target)*100
    angle = (360*percentage)/100
    print('completed calculations')
    return [f'{int(percentage)}%', angle]

def create_progress_ring(percentage, fill_angle, bg_arc_clr, top_arc_clr):
    #some configurations
    ring_width = 46
    R = center_x = center_y = 379 #radius of the circle minus half of the ring_width + 2 offset
    font = ImageFont.truetype('Roboto-Bold.ttf', 20)
    fill_angle -=90

    ring_bg = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    ring = ImageDraw.Draw(ring_bg)
    ring.arc([(0,0), ring_bg.size], start=0, end=360, fill=bg_arc_clr, width=ring_width)
    ring.arc([(0, 0), ring_bg.size], start=-90, end=fill_angle, fill=top_arc_clr, width=ring_width)
    text_x = R * math.cos(math.radians(fill_angle-5)) + center_x + 2 # another +2 offset
    text_y = R * math.sin(math.radians(fill_angle-5)) + center_y + 2
    ring.text((text_x, text_y), percentage, (255, 255, 255), font=font)
    ring = ring_bg.resize((400, 400), Image.LANCZOS) #smoothens the arc

    profile = Image.open('profile.jpg').convert('RGB')
    profile = profile.resize((400, 400))
    profile.paste(ring, (0,0), ring)
    profile.save('upload.jpg')

def upload_avatar():
    api.update_profile_image(filename='upload.jpg')
    print('Upload Success!')

def get_new_profile_img(screen_name):
    user = api.get_user(screen_name=screen_name, include_entities=False)
    print('fetched profile url')
    img_url = user.profile_image_url_https.replace('_normal', '_400x400')
    file, _ = urllib.request.urlretrieve(img_url)
    img = Image.open(file).convert('RGB')
    img = img.resize((400, 400)) #just to be safe
    img.save('profile.jpg')
    print('fetched avatar')

def start_polling(screen_name,target, cached_count, bg_arc_clr, top_arc_clr):
    while True:
        try:
            followers_count = get_followers_count(screen_name)
            if followers_count != cached_count:
                print('detected change in followers')
                cached_count = followers_count
                cached_obj = {'followers_count': cached_count}
                with open('data.json', 'w') as f:
                    json.dump(cached_obj, f)
                create_progress_ring(*calculate_progress(followers_count, target), bg_arc_clr, top_arc_clr)
                upload_avatar()
            else:
                print('no change detected')
            time.sleep(60)
            print('checking again...')
        except KeyboardInterrupt:
            print('exit')
            break

menu_res = input('type `reset` to start the script from scratch or `poll` to use cached data from previous run\n').lower()
if menu_res == 'reset':
    get_new_profile_img(screen_name)
    cached_count = 0
    start_polling(screen_name, target, cached_count, primary_arc_color, secondary_arc_color)
elif menu_res == 'poll':
    start_polling(screen_name, target, cached_count, primary_arc_color, secondary_arc_color)
else:
    print('invalid response. quitting...')