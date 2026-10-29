"""
Render the Reddit version of the horror rating vs. jump scares chart (D3.js -> PNG).

Input is the csv written by plot_horror_jump_scares.ipynb. The data is injected into
horror_chart_template.html, which is saved next to the png (open it in a browser for the
interactive version with tooltips) and screenshot with headless Chromium via Playwright.
"""
import json
import os
from datetime import date

import polars as pl
from playwright.sync_api import sync_playwright
from scipy.stats import spearmanr

from mapy.paths import OUTPUT_DIR

INPUT_FILE = os.path.join(OUTPUT_DIR, 'horror_rating_vs_jump_scares.csv')
INPUT_ALL_FILE = os.path.join(OUTPUT_DIR, 'horror_rating_vs_jump_scares_all.csv')  ## All rated
TEMPLATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'horror_chart_template.html')
OUTPUT_HTML = os.path.join(OUTPUT_DIR, 'horror_rating_vs_jump_scares_reddit.html')
OUTPUT_PNG = os.path.join(OUTPUT_DIR, 'horror_rating_vs_jump_scares_reddit.png')
OUTPUT_JPG = os.path.join(OUTPUT_DIR, 'horror_rating_vs_jump_scares_reddit.jpg')  ## For upload
N_TOP = 100
SCALE = 2  ## Device pixel ratio of the screenshot: 1800x1560 css px -> 3600x3120 png

COLUMNS = ['rank', 'title', 'year', 'rating', 'imdb_rating', 'lb_rating', 'rt_avg', 'mc_score',
           'jump_scares', 'wjs_major', 'wtj_total']

if __name__ == '__main__':
    for f in [INPUT_FILE, INPUT_ALL_FILE]:
        assert os.path.exists(f), 'Run plot_horror_jump_scares.ipynb first, it writes {}'.format(f)

    df = pl.read_csv(INPUT_FILE).sort('rank').head(N_TOP)
    df = df.select(COLUMNS).with_columns(pl.int_range(1, pl.len() + 1).alias('position'))
    rho, _ = spearmanr(df['rating'], df['jump_scares'])
    df_all = pl.read_csv(INPUT_ALL_FILE)
    rho_all, _ = spearmanr(df_all['rating'], df_all['jump_scares'])
    data = {
        'movies': df.to_dicts(),
        'rho': rho,
        'rho_all': rho_all,
        'n_all': df_all.height,
        'skipped': int(df['rank'].max()) - N_TOP,  ## Higher ranked movies without jump scare data
        'retrieved': date.fromtimestamp(os.path.getmtime(INPUT_FILE)).strftime('%b %-d, %Y'),
    }

    with open(TEMPLATE_FILE) as f:
        html = f.read().replace('__DATA__', json.dumps(data).replace('</', '<\\/'))
    with open(OUTPUT_HTML, 'w') as f:
        f.write(html)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1800, 'height': 1560},
                                device_scale_factor=SCALE)
        page.on('console', lambda msg: print('[browser]', msg.text))
        page.on('pageerror', lambda err: print('[browser error]', err))
        page.goto('file://' + os.path.abspath(OUTPUT_HTML))
        ## Label placement is slow, and much slower on a busy cpu
        page.wait_for_function('window.chartReady === true', timeout=120000)
        page.locator('#poster').screenshot(path=OUTPUT_PNG)
        page.locator('#poster').screenshot(path=OUTPUT_JPG, type='jpeg', quality=92)
        browser.close()
    print(OUTPUT_PNG, 'and', OUTPUT_JPG, 'were saved.')

