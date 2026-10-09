# Data files

All satisfaction figures are "% positive rating": the share of students who rated that area positively.
UG = undergraduate. Year = 2025 unless stated.

| File | What it holds | Source sheet |
|---|---|---|
| uni_ug_2025.csv | 43 universities × 6 focus areas, UG population surveyed, % international, overall rating split domestic/international, intl living experience, state + main-campus lat/lon | SES National: FOCUS_UG_UNI_1Y_INST_CI, CHARINT_UG_UNI_1Y_INST, FOCUS_UG_UNI_2Y_INST_CI_E942; SES International: INTSAT_UG_UNI_1Y_INST_CI |
| state_ug_2025.csv | State averages of the 6 focus areas (weighted by each university's UG population) | Derived from uni_ug_2025.csv |
| area_ug_2025.csv | 21 study areas × 6 focus areas + sense of belonging (universities only) | FOCUS_UG_UNI_1Y_AREA, BELONG_UG_ALL_17-YY_AREA |
| trend_ug.csv | National trend 2017–2025, 6 focus areas | FOCUS_UG_ALL_17-YY_YEAR |
| groups_ug_2025.csv | Focus areas by student group (stage, study mode, age, gender, international…) | FOCUS_UG_UNI_1Y_SG |
| items_ug_2025.csv | 37 individual survey questions behind the focus areas | DEVEL/ENGAG/TEACH/SUPP/RESR_UG_ALL_17-YY_STAGE |
| leave_reasons_ug.csv | Reasons students considered leaving, 2023–2025 | CONSID_UG_ALL_17-YY_CH |
| domestic_vs_intl_ug_2025.csv | Domestic vs international, 6 focus areas | FOCUS_UG_ALL_17-YY_E942 |
| intl_reasons_by_country_ug.csv | Why international students chose Australia, by home country | INTAUS_UG_ALL_1Y_COUNTRY_CI |
| intl_living_by_country_ug.csv | International living experience by home country | INTSAT_UG_ALL_1Y_COUNTRY_CI |
| malaysia_he_by_state_2025.csv | Malaysian higher-education students by state (Dec YTD 2025) | Dept of Education international student pivot |
| malaysia_he_trend.csv | Malaysian higher-education students, 2005–2025 | same |
| top10_nationalities_by_state_2025.csv | Top 10 nationalities × state | same |

Notes
- Peer Engagement and Student Support questions changed in 2023, so earlier years aren't directly comparable for those two areas.
- Lat/lon is each university's main campus, entered by hand. Check it before publishing.
- Adelaide and UniSA merged into Adelaide University in January 2026. The 2025 data still lists them separately.
- Very small institutions (e.g. Australian University of Theology, University of Divinity) have few respondents, so their scores are less reliable.

Sources
- QILT, 2025 Student Experience Survey National & International Report Tables, Social Research Centre for the Australian Government Department of Education. https://www.qilt.edu.au/surveys/student-experience-survey-(ses)
- Australian Government Department of Education, International Student Data (YTD December 2025). https://www.education.gov.au/international-education-data-and-research/international-student-data

Map and helper files
- australia_states.geojson: Australian state and territory boundaries (Natural Earth 1:50m, coordinates rounded to 2 decimals).
- region_countries.geojson: country outlines for South-East Asia and Oceania (Natural Earth 1:110m).
- state_capitals.csv: latitude and longitude of each state capital, used to draw the flow map.
