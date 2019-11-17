import feedparser
import requests
import re
import db
from bs4 import BeautifulSoup

import tvtime

rss_link = "feed://ilcorsaronero.unblocker.cc/rsscat.php?cat=15"


def get_list():
    l = tvtime.get_show_list()
    return create_match_list(l)


def check_rss():
    feed = feedparser.parse(rss_link)
    feed = feed.entries
    return feed


def create_match_list(show_list):
    m_list = []
    for s in show_list:
        s = s.lower()
        m_list.append(s)
        if s.find(" ") != -1:
            m_list.append(s.replace(" ", "."))
    return m_list


def analize_page(link):
    page = requests.get(link)
    page_parsed = BeautifulSoup(page.text, features="html.parser")
    title = page_parsed.title.text.split("-", 1)[1].rsplit("-", 1)[0].strip()
    magnet = re.findall('''href="(magnet:.+)" title''', page.text)[0]
    size = re.findall("<td>Size</td> <td>(.+)</td>", page.text)[0]
    return title, magnet, size


def analyze_feed(feed):
    tv_list = get_list()
    possible_torrent = []
    last = db.get_last()["name"]
    for f in feed:
        title = f["title"].lower()
        if title == last:
            break
        if any(s in title for s in tv_list):
            title_current, magnet, size = analize_page(f["link"])
            num = db.write_magnet(title, magnet)
            possible_torrent.append({"title": title_current, "magnet": magnet, "size": size, "number": num})
    return possible_torrent



