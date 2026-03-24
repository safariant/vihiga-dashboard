import streamlit as st
import ee
import geemap.foliumap as geemap
import pandas as pd

# -----------------------------

# EARTH ENGINE INIT

# -----------------------------

ee.Initialize()

st.title("Vihiga Landslide Risk Dashboard")

# -----------------------------

# LOAD DATA

# -----------------------------

Vihiga = ee.FeatureCollection("projects/ee-evanomondi/assets/Vihiga")
AOI = Vihiga.geometry()

# DEM → Slope

dem = ee.Image("USGS/SRTMGL1_003").clip(AOI)
slope = ee.Terrain.slope(dem)

# NDVI

s2 = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(AOI)
    .filterDate('2026-01-01', '2026-03-20')
    .median()
)

ndvi = s2.normalizedDifference(['B8', 'B4'])

# Simple risk model

risk = slope.divide(60).add(ndvi.multiply(-1).add(1)).divide(2)

# -----------------------------

# MAP

# -----------------------------

m = geemap.Map(center=[0.06, 34.72], zoom=11)
m.addLayer(risk, {'min':0, 'max':1, 'palette':['green','yellow','red']}, 'Risk')

m.to_streamlit(height=500)

st.success("App running successfully")
