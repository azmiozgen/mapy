# Horror movie ratings vs. jump scares

![Horror movie rating vs. jump scares](../../docs/images/horror_rating_vs_jump_scares_reddit.jpg)

Do the best horror movies rely on jump scares? Each dot is one of the 100 highest-rated horror
movies, placed by its combined rating and its number of jump scares.

## Method

* **Rating:** mean of IMDb (x10), Letterboxd (x20), Metacritic Metascore and the Rotten Tomatoes
  critics' *average rating* (x10, not the Tomatometer), all on a 0-100 scale. A movie needs at
  least 3 of the 4 scores and 25,000 IMDb votes.
* **Horror:** at least one genre tag containing "horror" on IMDb, TMDB or Letterboxd. "Thriller"
  alone does not count.
* **Jump scares:** [WhenJumpScare](https://www.whenjumpscare.com), with
  [Where's The Jump](https://wheresthejump.com) as fallback and cross-check.
* **Matching:** IMDb ids are mapped to Rotten Tomatoes and Metacritic pages with Wikidata. A page
  counts only if its release year is within one year or its director matches.

## Results

* Among the top 100: Spearman ρ = -0.11 (p = 0.29), no meaningful relationship.
* Across all 438 popular horror movies with jump scare data: ρ = -0.19 (p < 0.001), a weak link
  between more jump scares and slightly lower ratings. It holds after controlling for release
  year (partial ρ = -0.18).

## Caveats

* Jump scare counts are crowd-sourced and there is no standard definition of a jump scare.
  WhenJumpScare bulk-imported Where's The Jump, so agreement between them is not independent.
* 54 higher-rated movies, mostly before 1960, have no jump scare data on either site, so this is
  the top 100 *among movies with data*.
* The y-axis uses a square-root scale, because most movies have 0-5 jump scares.

## Files

| File | What it does |
|---|---|
| `horror_sources.py` | Fetches and parses every source. Responses are cached in `data/cache/horror/pages`, with about one request per second per site. |
| `plot_horror_jump_scares.ipynb` | Builds the candidate pool, combines ratings, joins jump scares, writes the csv files and matplotlib versions of the plot |
| `horror_chart_template.html` | D3.js poster template |
| `plot_horror_jump_scares_web.py` | Injects the csv data into the template and screenshots it with Playwright |

## Run

1. Download `title.basics.tsv.gz` and `title.ratings.tsv.gz` from
   [IMDb datasets](https://datasets.imdbws.com/) into `data/cache/horror/imdb/`, and the TMDB
   csv (see [data sources](../../docs/data_sources.md)) into `data/`.
2. Run `plot_horror_jump_scares.ipynb`. The first run scrapes a few thousand pages and takes a
   while; later runs read from the cache.
3. `python projects/horror_jump_scares/plot_horror_jump_scares_web.py` writes the poster to
   `data/output/horror_rating_vs_jump_scares_reddit.{html,png,jpg}`.

Ratings and jump scare counts were retrieved on Oct 8, 2026.
