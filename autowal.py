
import requests
import os
import datetime
import subprocess
import random
from platformdirs import user_config_dir, user_data_dir
import configparser

APP_NAME = "autowal"
CONFIG_DIR = user_config_dir(APP_NAME)
DATA_DIR = user_data_dir(APP_NAME)

os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.ini')
LAST_POLL_PATH = os.path.join(CONFIG_DIR, 'last-poll.txt')
LAST_WALLPAPER_PATH = os.path.join(CONFIG_DIR, 'last-wallpaper.txt')
FALLBACK_WALLPAPER_PATH = os.path.join(CONFIG_DIR, 'fallback.jpg') 
FORMAT = '%Y-%m-%d'

BASE_REQUEST_URL = 'https://wallhaven.cc/api/v1/search?atleast={}&ratios={}&sorting={}&topRange={}'
FALLBACK_CONFIG = (
'''
[wallhaven]
atleast = 1920x1080
ratios = 16x9
sorting = toplist
topRange = 1y
'''
)

def show_config():
    print(f'\nCurrent configuration (found at {CONFIG_PATH}):')
    print('Documentation can be found at https://wallhaven.cc/help/api\n')
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        print(f.read())

def retrieve_url():
    '''
    this function only returns the request url currently but can expand
    when the config expands
    '''

    if not os.path.isfile(CONFIG_DIR):
        with open(CONFIG_PATH, 'w') as f:
            f.write(FALLBACK_CONFIG)
    
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    params = [config.get("wallhaven", i) for i in ["atleast", "ratios", "sorting", "topRange"]]
    return BASE_REQUEST_URL.format(*params)
        

def retrieve_wallpaper_urls():

    results = requests.get(retrieve_url())
    urls = [i['path'] for i in results.json()['data']]
    
    return urls

def log_last_poll():

    with open(LAST_POLL_PATH, 'w') as f:
        f.write(datetime.datetime.now().strftime(FORMAT))

def download_all(urls):

    has_one_downloaded = False
    for i in urls:
        filename = i.split('/')[-1]
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'wb') as f:
            image = requests.get(i)
            f.write(image.content)

        if not has_one_downloaded:
            has_one_downloaded = True
            log_last_poll()            
            pick(filepath)

def should_poll():

    if not os.path.isfile(LAST_POLL_PATH):
        return True  
    
    with open(LAST_POLL_PATH, 'r') as f:
        return datetime.datetime.now() - datetime.datetime.strptime(f.read().strip(), FORMAT) > datetime.timedelta(days=1)

def poll():
    for i in os.listdir(DATA_DIR):
        if '.jpg' in i or '.png' in i and i != 'fallback.jpg':
            os.remove(os.path.join(DATA_DIR, i))
    
    try:
        download_all(retrieve_wallpaper_urls())
    except:
        print("Errors occurred during polling.")

def pick(choice=None):
    
    try:
        if choice == None:
            if os.path.isfile(LAST_WALLPAPER_PATH):
                with open(LAST_WALLPAPER_PATH, 'r') as f:
                    last_wallpaper_image = f.read()

                wallpaper_options = [i for i in os.listdir(DATA_DIR) if '.jpg' in i or '.png' in i and i != last_wallpaper_image]
            else:
                wallpaper_options = [i for i in os.listdir(DATA_DIR) if '.jpg' in i or '.png' in i]
            
            if len(wallpaper_options) == 0:
                download_all(retrieve_wallpaper_urls())
                quit()

            choice = os.path.join(DATA_DIR, random.choice(wallpaper_options))

        subprocess.run(['wal', '-i', choice])
        
        with open(LAST_WALLPAPER_PATH, 'w') as f:
            f.write(os.path.split(choice)[-1])

    except Exception as e:
        
        print('Errors occurred while choosing a new wallpaper.')
        print(f'Falling back to {FALLBACK_WALLPAPER_PATH}.')
        
        if not os.path.isfile(FALLBACK_WALLPAPER_PATH):
            raise Exception("Fallback wallpaper not properly initialized.")

        subprocess.run(['wal', '-i', FALLBACK_WALLPAPER_PATH])
        raise e
    
def main():
    if should_poll():
        poll()
    
    else:
        pick()

if __name__ == '__main__':
    main()


