import re
import urllib.parse
from typing import List, Optional
from datetime import datetime, timedelta, timezone

import bs4
import requests
from podgen import Podcast, Episode, Media

from tapes.util import log


def _stripped_text(elem):
    return re.sub('\\s+', ' ', elem.get_text()).strip()


def _extract_podcast(table_elem, current_title, page_url) -> Optional[Podcast]:
    episodes = []

    # We use fake, increasing publication dates for all episodes so that they
    # podcast clients show them in the same order as they are listed on the
    # web page.
    publication_date = datetime.fromtimestamp(0, timezone.utc)

    # Look for links to MP3s in each row of the table. Use the content of the
    # first column as an episode's title.
    for row_elem in table_elem.find_all('tr'):
        for link_elem in row_elem.find_all('a'):
            href = link_elem.get('href')

            if href and href.endswith('.mp3'):
                episode_title = _stripped_text(row_elem.find('td'))
                mp3_media_url = urllib.parse.urljoin(page_url, href)

                if current_title is None:
                    log(f'Warning: Found link to FLAC file "{mp3_media_url}" '
                        f'without detecting a preceding title.')
                else:
                    episode = Episode(
                        title=episode_title,
                        media=Media(mp3_media_url),
                        publication_date=publication_date)

                    episodes.append(episode)
                    publication_date += timedelta(days=1)

    # Podgen requires a description to be set, but we're not extracting one
    # from the processed web pages.
    return Podcast(
        name=current_title,
        website=page_url,
        explicit=False,
        description='☎️',
        episodes=episodes)


def extract_podcasts(page_url) -> List[Podcast]:
    soup = bs4.BeautifulSoup(requests.get(page_url).text, 'lxml')
    current_title = None
    podcasts = []

    for elem in soup.find_all():
        if elem.name == 'font' and elem.get('size') == '3':
            current_title = _stripped_text(elem)
        elif elem.name == 'table' and not elem.find('table'):
            podcast = _extract_podcast(elem, current_title, page_url)

            # We might get table elements that don't contain episodes.
            if podcast.episodes:
                podcasts.append(podcast)

    return podcasts
