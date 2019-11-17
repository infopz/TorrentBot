import requests
import re
from bs4 import BeautifulSoup

from config import tv_time_user, tv_time_password, tv_time_user_id


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

base_url = 'https://www.tvtime.com'

translation = {"Cosmos (2014)": "Cosmos", "Disenchantment": "Disincanto", "Glitch (2015)": "Glitch",
               "Love, Death &amp; Robots": "Love Death Robot", "Maniac (2018)": "Maniac",
               "Chilling Adventures of Sabrina": "Le terrificanti avventure di sabrina",
               "Mars (2016)": "mars 2016", "Money Heist": "la casa di carta", "Mr. Robot": "mr robot",
               "The End of the F***ing World": "the end of the f"}


def get_show_list():
    with requests.Session() as s:
        form = {
            'username': tv_time_user,
            'password': tv_time_password,
            'redirect_path': base_url + '/en'
        }
        s.post(base_url+'/signin', data=form, headers=headers)
        r = s.get(base_url+"/en/user/" + tv_time_user_id + "/profile", headers=headers)
    soup = BeautifulSoup(r.text, features="html.parser")
    all_show = soup.find(id="all-shows")
    s = all_show.find_all("li")
    titles = []
    for show in s:
        show = str(show).replace("\n", "")
        title = re.findall('<h2><a href="/en/show/.+">(.+)</a></h2>', show)[0].strip()
        if title in translation:
            title = translation[title]
        titles.append(title)
    return titles


