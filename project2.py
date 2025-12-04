import ee   
import pandas as pd
import arcpy
import geopandas

#ee.Authenticate()

def project2(project_name,csv_path, raster_path, shapefile_path):
    
    ee.Initialize(project=project_name)
    dem = ee.Image('USGS/3DEP/10m')

    table = pd.read_csv(csv_path)
    table.head()

    ra1 = arcpy.Raster(raster_path)
    print(ra1.spatialReference.factoryCode)

    gdf = geopandas.GeoDataFrame(table)

    gdf.set_geometry( geopandas.points_from_xy(gdf['X'], gdf['Y']), 
                     inplace=True, crs=f'EPSG:{ra1.spatialReference.factoryCode}')
    
    try:
        gdf.to_file(shapefile_path)
        
        arcpy.management.AddField(shapefile_path,'elevation',field_type='FLOAT')
    except Exception as e:
        print(e)  
        return  
    
    
    geom_list = []
    with arcpy.da.SearchCursor(shapefile_path,['SHAPE@XY'],spatial_reference=4326) as cursor:
        for row in cursor:
            X,Y = row[0]
            geom = ee.Geometry.Point([X,Y])
            geom_list.append(geom)
    geom_col = ee.FeatureCollection(geom_list)
    elev = dem.sampleRegions(geom_col).getInfo().get('features')

    i = 0
    with arcpy.da.UpdateCursor(shapefile_path,['elevation']) as cursor:
        for row in cursor:
            elevation = elev[i]['properties']['elevation']
            row[0] = elevation
            cursor.updateRow(row)
            i += 1
       
if __name__ == "__main__":     
    csv_path = r"C:\Users\bghosn2\Documents\geog4057\Project 2\boundary.csv"
    raster_path = r"C:\Users\bghosn2\Documents\geog4057\Project 2\flood_2class.tif"
    shapefile_path = r"C:\Users\bghosn2\Documents\geog4057\Project 2\boundary.shp"
    project_name = "ee-bghosn4"

    project2(project_name,csv_path,raster_path,shapefile_path)