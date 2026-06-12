import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import numpy as np

from libpysal.weights import Queen
from esda.moran import Moran, Moran_Local


# =========================
# Page setup
# =========================
st.set_page_config(
    page_title="Generic Drug Analysis in Japan",
    layout="wide"
)

st.title("Generic Drug Analysis in Japan")


# =========================
# Data reading
# =========================
@st.cache_data
def load_data():

    df = pd.read_csv(
        "NDB_OpenData_Japan_Drug_Top100_15_23.csv"
    )

    return df


@st.cache_data
def load_map():

    gdf = gpd.read_file(
        "jp.json"
    )

    gdf["prefecture"] = gdf["name"]

    return gdf


df = load_data()
jp_map = load_map()


# =========================
# Sidebar
# =========================
st.sidebar.header("Filter")

# source
source_options = sorted(
    df["source"].dropna().unique()
)

selected_sources = st.sidebar.multiselect(
    "Data source",
    source_options,
    default=source_options
)

# dosage form
dosage_options = sorted(
    df["d_form"].dropna().unique()
)

selected_dosage = st.sidebar.multiselect(
    "Dosage form",
    dosage_options,
    default=dosage_options
)

# category
category_options = sorted(
    df["category"].dropna().unique()
)

selected_category = st.sidebar.multiselect(
    "Drug category",
    category_options,
    default=category_options
)

# area
area_options = sorted(
    df["area"].dropna().unique()
)

selected_area = st.sidebar.multiselect(
    "Region",
    area_options,
    default=area_options
)

# prefecture
pref_options = sorted(
    df["prefecture"].dropna().unique()
)

selected_pref = st.sidebar.multiselect(
    "Prefecture",
    pref_options,
    default=pref_options
)


# analysis mode
analysis_mode = st.sidebar.radio(
    "Analysis mode",
    [
        "Trend analysis",
        "Stratified analysis",
        "Spatial analysis",
        "Dataset explorer"
    ]
)


# chart type
chart_type = st.sidebar.radio(
    "Trend chart type",
    [
        "Line chart",
        "Bar chart"
    ],
    index=0
)


