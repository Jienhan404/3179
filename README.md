# Worth the flight? Student satisfaction at Australian universities

FIT3179 Data Visualisation 2. A single scrolling page, built with Vega-Lite, that tells Malaysian students and families what current students think of Australian universities.

## View it

Open `index.html` through a web server (the charts load their data with `fetch`, so opening the file directly will not work):

```
python3 -m http.server 8000
```

Then visit http://localhost:8000. On GitHub Pages the page is served from the repository root.

## What is where

| Path | Contents |
|---|---|
| `index.html` | The page and its text |
| `css/style.css` | Layout and typography |
| `js/main.js` | Loads each chart with vega-embed and applies the shared chart style |
| `specs/*.vl.json` | One Vega-Lite specification per chart |
| `data/` | The CSV and GeoJSON files the charts read (see `data/README.md`) |
| `scripts/extract_ses.py` | Script that produced the CSVs from the published survey tables |

## Charts

| # | Spec | Idiom |
|---|---|---|
| 1 | `malaysia_trend` | Annotated area chart |
| 2 | `nationalities` | Waffle chart with Malaysia highlighted |
| 3 | `map_flow` | **Map: flow map** (Kuala Lumpur to each state) |
| 4 | `trend_focus` | Annotated multi-line chart with direct labels |
| 5 | `map_choropleth` | **Map: choropleth** by state, with a measure selector |
| 6 | `map_universities` | **Map: proportional symbol map** of universities |
| 7 | `uni_strip` | Box plot with jittered dots and a university highlighter |
| 8 | `area_heatmap` | Heatmap, field of study by measure |
| 9 | `items_lollipop` | Ranked lollipop chart with a clickable legend |
| 10 | `drivers_scatter` | Small-multiple scatterplots with trend lines (3 + 2 grid) |
| 11 | `groups_dumbbell` | Dumbbell chart with a group selector |
| 12 | `leave_reasons` | Slope chart, 2023 to 2025 |
| 13 | `malaysia_reasons` | Dumbbell chart, Malaysia vs all international students |
| 14 | `living_heatmap` | Heatmap, home country by aspect of living |

The Australia maps use an Albers equal-area conic projection so state areas are comparable. The flow map uses Mercator so the straight lines keep a constant compass direction.

## Data sources

- QILT, *2025 Student Experience Survey: National Report Tables and International Report Tables*, Social Research Centre for the Australian Government Department of Education. https://www.qilt.edu.au/surveys/student-experience-survey-(ses)
- Australian Government Department of Education, *International Student Data* (year to date, December 2025). https://www.education.gov.au/international-education-data-and-research/international-student-data
- Natural Earth (public domain) for state and country boundaries. https://www.naturalearthdata.com/

## Acknowledgement

Claude (Anthropic) was used to help prepare the data files, write the Vega-Lite specifications and page code, and draft the text.
