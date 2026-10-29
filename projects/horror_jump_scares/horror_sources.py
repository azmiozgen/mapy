"""
Fetch and parse horror movie ratings and jump scare counts.

Sources:
    * IMDb datasets      https://datasets.imdbws.com/
    * Wikidata SPARQL    IMDb id -> Rotten Tomatoes / Metacritic ids
    * Letterboxd         https://letterboxd.com/imdb/<imdb_id>/
    * Rotten Tomatoes    https://www.rottentomatoes.com/<rt_id>
    * Metacritic         https://www.metacritic.com/<mc_id>/
    * WhenJumpScare      https://www.whenjumpscare.com/movie/<tmdb_id>
    * Where's The Jump   https://wheresthejump.com/full-movie-list/

Every response is cached on disk, so re-running only hits the network for new urls.
"""
import hashlib
import html
import json
import os
import re
import threading
import time
import unicodedata
from urllib.parse import urlparse

import requests

from mapy.paths import DATA_DIR

CACHE_DIR = os.path.join(DATA_DIR, 'cache', 'horror', 'pages')
USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
WIKIDATA_USER_AGENT = 'mapy-horror-jump-scares/0.1 (personal data visualization project)'
REQUEST_DELAY = 1.0  ## Seconds between two network requests to the same domain
WTJ_URL = 'https://wheresthejump.com/full-movie-list/'
WJS_SITEMAP_URL = 'https://www.whenjumpscare.com/sitemap.xml'

_last_request = {}
_domain_locks = {}
_locks_guard = threading.Lock()


def _domain_lock(domain):
    with _locks_guard:
        return _domain_locks.setdefault(domain, threading.Lock())


def fetch(url, cache_dir=CACHE_DIR, delay=REQUEST_DELAY):
    """
    Return (status_code, final_url, text) for url, using the on-disk cache.
    Requests to the same domain are spaced by at least `delay` seconds.
    """
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, hashlib.sha1(url.encode()).hexdigest() + '.json')
    if os.path.exists(path):
        with open(path) as f:
            cached = json.load(f)
        return cached['status'], cached['final_url'], cached['text']

    domain = urlparse(url).netloc
    with _domain_lock(domain):
        wait = _last_request.get(domain, 0) + delay - time.time()
        if wait > 0:
            time.sleep(wait)
        try:
            response = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=30)
            status, final_url, text = response.status_code, response.url, response.text
        except requests.RequestException as e:
            status, final_url, text = -1, url, str(e)
        _last_request[domain] = time.time()

    ## Cache only definitive answers, so transient errors are retried next run
    if status in (200, 404, 410):
        with open(path, 'w') as f:
            json.dump({'status': status, 'final_url': final_url, 'text': text}, f)
    return status, final_url, text


def _json_ld_movie(text):
    """
    Return the first schema.org Movie object found in the page's JSON-LD blocks.
    """
    pattern = r'<script type="application/ld\+json"[^>]*>(.*?)</script>'
    for block in re.findall(pattern, text, re.S):
        block = re.sub(r'/\*.*?\*/', '', block, flags=re.S).strip()  ## Letterboxd CDATA
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        candidates = data if isinstance(data, list) else data.get('@graph', [data])
        for item in candidates:
            if isinstance(item, dict) and item.get('@type') == 'Movie':
                return item
    return None


## ---------------------------------------------------------------- Wikidata

def wikidata_ids(imdb_ids, batch_size=200):
    """
    Return {imdb_id: {'rt': [rt ids], 'mc': [metacritic ids]}} from Wikidata.
    """
    query_template = """
    SELECT ?imdb ?rt ?mc WHERE {{
      VALUES ?imdb {{ {} }}
      ?film wdt:P345 ?imdb .
      OPTIONAL {{ ?film wdt:P1258 ?rt . }}
      OPTIONAL {{ ?film wdt:P1712 ?mc . }}
    }}"""
    ids = {}
    imdb_ids = list(imdb_ids)
    for i in range(0, len(imdb_ids), batch_size):
        values = ' '.join('"{}"'.format(x) for x in imdb_ids[i:i + batch_size])
        response = requests.get('https://query.wikidata.org/sparql',
                                params={'query': query_template.format(values),
                                        'format': 'json'},
                                headers={'User-Agent': WIKIDATA_USER_AGENT},
                                timeout=120)
        response.raise_for_status()
        for row in response.json()['results']['bindings']:
            entry = ids.setdefault(row['imdb']['value'], {'rt': [], 'mc': []})
            for key in ('rt', 'mc'):
                value = row.get(key, {}).get('value')
                if value and value not in entry[key]:
                    entry[key].append(value)
        time.sleep(REQUEST_DELAY)
    return ids


