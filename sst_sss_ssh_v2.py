#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 13:16:50 2025

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
    
    
    import os
import xarray as xr
import pandas as pd

# Directorio donde se encuentran los archivos
directorio = "/Volumes/LLACA/Python/PTM"
archivo_salida = os.path.join(directorio, "sst_sss_ssh.csv")

# Lista de archivos NetCDF a explorar
archivo_nc = "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_1740084783181.nc"
ruta = os.path.join(directorio, archivo_nc)

# Abrir el archivo NetCDF
ds = xr.open_dataset(ruta)

# Seleccionar variables de interés y renombrarlas
ds_selected = ds[["zos", "so", "thetao"]].rename({
    "zos": "ssh",
    "so": "sss",
    "thetao": "sst"
})

# Convertir a DataFrame
df = ds_selected.to_dataframe().reset_index()

# Reordenar columnas y ajustar formato de la fecha
df["time"] = pd.to_datetime(df["time"]).dt.strftime("%Y-%m-%d")
df = df[["time", "longitude", "latitude", "ssh", "sst", "sss"]]

# Guardar como CSV
df.to_csv(archivo_salida, index=False)

print(f"✅ Archivo CSV guardado en: {archivo_salida}")

    