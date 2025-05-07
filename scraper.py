
import requests
import os
import datetime
import subprocess
import random

CWD = '/home/isaac/Pictures/wallpapers/'
LAST_POLL_PATH  = os.path.join(CWD, 'last-poll.txt')
FORMAT = '%Y-%m-%d'
REQUEST_URL = 'https://wallhaven.cc/api/v1/search?atleast=1920x1080&ratios=16x9&sorting=toplist&topRange=1y'

def download(_id):
    with open("image.png", 'wb') as f:
        content = requests.get(f'https://wallhaven.cc/api/v1/w/{_id}')
        image = requests.get(content.json()['data']['path'])
        f.write(image.content)

def retrieve_top():
    results = requests.get(REQUEST_URL)
    response = [i['path'] for i in results.json()['data']]
    
    # print(len(results.json()['data']))
    # for index, i in enumerate(results.json()['data']):
    #     print(index, i['path'])

    return response

def download_all(urls):
    has_one_downloaded = False
    for i in urls:

        with open(os.path.join(CWD, i.split('/')[-1]), 'wb') as f:
            image = requests.get(i)
            f.write(image.content)

        if not has_one_downloaded:
            has_one_downloaded = True
            
            with open(LAST_POLL_PATH, 'w') as f:
                f.write(datetime.datetime.now().strftime(FORMAT))

            pick(os.path.join(CWD, i.split('/')[-1]))

def should_poll():
    if not os.path.isfile(LAST_POLL_PATH):
        return True  
    
    with open(LAST_POLL_PATH, 'r') as f:
        return datetime.datetime.now() - datetime.datetime.strptime(f.read().strip(), FORMAT) > datetime.timedelta(days=1)

def poll():
    for i in os.listdir(CWD):
        if '.jpg' in i or '.png' in i and i != 'fallback.jpg':
            os.remove(os.path.join(CWD, i))

    download_all(retrieve_top())

def pick(choice=None):
    
    if choice == None:
        last_wallpaper_path = os.path.join(CWD, 'last-wallpaper.txt')
        if os.path.isfile(last_wallpaper_path):
            with open(last_wallpaper_path, 'r') as f:
                last_wallpaper_image = f.read()
            choice = os.path.join(CWD, random.choice([i for i in os.listdir(CWD) if '.jpg' in i or '.png' in i and i != last_wallpaper_image]))
        else:
            choice = os.path.join(CWD, random.choice([i for i in os.listdir(CWD) if '.jpg' in i or '.png' in i]))

    subprocess.run(['wal', '-i', choice])
    
    with open(last_wallpaper_path, 'w') as f:
        f.write(choice.split('/')[-1])
    
def pick_default():
    subprocess.run(['wal', '-i', os.path.join(CWD, 'fallback.jpg')])

def main():
    if should_poll():
        poll()
    
    else:
        pick()

if __name__ == '__main__':
    main()