## ---------------------------------------------------------------- Ratings

def _directors(movie):
    """
    Director surnames (lower-case, accent-free) from a JSON-LD Movie object.
    """
    people = movie.get('director') or []
    if isinstance(people, dict):
        people = [people]
    surnames = set()
    for person in people:
        name = html.unescape(person.get('name') or '').lower()
        name = name.translate(str.maketrans({'ł': 'l', 'ø': 'o', 'đ': 'd', 'ß': 'ss'}))
        name = unicodedata.normalize('NFKD', name)
        name = re.sub(r'[^a-z ]', '', name.encode('ascii', 'ignore').decode().lower())
        if name.split():
            surnames.add(name.split()[-1])
    return surnames


def parse_letterboxd(text):
    """
    Letterboxd film page -> average rating (out of 5), rating count, genres, year, TMDB id.
    """
    movie = _json_ld_movie(text) or {}
    rating = movie.get('aggregateRating') or {}
    year = re.search(r'/films/year/(\d{4})/', text)
    tmdb_id = re.search(r'themoviedb\.org/movie/(\d+)', text)
    return {
        'lb_rating': float(rating['ratingValue']) if 'ratingValue' in rating else None,
        'lb_count': int(rating['ratingCount']) if 'ratingCount' in rating else None,
        'lb_genres': movie.get('genre') or [],
        'lb_year': int(year.group(1)) if year else None,
        'lb_tmdb_id': int(tmdb_id.group(1)) if tmdb_id else None,
        'lb_title': html.unescape(movie.get('name') or ''),
        'lb_directors': _directors(movie),
    }


def letterboxd(imdb_id):
    status, final_url, text = fetch('https://letterboxd.com/imdb/{}/'.format(imdb_id))
    if status != 200:
        return {'lb_url': None}
    return {'lb_url': final_url, **parse_letterboxd(text)}


def parse_rotten_tomatoes(text):
    """
    Rotten Tomatoes movie page -> critics' average rating (out of 10), Tomatometer, year.
    """
    result = {'rt_avg': None, 'rt_reviews': None, 'rt_tomatometer': None, 'rt_year': None}
    match = re.search(r'<script[^>]*id="media-scorecard-json"[^>]*>(.*?)</script>', text, re.S)
    if match:
        critics = json.loads(match.group(1)).get('criticsScore') or {}
        if critics.get('averageRating'):
            result['rt_avg'] = float(critics['averageRating'])
        if critics.get('reviewCount') is not None:
            result['rt_reviews'] = int(critics['reviewCount'])
        if critics.get('score'):
            result['rt_tomatometer'] = int(critics['score'])
    movie = _json_ld_movie(text) or {}
    ## "releaseDate" is the latest (re-)release; "releaseYear" and dateCreated are the original
    match = re.search(r'"releaseYear":"(\d{4})"', text)
    if match:
        result['rt_year'] = int(match.group(1))
    elif movie.get('dateCreated'):
        result['rt_year'] = int(movie['dateCreated'][:4])
    result['rt_directors'] = _directors(movie)
    return result


def rotten_tomatoes(rt_id):
    status, final_url, text = fetch('https://www.rottentomatoes.com/{}'.format(rt_id))
    if status != 200:
        return {'rt_url': None}
    return {'rt_url': final_url, **parse_rotten_tomatoes(text)}


def parse_metacritic(text):
    """
    Metacritic movie page -> Metascore (out of 100), number of critic reviews, year (US release).
    """
    movie = _json_ld_movie(text) or {}
    rating = movie.get('aggregateRating') or {}
    year = None
    if movie.get('datePublished'):
        year = int(movie['datePublished'][:4])
    return {
        'mc_score': int(rating['ratingValue']) if 'ratingValue' in rating else None,
        'mc_reviews': int(rating['reviewCount']) if 'reviewCount' in rating else None,
        'mc_year': year,
        'mc_directors': _directors(movie),
    }