# =========================
# Data filtering
# =========================
filtered_df = df[
    (df["source"].isin(selected_sources))
    &
    (df["d_form"].isin(selected_dosage))
    &
    (df["category"].isin(selected_category))
    &
    (df["prefecture"].isin(selected_pref))
    &
    (df["area"].isin(selected_area))
]
# =========================
# Trend analysis
# =========================
def trend_analysis():

    # ==================================
    # Annual fluctuations
    # ==================================
    st.subheader("Annual fluctuations in cost ratios")

    summary = (
        filtered_df
        .groupby(["year", "generic"], as_index=False)["cost"]
        .sum()
    )

    summary["total_cost"] = (
        summary
        .groupby("year")["cost"]
        .transform("sum")
    )

    summary["cost_ratio"] = (
        summary["cost"] /
        summary["total_cost"]
    )

    summary["generic_label"] = summary["generic"].map({
        0: "Brand names",
        1: "Generics"
    })

    if chart_type == "Line chart":

        fig = px.line(
            summary,
            x="year",
            y="cost_ratio",
            color="generic_label",
            markers=True,
            labels={
                "year": "Fiscal year",
                "cost_ratio": "Cost ratio",
                "generic_label": "Drug category"
            }
        )

    else:

        fig = px.bar(
            summary,
            x="year",
            y="cost_ratio",
            color="generic_label",
            labels={
                "year": "Fiscal year",
                "cost_ratio": "Cost ratio",
                "generic_label": "Drug category"
            }
        )

    fig.update_layout(
        yaxis_tickformat=".1%",
        hovermode="x unified",
        barmode="stack"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ==================================
    # Annual cost summary
    # ==================================
    st.subheader("Annual cost summary")

    table = (
        summary
        .pivot_table(
            index="year",
            columns="generic_label",
            values="cost",
            aggfunc="sum"
        )
        .reset_index()
    )

    table["Total cost"] = (
        table
        .drop(columns=["year"])
        .sum(axis=1)
    )

    st.dataframe(
        table.style.format("{:,.0f}"),
        use_container_width=True
    )


    # ==================================
    # Regional trend
    # ==================================
    st.subheader(
        "Regional trend of generic cost ratio"
    )

    area_summary = (
        filtered_df
        .groupby(
            ["year", "area", "generic"],
            as_index=False
        )["cost"]
        .sum()
    )

    area_summary["total_cost"] = (
        area_summary
        .groupby(
            ["year", "area"]
        )["cost"]
        .transform("sum")
    )

    area_summary["cost_ratio"] = (
        area_summary["cost"]
        /
        area_summary["total_cost"]
    )

    area_generic = area_summary[
        area_summary["generic"] == 1
    ]

    fig_area = px.line(
        area_generic,
        x="year",
        y="cost_ratio",
        color="area",
        markers=True,
        labels={
            "year": "Fiscal year",
            "cost_ratio": "Generic cost ratio",
            "area": "Region"
        }
    )

    fig_area.update_layout(
        yaxis_tickformat=".1%",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_area,
        use_container_width=True
    )


    # ==================================
    # Regional annual summary
    # ==================================
    st.subheader(
        "Regional annual cost summary"
    )

    area_table = (
        area_summary
        .pivot_table(
            index=["area", "year"],
            columns="generic",
            values="cost",
            aggfunc="sum"
        )
        .reset_index()
    )

    area_table = area_table.rename(
        columns={
            0: "Brand names",
            1: "Generics"
        }
    )

    area_table["Total cost"] = (
        area_table[
            ["Brand names", "Generics"]
        ]
        .sum(axis=1)
    )

    area_table["Generic cost ratio"] = (
        area_table["Generics"]
        /
        area_table["Total cost"]
    )

    st.dataframe(
        area_table.style.format({
            "Brand names": "{:,.0f}",
            "Generics": "{:,.0f}",
            "Total cost": "{:,.0f}",
            "Generic cost ratio": "{:.2%}"
        }),
        use_container_width=True
    )
# =========================
# Stratified analysis
# =========================
def stratified_analysis():

    # ==================================
    # Data source trend
    # ==================================
    st.subheader(
        "Generic cost ratio by data source"
    )

    source_summary = (
        filtered_df
        .groupby(
            ["year", "source", "generic"],
            as_index=False
        )["cost"]
        .sum()
    )

    source_summary["total_cost"] = (
        source_summary
        .groupby(
            ["year", "source"]
        )["cost"]
        .transform("sum")
    )

    source_summary["cost_ratio"] = (
        source_summary["cost"]
        /
        source_summary["total_cost"]
    )

    source_generic = source_summary[
        source_summary["generic"] == 1
    ]

    fig_source = px.line(
        source_generic,
        x="year",
        y="cost_ratio",
        color="source",
        markers=True,
        labels={
            "year": "Fiscal year",
            "cost_ratio": "Generic cost ratio",
            "source": "Data source"
        }
    )

    fig_source.update_layout(
        yaxis_tickformat=".1%",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_source,
        use_container_width=True
    )


    # ==================================
    # Data source summary
    # ==================================
    st.subheader(
        "Data source annual summary"
    )

    source_table = (
        source_generic
        .pivot_table(
            index="year",
            columns="source",
            values="cost_ratio"
        )
    )

    st.dataframe(
        source_table.style.format("{:.2%}"),
        use_container_width=True
    )


    # ==================================
    # Dosage form trend
    # ==================================
    st.subheader(
        "Generic cost ratio by dosage form"
    )

    dose_summary = (
        filtered_df
        .groupby(
            ["year", "d_form", "generic"],
            as_index=False
        )["cost"]
        .sum()
    )

    dose_summary["total_cost"] = (
        dose_summary
        .groupby(
            ["year", "d_form"]
        )["cost"]
        .transform("sum")
    )

    dose_summary["cost_ratio"] = (
        dose_summary["cost"]
        /
        dose_summary["total_cost"]
    )

    dose_generic = dose_summary[
        dose_summary["generic"] == 1
    ]

    fig_dose = px.line(
        dose_generic,
        x="year",
        y="cost_ratio",
        color="d_form",
        markers=True,
        labels={
            "year": "Fiscal year",
            "cost_ratio": "Generic cost ratio",
            "d_form": "Dosage form"
        }
    )

    fig_dose.update_layout(
        yaxis_tickformat=".1%",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_dose,
        use_container_width=True
    )


    # ==================================
    # Dosage form summary
    # ==================================
    st.subheader(
        "Dosage form annual summary"
    )

    dose_table = (
        dose_generic
        .pivot_table(
            index="year",
            columns="d_form",
            values="cost_ratio"
        )
    )

    st.dataframe(
        dose_table.style.format("{:.2%}"),
        use_container_width=True
    )
# =========================
# Spatial analysis
# =========================
def spatial_analysis():

    # ==================================
    # Select fiscal year
    # ==================================
    selected_year = st.selectbox(
        "Fiscal year",
        sorted(filtered_df["year"].unique()),
        index=len(sorted(filtered_df["year"].unique()))-1
    )

    year_df = filtered_df[
        filtered_df["year"] == selected_year
    ]

    # ==================================
    # Prefecture summary
    # ==================================
    pref_summary = (
        year_df
        .groupby(["prefecture", "generic"], as_index=False)["cost"]
        .sum()
    )

    pref_summary["total_cost"] = (
        pref_summary
        .groupby("prefecture")["cost"]
        .transform("sum")
    )

    pref_summary["cost_ratio"] = (
        pref_summary["cost"] /
        pref_summary["total_cost"]
    )

    pref_table = (
        pref_summary
        .pivot_table(
            index="prefecture",
            columns="generic",
            values="cost",
            aggfunc="sum"
        )
        .reset_index()
    )

    pref_table = pref_table.rename(
        columns={
            0: "Brand names",
            1: "Generics"
        }
    )

    pref_table["Total cost"] = (
        pref_table["Brand names"] +
        pref_table["Generics"]
    )

    pref_table["Generic cost ratio"] = (
        pref_table["Generics"] /
        pref_table["Total cost"]
    )

    # ==================================
    # Generic cost ratio of prefectures
    # ==================================
    st.subheader(
        "Generic cost ratio of prefectures"
    )

    fig_pref = px.bar(
        pref_table.sort_values(
            "Generic cost ratio",
            ascending=False
        ),
        x="prefecture",
        y="Generic cost ratio",
        labels={
            "prefecture": "Prefecture",
            "Generic cost ratio": "Generic cost ratio"
        }
    )

    fig_pref.update_layout(
        yaxis_tickformat=".1%",
        xaxis_tickangle=-90
    )

    st.plotly_chart(
        fig_pref,
        use_container_width=True
    )

    st.dataframe(
        pref_table.style.format({
            "Brand names":"{:,.0f}",
            "Generics":"{:,.0f}",
            "Total cost":"{:,.0f}",
            "Generic cost ratio":"{:.2%}"
        }),
        use_container_width=True
    )

    # ==================================
    # Descriptive statistics
    # ==================================
    st.subheader(
        "Descriptive statistics"
    )

    st.dataframe(
        pref_table[
            ["Generic cost ratio"]
        ].describe().style.format("{:.2%}")
    )

    # ==================================
    # Regional distribution map
    # ==================================
    st.subheader(
        "Regional distribution map"
    )

    map_df = jp_map.merge(
        pref_table,
        on="prefecture"
    )

    fig_map = px.choropleth(
        map_df,
        geojson=map_df.geometry,
        locations=map_df.index,
        color="Generic cost ratio",
        hover_name="prefecture",
        projection="mercator"
    )

    fig_map.update_geos(
        fitbounds="locations",
        visible=False
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True
    )

    # ==================================
    # Global Moran's I
    # ==================================
    st.subheader(
        "Global Moran's I"
    )

    w = Queen.from_dataframe(map_df)
    w.transform = "r"

    y = map_df["Generic cost ratio"].values

    moran = Moran(
        y,
        w
    )

    moran_table = pd.DataFrame({
        "Moran's I":[moran.I],
        "P value":[moran.p_sim]
    })

    st.dataframe(
        moran_table.style.format({
            "Moran's I":"{:.3f}",
            "P value":"{:.4f}"
        }),
        use_container_width=True
    )

    # ==================================
    # Moran's I trend
    # ==================================
    st.subheader(
        "Temporal trend of Moran's I"
    )

    moran_list = []

    for year in sorted(filtered_df["year"].unique()):

        temp = filtered_df[
            filtered_df["year"] == year
        ]

        temp_summary = (
            temp
            .groupby(["prefecture", "generic"], as_index=False)["cost"]
            .sum()
        )

        temp_summary["total_cost"] = (
            temp_summary
            .groupby("prefecture")["cost"]
            .transform("sum")
        )

        temp_summary["cost_ratio"] = (
            temp_summary["cost"] /
            temp_summary["total_cost"]
        )

        temp_table = (
            temp_summary
            .pivot_table(
                index="prefecture",
                columns="generic",
                values="cost"
            )
            .reset_index()
        )

        temp_table["Generic cost ratio"] = (
            temp_table[1] /
            (temp_table[0] + temp_table[1])
        )

        temp_map = jp_map.merge(
            temp_table,
            on="prefecture"
        )

        w_temp = Queen.from_dataframe(temp_map)
        w_temp.transform = "r"

        moran_temp = Moran(
            temp_map["Generic cost ratio"],
            w_temp
        )

        moran_list.append(
            {
                "year": year,
                "Moran's I": moran_temp.I
            }
        )

    moran_df = pd.DataFrame(
        moran_list
    )

    fig_moran = px.line(
        moran_df,
        x="year",
        y="Moran's I",
        markers=True
    )

    st.plotly_chart(
        fig_moran,
        use_container_width=True
    )


    # ==================================
    # LISA cluster map
    # ==================================
    st.subheader(
        "LISA cluster map"
    )

    # Local Moran
    lisa = Moran_Local(
        y,
        w
    )

    # quadrant and p-value
    map_df["quadrant"] = lisa.q
    map_df["p_value"] = lisa.p_sim

    # default
    map_df["Cluster"] = "Not significant"

    # significance
    sig = map_df["p_value"] < 0.05

    map_df.loc[
        sig & (map_df["quadrant"] == 1),
        "Cluster"
    ] = "High-High"

    map_df.loc[
        sig & (map_df["quadrant"] == 2),
        "Cluster"
    ] = "Low-High"

    map_df.loc[
        sig & (map_df["quadrant"] == 3),
        "Cluster"
    ] = "Low-Low"

    map_df.loc[
        sig & (map_df["quadrant"] == 4),
        "Cluster"
    ] = "High-Low"

    # Exclude islands (same as GeoDa)
    island_prefectures = [
        "Hokkaidō",
        "Okinawa"
    ]

    map_df.loc[
        map_df["prefecture"].isin(
            island_prefectures
        ),
        "Cluster"
    ] = "Island (excluded)"

    # GeoDa color scheme
    color_map = {
        "High-High": "#e41a1c",
        "Low-Low": "#377eb8",
        "Low-High": "#a6cee3",
        "High-Low": "#f781bf",
        "Not significant": "#d9d9d9",
        "Island (excluded)": "#f5f5f5"
    }

    fig_lisa = px.choropleth(
        map_df,
        geojson=map_df.geometry,
        locations=map_df.index,
        color="Cluster",
        hover_name="prefecture",
        projection="mercator",
        color_discrete_map=color_map,
        category_orders={
            "Cluster": [
                "High-High",
                "Low-Low",
                "Low-High",
                "High-Low",
                "Not significant",
                "Island (excluded)"
            ]
        }
    )

    fig_lisa.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig_lisa.update_layout(
        legend_title_text="LISA cluster"
    )

    st.plotly_chart(
        fig_lisa,
        use_container_width=True
    )


    # ==================================
    # Cluster summary
    # ==================================
    st.subheader(
        "Cluster summary"
    )

    cluster_summary = (
        map_df["Cluster"]
        .value_counts()
        .reset_index()
    )

    cluster_summary.columns = [
        "Cluster",
        "Number of prefectures"
    ]

    st.dataframe(
        cluster_summary,
        use_container_width=True
    )


    # ==================================
    # Detailed LISA results
    # ==================================
    st.subheader(
        "Detailed LISA results"
    )

    lisa_table = map_df[
        [
            "prefecture",
            "Generic cost ratio",
            "Cluster",
            "p_value"
        ]
    ].sort_values(
        "Generic cost ratio",
        ascending=False
    )

    st.dataframe(
        lisa_table.style.format({
            "Generic cost ratio": "{:.2%}",
            "p_value": "{:.4f}"
        }),
        use_container_width=True
    )
# =========================
# Database information
# =========================
def dataset_explorer():

    st.subheader(
        "Database overview"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Records",
            len(filtered_df)
        )

    with col2:
        st.metric(
            "Fiscal years",
            filtered_df["year"].nunique()
        )

    with col3:
        st.metric(
            "Prefectures",
            filtered_df["prefecture"].nunique()
        )

    with col4:
        st.metric(
            "Drug categories",
            filtered_df["category"].nunique()
        )

    # ==================================
    # Variable information
    # ==================================
    st.subheader(
        "Variable information"
    )

    variable_table = pd.DataFrame({
        "Variable": [
            "year",
            "prefecture",
            "area",
            "category",
            "source",
            "d_form",
            "generic",
            "cost"
        ],

        "Description": [
            "Fiscal year",
            "Prefecture",
            "Region",
            "Drug category",
            "Data source",
            "Dosage form",
            "Brand names or generics",
            "Drug expenditure"
        ]
    })

    st.dataframe(
        variable_table,
        use_container_width=True
    )

    # ==================================
    # Random sample
    # ==================================
    st.subheader(
        "Random sample (100 records)"
    )

    sample_size = min(
        100,
        len(filtered_df)
    )

    sample_df = filtered_df.sample(
        sample_size,
        random_state=123
    )

    st.dataframe(
        sample_df,
        use_container_width=True
    )


# =========================
# Main
# =========================
if analysis_mode == "Trend analysis":

    trend_analysis()

elif analysis_mode == "Stratified analysis":

    stratified_analysis()

elif analysis_mode == "Spatial analysis":

    spatial_analysis()

else:

    dataset_explorer()