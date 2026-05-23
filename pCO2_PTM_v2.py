#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 09:17:13 2025

@author: lucoronado
"""

import os
import xarray as xr

# Ruta del archivo
directorio = "/Volumes/LLACA/Python/PTM"
archivo = "cmems_mod_glo_bgc-co2_anfc_0.25deg_P1D-m_1740085571653.nc"
ruta = os.path.join(directorio, archivo)

# Abrir el archivo NetCDF
ds = xr.open_dataset(ruta)

# Información general del archivo
print("Información general del archivo:")
print(ds)

# Listar las variables disponibles
print("\nVariables disponibles:")
for var in ds.data_vars:
    print(f"- {var}: {ds[var].attrs.get('long_name', 'No disponible')} ({ds[var].attrs.get('units', 'Sin unidades')})")

# Dimensiones y coordenadas
print("\nDimensiones:")
print(ds.dims)

print("\nCoordenadas:")
print(ds.coords)

# Atributos globales
print("\nAtributos globales:")
for attr, value in ds.attrs.items():
    print(f"{attr}: {value}")

# Cerrar el archivo
ds.close()



##################################################################
##################################################################
##################################################################

import os
import xarray as xr
import matplotlib.pyplot as plt

# Ruta del archivo
directorio = "/Volumes/LLACA/Python/PTM"
archivo = "cmems_mod_glo_bgc-co2_anfc_0.25deg_P1D-m_1737671243364.nc"
ruta = os.path.join(directorio, archivo)

# Abrir el archivo NetCDF
ds = xr.open_dataset(ruta)

# Filtrar el rango de fechas deseado (1 al 30 de septiembre de 2024)
spco2 = ds["spco2"].sel(time=slice("2024-09-01", "2024-09-30"))

# Convertir pCO₂ de Pa a µatm
spco2_microatm = spco2 * 10

# Calcular el promedio, mínimo y máximo diario
spco2_mean = spco2_microatm.mean(dim=["latitude", "longitude"])
spco2_min = spco2_microatm.min(dim=["latitude", "longitude"])
spco2_max = spco2_microatm.max(dim=["latitude", "longitude"])

# Graficar la serie de tiempo
plt.figure(figsize=(10, 6))
plt.plot(spco2_mean["time"], spco2_mean, label="Promedio diario", color="black", linestyle="--", marker="o")
plt.plot(spco2_min["time"], spco2_min, label="Mínimo diario", color="red", linestyle="--", marker="x")
plt.plot(spco2_max["time"], spco2_max, label="Máximo diario", color="red", linestyle="--", marker="x")

# Configurar el gráfico
plt.title("Serie de tiempo de pCO₂ superficial en µatm (septiembre 2024)")
plt.xlabel("Fecha")
plt.ylabel("pCO₂ (µatm)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Hacer mapas de pCO₂ para el 22, 23 y 24 de septiembre de 2024
fechas = ["2024-09-22", "2024-09-23", "2024-09-24"]
for fecha in fechas:
    spco2_dia = spco2_microatm.sel(time=fecha)
    
    # Graficar el mapa
    plt.figure(figsize=(10, 6))
    spco2_dia.plot(cmap="coolwarm", cbar_kwargs={"label": "pCO₂ (µatm)"})
    plt.title(f"Mapa de pCO₂ superficial en µatm - {fecha}")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid()
    plt.tight_layout()
    plt.show()
    
    

##################################################################
##################################################################
##################################################################



    
    

##################################################################
##################################################################
##################################################################
# Convertir los datos a un DataFrame
import pandas as pd
import os  # También necesitas importar 'os' si lo estás usando para guardar el archivo


spco2_df = spco2_microatm.to_dataframe().reset_index()

# Reordenar columnas y ajustar formato de la fecha
spco2_df["time"] = pd.to_datetime(spco2_df["time"]).dt.strftime("%Y-%m-%d")
spco2_df = spco2_df[["time", "longitude", "latitude", "spco2"]]

# Renombrar columnas para mayor claridad
spco2_df = spco2_df.rename(columns={
    "time": "time",
    "longitude": "longitude",
    "latitude": "latitude",
    "spco2": "pco2_uatm"
})

# Guardar como CSV
archivo_csv = os.path.join(directorio, "pco2_septiembre_2024_v2.csv")
spco2_df.to_csv(archivo_csv, index=False)

print(f"Archivo CSV guardado en: {archivo_csv}")
