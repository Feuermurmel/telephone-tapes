import re
import urllib.parse
from typing import Optional, List

import bs4
import requests
from podgen import Podcast, Episode, Media

from tapes.util import log


def stripped_text(elem):
    return re.sub('\\s+', ' ', elem.get_text()).strip()


def extract_podcasts(page_url) -> List[Podcast]:
    soup = bs4.BeautifulSoup(requests.get(page_url).text, 'lxml')
    current_podcast_name = None
    podcasts = []

    for i in soup.find_all():
        if i.name == 'font' and i.get('size') == '3':
            current_podcast_name = stripped_text(i)
        elif i.name == 'table' and not i.find('table'):
            episodes = []

            for row_elem in i.find_all('tr'):
                for link_elem in row_elem.find_all('a'):
                    href = link_elem.get('href')

                    if href and href.endswith('.flac'):
                        episode_title = stripped_text(row_elem.find('td'))
                        flac_media_url = urllib.parse.urljoin(page_url, href)

                        if current_podcast_name is None:
                            log(f'Warning: Found link to FLAC file '
                                f'"{flac_media_url}" without detecting a '
                                f'preceding title.')
                        else:
                            media = Media(flac_media_url, type='audio/flac')
                            episodes.append(
                                Episode(title=episode_title, media=media))

            if episodes:
                podcast = Podcast(
                    name=current_podcast_name,
                    website=page_url,
                    explicit=False,
                    description='☎️',
                    episodes=episodes)

                podcasts.append(podcast)

    return podcasts