from osgeo import gdal, osr
import geopandas as gpd
import gdal
import os
import matplotlib.pyplot as plt
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import rasterio as rio
import numpy as np
import imageio
from rasterio.plot import show
import pandas as pd
import pathlib
import mapclassify as mc
import laspy
from rasterio import mask
import folium

class Fetch():
    '''
    A Data fetcher class which fetches data and vicualize it
    
    Parameters
    ----
    Polygon
        a series of x and y coordinate pairs that enclose an
        area—as one of its properties (or fields) in the row in the database
        
    epsg
        a database of coordinate system information plus 
        some very good related documents on map projections and datums
    
    '''
    def __init__(self) -> None:
        
        minx, miny, maxx, maxy = self.get_polygon_points(polygon, epsg)
        self.epsg = epsg
        self.filename= '../Data/iowa.tif'
        
    #open and load a raster file    
    def get_getitem__(self):
        ds= gdal.Open(self.filename)
        return ds
    
    #raster info
    def raster info(self):
        Ds=get_getitem__()
        Width= Ds.RasterXSize 
        Height= Ds.RasterYSize 
        return Width,Height     
    
    # getting an from raster data
    def get_pipeline_arrays(self):
         Ds=get_getitem__()
         rastArr= Ds.GetRasterBand(1).ReadAsArray()
         return rastArr
     
     # get shp from tif
    def get_shp_from_tif(tif_path:str, shp_file_path:str) -> None:
        raster = rio.open(tif_path)
        df= gpd.GeoDataFrame([polygon], columns=["geometry"])
        df.set_crs(epsg=4326, inplace=True)
    # save to file
        df.to_file(shp_file_path)
        print('Saved..')
    
      
    def get_polygon_points():
        
        
        try:
            grid = gpd.GeoDataFrame([polygon], columns=["geometry"])
            grid.set_crs(epsg=epsg, inplace=True)

            grid['geometry'] = grid.geometry.to_crs(epsg=3857)

            minx, miny, maxx, maxy = grid.geometry[0].bounds
            # bounds: ([minx, maxx], [miny, maxy])
            self.extraction_bounds = f"({[minx, maxx]},{[miny,maxy]})"

            # Cropping Bounds
            self.polygon_cropping = self.get_crop_polygon(grid.geometry[0])

            grid['geometry'] = grid.geometry.to_crs(epsg=epsg)
            self.geo_df = grid

            logger.info(
                'Successfully Extracted Polygon Edges and Polygon Cropping Bounds')

            return minx, miny, maxx, maxy
        
        except Exception as e:
            logger.exception(
                'Failed to Extract Polygon Edges and Polygon Cropping Bounds')

    def get_crop_polygon(self, polygon: Polygon) -> str:
        """Calculates Polygons Cropping string used when building Pdal's crop pipeline.

        Parameters
        ----------
        polygon: Polygon
            Polygon object describing the boundary of the location required

        Returns
        -------
        str
            Cropping string used by Pdal's crop pipeline
        """
        polygon_cords = 'POLYGON(('
        for i in list(polygon.exterior.coords):
            polygon_cords += f'{i[0]} {i[1]},'

        polygon_cords = polygon_cords[:-1] + '))'

        return polygon_cords





if __name__ == "__main__":
    MINX, MINY, MAXX, MAXY = [-93.756155, 41.918015, -93.747334, 41.921429]
    polygon = Polygon(((MINX, MINY), (MINX, MAXY),
                       (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))

    df = DataFetcher(polygon=polygon, epsg="4326")

   

