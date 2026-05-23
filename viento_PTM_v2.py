#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 14:08:00 2025

@author: lucoronado
"""

import os
import xarray as xr

# Ruta del archivo
directorio = "/Volumes/LLACA/Python/PTM"
archivo = "viento.nc"
ruta = os.path.join(directorio, archivo)

# Abrir el archivo NetCDF
ds = xr.open_dataset(ruta)

# Mostrar información general del dataset
print("=== Información General ===")
print(ds)

# Mostrar las variables disponibles
print("\n=== Variables Disponibles ===")
print(ds.data_vars)

# Mostrar las dimensiones
print("\n=== Dimensiones ===")
print(ds.dims)

# Mostrar las coordenadas
print("\n=== Coordenadas ===")
print(ds.coords)

# Mostrar atributos globales
print("\n=== Atributos Globales ===")
print(ds.attrs)

# Opcional: inspeccionar una variable en específico (puedes cambiar 'viento' por el nombre real)
if 'viento' in ds.data_vars:
    print("\n=== Detalles de la Variable 'viento' ===")
    print(ds['viento'])
else:
    print("\nNo se encontró una variable llamada 'viento'.")


##############################################################
##############################################################
##############################################################
import os
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Ruta del archivo
directorio = "/Volumes/LLACA/Python/PTM"
archivo = "viento.nc"
ruta = os.path.join(directorio, archivo)

# Abrir el archivo NetCDF
ds = xr.open_dataset(ruta)

# Seleccionar las variables de viento (u10 y v10)
u10 = ds["u10"]
v10 = ds["v10"]

# Calcular la magnitud y dirección del viento
magnitude = np.sqrt(u10**2 + v10**2)
direction = np.arctan2(v10, u10)

# Promedio espacial (todas las latitudes y longitudes) para la magnitud
time_avg_magnitude = magnitude.mean(dim=["latitude", "longitude"])

# Fechas
dates = pd.to_datetime(magnitude["valid_time"].values)

# --- 2. Gráfica de tiempo vs. magnitud promedio ---
plt.figure(figsize=(12, 6))
plt.plot(dates, time_avg_magnitude, label="Magnitud del viento (promedio)", color="blue")
plt.title("Evolución temporal de la magnitud del viento - Septiembre 2024")
plt.xlabel("Fecha")
plt.ylabel("Magnitud del viento (m/s)")
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

# --- 3. Mapas con vectores del viento ---
# Seleccionar rango de fechas para graficar
selected_dates = pd.date_range("2024-09-22", "2024-09-25")

# Crear los mapas con vectores del viento
for date in selected_dates:
    # Seleccionar datos para el día actual
    u10_day = u10.sel(valid_time=date)
    v10_day = v10.sel(valid_time=date)
    magnitude_day = magnitude.sel(valid_time=date)

    # Crear el mapa
    plt.figure(figsize=(10, 6))
    plt.quiver(u10_day["longitude"], u10_day["latitude"], u10_day, v10_day, magnitude_day, cmap="coolwarm", scale=50)
    plt.title(f"Vectores del viento - {date.strftime('%Y-%m-%d')}")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.colorbar(label="Magnitud del viento (m/s)")
    plt.grid()
    plt.tight_layout()
    plt.show()


##############################################################
##############################################################
##############################################################
import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap  # Importar correctamente colormap
from windrose import WindroseAxes

# Ruta del archivo
directorio = "/Volumes/LLACA/Python/PTM"
archivo = "viento.nc"
ruta = os.path.join(directorio, archivo)

# Cargar el archivo NetCDF
ds = xr.open_dataset(ruta)

# Variables de viento
u10 = ds["u10"]
v10 = ds["v10"]

# Calcular magnitud y dirección del viento
wind_speed = np.sqrt(u10**2 + v10**2)  # Magnitud
wind_direction = np.arctan2(v10, u10) * (180 / np.pi)  # Dirección en grados
wind_direction = (wind_direction + 360) % 360  # Convertir dirección a [0, 360]

# Seleccionar datos para septiembre 2024
wind_speed_sept = wind_speed.sel(valid_time=slice("2024-09-01", "2024-09-30"))
wind_direction_sept = wind_direction.sel(valid_time=slice("2024-09-01", "2024-09-30"))

# Convertir los datos en arrays planos
wind_speed_flat = wind_speed_sept.values.flatten()
wind_direction_flat = wind_direction_sept.values.flatten()

# Filtrar valores NaN
valid_indices = ~np.isnan(wind_speed_flat) & ~np.isnan(wind_direction_flat)
wind_speed_flat = wind_speed_flat[valid_indices]
wind_direction_flat = wind_direction_flat[valid_indices]

# Crear la rosa de los vientos
fig = plt.figure(figsize=(10, 8))
ax = WindroseAxes.from_ax()
cmap = get_cmap("cool")  # Usar el colormap como objeto Colormap
ax.bar(wind_direction_flat, wind_speed_flat, bins=np.arange(0, 20, 2), normed=True, cmap=cmap)
ax.set_title("Rosa de los Vientos - Septiembre 2024")
ax.set_legend(title="Velocidad del viento (m/s)", loc="lower right", bbox_to_anchor=(1.2, 0))
plt.tight_layout()
plt.show()


##############################################################
##############################################################
##############################################################