def metacritic(mc_id):
    status, final_url, text = fetch('https://www.metacritic.com/{}/'.format(mc_id))
    if status != 200:
        return {'mc_url': None}
    return {'mc_url': final_url, **parse_metacritic(text)}


def best_match(results, year, directors, prefix, value_key):
    """
    Among candidate pages of one site, keep those that are the same movie and have a value:
    release year within 1 of `year`, or a director in common with `directors` (re-releases,
    late US releases). Return the one with the closest year, plus the rejected pages.
    """
    usable = [r for r in results if r.get(value_key) is not None]
    same_movie = [r for r in usable
                  if abs((r.get(prefix + '_year') or 9999) - year) <= 1
                  or directors & r.get(prefix + '_directors', set())]
    rejected = [r for r in usable if r not in same_movie]
    if not same_movie:
        return {}, rejected
    best = min(same_movie, key=lambda r: abs((r.get(prefix + '_year') or 9999) - year))
    return best, rejected


## ---------------------------------------------------------------- Jump scares

def wjs_movie_ids():
    """
    Return {tmdb_id: url} for every movie listed in WhenJumpScare's sitemap.
    """
    status, _, text = fetch(WJS_SITEMAP_URL)
    assert status == 200, 'WhenJumpScare sitemap not reachable ({})'.format(status)
    urls = re.findall(r'<loc>(https://www\.whenjumpscare\.com/movie/(\d+)-[^<]*)</loc>', text)
    return {int(tmdb_id): url for url, tmdb_id in urls}


def parse_whenjumpscare(text):
    """
    WhenJumpScare movie page -> total, major and minor jump scare counts, and contributors.
    """
    result = {'wjs_total': None, 'wjs_major': None, 'wjs_minor': None}
    plain = re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', '', text, flags=re.S))
    plain = html.unescape(plain)
    result['wjs_contributors'] = sorted(set(
        name.strip() for name in re.findall(r'Credit:\s+(.+?)\s+Spoiler', plain)))
    match = re.search(r'All (\d+) jumpscare timestamps? for .*? — (\d+) major, (\d+) minor', text)
    if not match:  ## Pages without the summary sentence
        match = re.search(r'(\d+)\s+Jumpscares?\s+(\d+)\s+major\s+·\s+(\d+)\s+minor', plain)
    if match:
        result['wjs_total'], result['wjs_major'], result['wjs_minor'] = map(int, match.groups())
    elif re.search(r'\b0\s+Jumpscares\b|No jumpscares', plain, re.I):
        result['wjs_total'], result['wjs_major'], result['wjs_minor'] = 0, 0, 0
    return result


def whenjumpscare(url):
    status, final_url, text = fetch(url)
    if status != 200:
        return {'wjs_url': None}
    return {'wjs_url': final_url, **parse_whenjumpscare(text)}


def wheresthejump():
    """
    Where's The Jump full movie list -> list of dicts (title, director, year, count, rating).
    """
    status, _, text = fetch(WTJ_URL, delay=20)  ## Their robots.txt asks for a 20 s crawl delay
    assert status == 200, "Where's The Jump list not reachable ({})".format(status)
    rows = []
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>', text, re.S):
        cells = [html.unescape(re.sub(r'<[^>]+>', '', c)).strip()
                 for c in re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)]
        if len(cells) < 5 or not cells[2].isdigit() or not cells[3].isdigit():
            continue
        rows.append({'wtj_title': cells[0], 'wtj_director': cells[1], 'wtj_year': int(cells[2]),
                     'wtj_total': int(cells[3]),
                     'wtj_rating': float(cells[4]) if cells[4] else None})
    return rows


def normalize_title(title):
    """
    Lower-case, ascii-ish, punctuation-free title for fuzzy joining.
    """
    title = html.unescape(title).lower().replace('&', 'and')
    title = re.sub(r'[’\'`]', '', title)
    title = re.sub(r'[^a-z0-9]+', ' ', title).strip()
    return re.sub(r'^(the|a|an) ', '', title)

