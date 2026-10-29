# Data sources

The `data/` folder is not tracked: the files are large, some are third-party data that is
better downloaded from its source, and the rest are caches. Put the files below in `data/` to
re-run a project.

| File in `data/` | Used by | Source |
|---|---|---|
| `natural_earth/ne_10m_admin_0_countries.*` | all maps | [Natural Earth](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/) 1:10m Admin 0 countries, v4.1.0 |
| `world_country_lon_lat.csv`, `eu_country_lon_lat*.csv` | gnp, cinema | Country centroids from Google's [DSPL countries.csv](https://developers.google.com/public-data/docs/canonical/countries_csv) |
| `worldbank_gnp.csv` | gnp | [World Bank](https://data.worldbank.org/indicator/ny.gnp.pcap.pp.cd), GNI per capita (PPP), retrieved 2019-10-20 |
| `unesco_movie_producing.csv`, `unesco_science_tech_innov.csv` | cinema | [UNESCO Institute for Statistics](http://uis.unesco.org/), retrieved 2019-10 |
| `TMDB_movie_dataset_v11.csv` | cinema, horror_jump_scares | [TMDB movies dataset](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies) on Kaggle |
| `numbeo_cost_of_living_by_cities_2026.csv` | cost_of_living | [Numbeo cost of living rankings](https://www.numbeo.com/cost-of-living/rankings.jsp), 2026 |
| `output/{amenity}_counts.json` | osm_amenities | Written by the notebook from the [Overpass API](https://overpass-api.de/) (OpenStreetMap) |
| `cache/horror/` | horror_jump_scares | Written by the notebook, see [its README](../projects/horror_jump_scares/README.md) |

City coordinates and populations used by the European city maps are in `mapy/config.py`.
