// Shared look for every chart. Each chart's own definition lives in specs/<id>.vl.json.
const config = {
  background: "transparent",
  font: "Inter, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
  view: { stroke: null },
  axis: {
    labelColor: "#52514e",
    labelFontSize: 11.5,
    titleColor: "#52514e",
    titleFontSize: 12,
    titleFontWeight: "normal",
    titlePadding: 10,
    gridColor: "#e6e4df",
    domainColor: "#c9c7c0",
    tickColor: "#c9c7c0"
  },
  legend: {
    labelColor: "#52514e",
    labelFontSize: 11.5,
    titleColor: "#52514e",
    titleFontSize: 11.5,
    titleFontWeight: 600
  },
  header: { labelColor: "#0b0b0b" }
};

const charts = [
  "malaysia_trend",
  "nationalities",
  "map_flow",
  "trend_focus",
  "map_choropleth",
  "map_universities",
  "uni_strip",
  "area_heatmap",
  "items_lollipop",
  "drivers_scatter",
  "groups_dumbbell",
  "leave_reasons",
  "malaysia_reasons",
  "living_heatmap"
];

charts.forEach((id) => {
  vegaEmbed("#" + id, "specs/" + id + ".vl.json", { actions: false, renderer: "svg", config })
    .catch((error) => console.error(id, error));
});
