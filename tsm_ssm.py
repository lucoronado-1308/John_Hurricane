#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 11:55:42 2025

@author: lucoronado
"""
import os
import xarray as xr

# Directorio donde se encuentran los archivos
directorio = "/Volumes/LLACA/Python/PTM"

# Lista de archivos NetCDF a explorar
archivos_nc = [
    "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_1740084783181.nc"
]

# Explorar cada archivo
for archivo in archivos_nc:
    ruta = os.path.join(directorio, archivo)
    print(f"\nExplorando el archivo: {archivo}")
    
    # Abrir el archivo NetCDF
    ds = xr.open_dataset(ruta)
    
    # Información general del archivo
    print("\nInformación general del archivo:")
    print(ds)
    
    # Variables disponibles
    print("\nVariables disponibles:")
    for var in ds.data_vars:
        print(f"- {var}: {ds[var].attrs.get('long_name', 'No disponible')} ({ds[var].attrs.get('units', 'Sin unidades')})")
    
    # Dimensiones y coordenadas
    print("\nDimensiones y coordenadas:")
    print(ds.dims)
    print(ds.coords)
    
    # Cerrar el archivo
    ds.close()
    
    
    ##############################################################
    ##############################################################
    ##############################################################
    
    # Ruta base
ruta_base = "/Volumes/LLACA/Python/PTM"

# Cargar cada archivo
archivo_sst = os.path.join(ruta_base, "cmems_mod_glo_phy_anfc_0.083deg-sst-anomaly_P1D-m_1737663955781.nc")
archivo_uo_vo = os.path.join(ruta_base, "cmems_mod_glo_phy-cur_anfc_0.083deg_PT6H-i_1737663903304.nc")
archivo_so = os.path.join(ruta_base, "cmems_mod_glo_phy-so_anfc_0.083deg_PT6H-i_1737663765616.nc")
archivo_thetao = os.path.join(ruta_base, "cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1737663696994.nc")

# Cargar los DataSets
ds_sst = xr.open_dataset(archivo_sst)
ds_uo_vo = xr.open_dataset(archivo_uo_vo)
ds_so = xr.open_dataset(archivo_so)
ds_thetao = xr.open_dataset(archivo_thetao)

# Combinar en un solo DataSet
ds_combined = xr.merge([ds_sst, ds_uo_vo, ds_so, ds_thetao])

# Mostrar información combinada
print(ds_combined)


import matplotlib.pyplot as plt

# Graficar cada variable
variables = ['sea_surface_temperature_anomaly', 'uo', 'vo', 'so', 'thetao']
for var in variables:
    if var in ds_combined:
        ds_combined[var].isel(time=0).plot(cmap="coolwarm", figsize=(8, 6))
        plt.title(f"Mapa de {var}")
        plt.show()

    
    ##############################################################
    ##############################################################
    ##############################################################
    
    
import os
import xarray as xr
import matplotlib.pyplot as plt

# Ruta base
ruta_base = "/Volumes/LLACA/Python/PTM"

# Cargar cada archivo
archivo_sst = os.path.join(ruta_base, "cmems_mod_glo_phy_anfc_0.083deg-sst-anomaly_P1D-m_1737663955781.nc")
archivo_uo_vo = os.path.join(ruta_base, "cmems_mod_glo_phy-cur_anfc_0.083deg_PT6H-i_1737663903304.nc")
archivo_so = os.path.join(ruta_base, "cmems_mod_glo_phy-so_anfc_0.083deg_PT6H-i_1737663765616.nc")
archivo_thetao = os.path.join(ruta_base, "cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1737663696994.nc")

# Cargar los DataSets
ds_sst = xr.open_dataset(archivo_sst)  # Anomalía de temperatura
ds_uo_vo = xr.open_dataset(archivo_uo_vo)  # Corrientes (uo, vo)
ds_so = xr.open_dataset(archivo_so)  # Salinidad
ds_thetao = xr.open_dataset(archivo_thetao)  # Temperatura

# Promedios y variaciones diarias
variables = {
    "sea_surface_temperature_anomaly": ds_sst["sea_surface_temperature_anomaly"],
    "salinity": ds_so["so"],
    "temperature": ds_thetao["thetao"]
}

# Crear las series de tiempo
for var_name, data_array in variables.items():
    # Calcular el promedio, mínimo y máximo por día
    mean_daily = data_array.mean(dim=["latitude", "longitude"])  # Promedio diario
    min_daily = data_array.min(dim=["latitude", "longitude"])  # Mínimo diario
    max_daily = data_array.max(dim=["latitude", "longitude"])  # Máximo diario

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.plot(mean_daily["time"], mean_daily, label="Promedio diario", color="black", linestyle="--")
    plt.plot(mean_daily["time"], min_daily, label="Mínimo diario", color="red", linestyle="--")
    plt.plot(mean_daily["time"], max_daily, label="Máximo diario", color="red", linestyle="--")
    
    # Configurar gráfico
    plt.title(f"Serie de tiempo: {var_name}")
    plt.xlabel("Tiempo")
    plt.ylabel(f"{data_array.attrs.get('long_name', var_name)} ({data_array.attrs.get('units', '-')})")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

    
    ##############################################################
    ##############################################################
    ##############################################################
   
import os
import xarray as xr
import pandas as pd

# Ruta base
ruta_base = "/Volumes/LLACA/Python/PTM"

# Cargar los archivos NetCDF
archivo_sst = os.path.join(ruta_base, "cmems_mod_glo_phy_anfc_0.083deg-sst-anomaly_P1D-m_1737663955781.nc")
archivo_uo_vo = os.path.join(ruta_base, "cmems_mod_glo_phy-cur_anfc_0.083deg_PT6H-i_1737663903304.nc")
archivo_so = os.path.join(ruta_base, "cmems_mod_glo_phy-so_anfc_0.083deg_PT6H-i_1737663765616.nc")
archivo_thetao = os.path.join(ruta_base, "cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1737663696994.nc")

# Cargar los DataSets
ds_sst = xr.open_dataset(archivo_sst)  # Anomalía de TSM
ds_uo_vo = xr.open_dataset(archivo_uo_vo)  # Corrientes (uo, vo)
ds_so = xr.open_dataset(archivo_so)  # Salinidad
ds_thetao = xr.open_dataset(archivo_thetao)  # Temperatura

# Seleccionar la región común (asegúrate de que todos los archivos tienen las mismas dimensiones)
lat_min, lat_max = 10, 22
lon_min, lon_max = -110, -90

# Recortar las variables y asegurarse de que las dimensiones coincidan
sst_anomaly = ds_sst["sea_surface_temperature_anomaly"].sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))
uo = ds_uo_vo["uo"].sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))
vo = ds_uo_vo["vo"].sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))
salinity = ds_so["so"].sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))
temperature = ds_thetao["thetao"].sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))

# Convertir las variables en un DataFrame
df = xr.merge([temperature, sst_anomaly, salinity, uo, vo]).to_dataframe().reset_index()

# Renombrar columnas para claridad
df = df.rename(columns={
    "time": "time",
    "longitude": "longitude",
    "latitude": "latitude",
    "sea_surface_temperature_anomaly": "sst_anomaly",
    "thetao": "sst",
    "so": "salinity",
    "uo": "uo",
    "vo": "vo"
})

# Reordenar las columnas
df = df[["time", "longitude", "latitude", "sst", "sst_anomaly", "salinity", "uo", "vo"]]

# Guardar como CSV
archivo_salida = os.path.join(ruta_base, "datos_recortados.csv")
df.to_csv(archivo_salida, index=False)

print(f"Archivo CSV guardado en: {archivo_salida}")


   