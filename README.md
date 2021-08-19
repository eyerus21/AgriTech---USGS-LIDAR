# AgriTech---USGS-LIDAR


> At AgriTech, we are very interested in how water flows through a maize farm field. This knowledge will help us improve our research on new agricultural products being tested on farms.

---

## Table of contents

* [Description](#description)
* [Project Progress](#progress)
* [Installation requirements](#install)
* [How to Use](#use)
* [Skills and knowledge](#hint)
* [References](#refs)
* [License](#license)

# <a name='description'></a>
## Description
> **LiDAR** (light detection and ranging) is a popular remote sensing mechanism used for measuring the exact distance of an object on the earth's surface. Since the introduction of GPS technology, it has become a widely used method for calculating accurate geospatial measurements. These geospatial data are used for different analysis purposes.

> The purpose of this project is to build models of water flow and predict maize harvest if we better understand how water flows through a field, and which parts are likely to be flooded or too dry. 

---

## Data Source 
- https://registry.opendata.aws/usgs-lidar/

---

# <a name='progress'></a>

## Project Progress

* Main Tasks
  - [x] Enable Elevation Data Fetching
  - [x] Enable Data Loading from saved tif and las/laz files
  - [ ] Enable Terrian Visualization using retrieved or loaded LiDAR cloud points
  - [ ] Enable Cloud Point Standardizing/Sub-Sampling
  - [ ] Enable data augmentation to retrieved geopandas data-frame
  - [ ] Composing a QuickStart Guide Notebook

* Additional Tasks
  - [ ] Enable Diagrammatic way of comparing original terrain and subsampled terrain
  - [ ] Enable Soil-Data Fetching
  - [ ] Enable Climate-Data Fetching
  - [ ] Enable interaction with Sentinel public API
  - [ ] Enable users to download satellite imagery using Sentinels API

  ---

  # <a name='install'></a> 
  ## Installation requirements

  >Some of the python packages required to do the project are listed here and for more check the requiremnt.txt file:
  ```
pip install pdal
pip install geopandas
pip install rasterio
pip install laspy

```
  




Data Fetching and Loading

Terrain Visualization

Data Transformation 
 
---


Skills:
Working with satellite imagery as well as geographical data files

Exposure to building API that interacts with satellite imagery
Code packaging and modularity

Building data pipelines and orchestrations workflows


Knowledge:
Satellite and geographical Image processing 
Functional and Modular Coding
API access to Big Data
