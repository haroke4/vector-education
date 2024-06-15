from pprint import pprint

import requests
import vimeo

ACCESS_TOKEN = '3a666c6de34f774d71d2fcc0615deb24'


def get_video_link_from_vimeo(vimeo_link):
    video_id = vimeo_link.split('/')[-1]
    print(video_id, vimeo_link)

    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
    response = requests.get(f'https://api.vimeo.com/videos/{video_id}?fields=play', headers=headers)
    progressive = response.json()['play']['progressive']
    video = [video for video in progressive if video['rendition'] == '1080p'][0]
    expire_time = video['link_expiration_time']
    video_link = video['link']
    print(expire_time)
    print(video_link)

get_video_link_from_vimeo('https://vimeo.com/957650207')