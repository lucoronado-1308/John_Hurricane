#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 10:24:15 2025

@author: lucoronado
"""

import os
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd

# Ruta base
ruta_base = "/Volumes/LLACA/Python/PTM"

# Cargar cada archivo
archivo_sst = os.path.join(ruta_base, "cmems_mod_glo_phy_anfc_0.083deg-sst-anomaly_P1D-m_1737663955781.nc")
archivo_so = os.path.join(ruta_base, "cmems_mod_glo_phy-so_anfc_0.083deg_PT6H-i_1737663765616.nc")
archivo_thetao = os.path.join(ruta_base, "cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1737663696994.nc")

# Cargar los DataSets
ds_sst = xr.open_dataset(archivo_sst)  # Anomalía de temperatura
ds_so = xr.open_dataset(archivo_so)  # Salinidad
ds_thetao = xr.open_dataset(archivo_thetao)  # Temperatura

# Seleccionar variables
sst_anomaly = ds_sst["sea_surface_temperature_anomaly"]
salinity = ds_so["so"]
temperature = ds_thetao["thetao"]

# Extraer todas las fechas de septiembre
septiembre_filtro = slice("2024-09-01", "2024-09-30")
sst_septiembre = sst_anomaly.sel(time=septiembre_filtro)
salinity_septiembre = salinity.sel(time=septiembre_filtro)
temperature_septiembre = temperature.sel(time=septiembre_filtro)

# Extraer fechas del 22 al 25 de septiembre
septiembre_especifico = slice("2024-09-22", "2024-09-25")
sst_sept22_25 = sst_anomaly.sel(time=septiembre_especifico)
salinity_sept22_25 = salinity.sel(time=septiembre_especifico)
temperature_sept22_25 = temperature.sel(time=septiembre_especifico)

# Convertir a DataFrame
df_septiembre = xr.merge([sst_septiembre, salinity_septiembre, temperature_septiembre]).to_dataframe().reset_index()
df_sept22_25 = xr.merge([sst_sept22_25, salinity_sept22_25, temperature_sept22_25]).to_dataframe().reset_index()

# 📌 Función para graficar cada variable con PUNTOS
def graficar_variable(df, columna, titulo, ylabel, color):
    plt.figure(figsize=(12, 6))
    plt.scatter(df["time"], df[columna], label=titulo, color=color, alpha=0.6, s=10)  # ⚠️ SOLO PUNTOS (scatter)
    plt.title(titulo)
    plt.xlabel("Fecha")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# 📌 Graficar para todo septiembre (solo puntos)
graficar_variable(df_septiembre, "sea_surface_temperature_anomaly", "Anomalía SST - Todo septiembre", "Anomalía (°C)", "blue")
graficar_variable(df_septiembre, "thetao", "Temperatura del océano - Todo septiembre", "Temperatura (°C)", "orange")
graficar_variable(df_septiembre, "so", "Salinidad - Todo septiembre", "Salinidad (PSU)", "red")

# 📌 Graficar para el 22-25 de septiembre (solo puntos)
graficar_variable(df_sept22_25, "sea_surface_temperature_anomaly", "Anomalía SST - 22 al 25 de septiembre", "Anomalía (°C)", "blue")
graficar_variable(df_sept22_25, "thetao", "Temperatura del océano - 22 al 25 de septiembre", "Temperatura (°C)", "orange")
graficar_variable(df_sept22_25, "so", "Salinidad - 22 al 25 de septiembre", "Salinidad (PSU)", "red")




#################################################################
#################################################################
#################################################################

import os
import xarray as xr
import matplotlib.pyplot as plt

# Ruta base
ruta_base = "/Volumes/LLACA/Python/PTM"

# Cargar cada archivo
archivo_sst = os.path.join(ruta_base, "cmems_mod_glo_phy_anfc_0.083deg-sst-anomaly_P1D-m_1737663955781.nc")
archivo_so = os.path.join(ruta_base, "cmems_mod_glo_phy-so_anfc_0.083deg_PT6H-i_1737663765616.nc")
archivo_thetao = os.path.join(ruta_base, "cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1737663696994.nc")

# Cargar los DataSets
ds_sst = xr.open_dataset(archivo_sst)  # Anomalía de temperatura
ds_so = xr.open_dataset(archivo_so)  # Salinidad
ds_thetao = xr.open_dataset(archivo_thetao)  # Temperatura

# Filtrar datos del 22 al 25 de septiembre
fecha_filtro = slice("2024-09-22", "2024-09-25")
sst_sept22_25 = ds_sst["sea_surface_temperature_anomaly"].sel(time=fecha_filtro)
salinity_sept22_25 = ds_so["so"].sel(time=fecha_filtro)
temperature_sept22_25 = ds_thetao["thetao"].sel(time=fecha_filtro)

# 📌 Función para graficar mapas de cada variable
def graficar_mapa(data_array, titulo, cmap):
    for i, fecha in enumerate(data_array.time.values):
        plt.figure(figsize=(10, 6))
        data_array.sel(time=fecha).plot(cmap=cmap, cbar_kwargs={"label": titulo})
        plt.title(f"{titulo} - {str(fecha)[:10]}")
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.grid()
        plt.tight_layout()
        plt.show()

# 📌 Graficar mapas para cada variable del 22 al 25 de septiembre
graficar_mapa(sst_sept22_25, "Anomalía de Temperatura del Mar (°C)", "coolwarm")
graficar_mapa(temperature_sept22_25, "Temperatura del Océano (°C)", "inferno")
graficar_mapa(salinity_sept22_25, "Salinidad (PSU)", "viridis")

#################################################################
#################################################################
#################################################################
import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 📌 Ruta base
ruta_base = "/Volumes/LLACA/Python/PTM"

# 📌 Cargar cada archivo
archivo_sst = os.path.join(ruta_base, "cmems_mod_glo_phy_anfc_0.083deg-sst-anomaly_P1D-m_1737663955781.nc")
archivo_so = os.path.join(ruta_base, "cmems_mod_glo_phy-so_anfc_0.083deg_PT6H-i_1737663765616.nc")
archivo_thetao = os.path.join(ruta_base, "cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1737663696994.nc")

# 📌 Cargar los DataSets
ds_sst = xr.open_dataset(archivo_sst)  # Anomalía de temperatura
ds_so = xr.open_dataset(archivo_so)  # Salinidad
ds_thetao = xr.open_dataset(archivo_thetao)  # Temperatura

# 📌 Filtrar datos del 22 al 25 de septiembre
fecha_filtro = slice("2024-09-22", "2024-09-25")
sst_sept22_25 = ds_sst["sea_surface_temperature_anomaly"].sel(time=fecha_filtro)
salinity_sept22_25 = ds_so["so"].sel(time=fecha_filtro)
temperature_sept22_25 = ds_thetao["thetao"].sel(time=fecha_filtro)

# 📌 Definir límites de la máscara (Golfo de México)
lon_golfo_min, lon_golfo_max = -97, -80  # Rango de longitud del Golfo de México
lat_golfo_min, lat_golfo_max = 18, 30  # Rango de latitud del Golfo de México

# 📌 Función para aplicar la máscara (Ocultar el Golfo de México)
def aplicar_mascara(data_array):
    return data_array.where(
        ~((data_array.longitude >= lon_golfo_min) & (data_array.longitude <= lon_golfo_max) &
          (data_array.latitude >= lat_golfo_min) & (data_array.latitude <= lat_golfo_max))
    )

# 📌 Aplicar la máscara a cada variable
sst_sept22_25 = aplicar_mascara(sst_sept22_25)
salinity_sept22_25 = aplicar_mascara(salinity_sept22_25)
temperature_sept22_25 = aplicar_mascara(temperature_sept22_25)

# 📌 Función para graficar mapas con máscara, costa e isolíneas
def graficar_mapa(data_array, titulo, cmap, levels):
    for fecha in data_array.time.values:
        # Extraer valores y eliminar dimensiones extra
        var = data_array.sel(time=fecha).squeeze().values  # Eliminar dimensiones extra
        lon = data_array.longitude.values
        lat = data_array.latitude.values

        # 📌 Asegurar que lon y lat coincidan con la forma de var
        lon_2d, lat_2d = np.meshgrid(lon, lat)

        # 📌 Crear figura con Cartopy
        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()})

        # 📌 Graficar la variable con máscara
        mesh = ax.pcolormesh(lon_2d, lat_2d, var, cmap=cmap, shading="nearest")

        # 📌 Agregar isolíneas cada nivel definido
        contours = ax.contour(lon_2d, lat_2d, var, levels=levels, colors="k", linewidths=0.8, transform=ccrs.PlateCarree())
        ax.clabel(contours, inline=True, fontsize=8, fmt="%.1f")

        # 📌 Agregar línea de costa
        ax.add_feature(cfeature.COASTLINE, edgecolor="black", linewidth=1.2)

        # 📌 Configuración del mapa
        cbar = plt.colorbar(mesh, ax=ax, orientation="vertical", label=titulo)
        ax.set_title(f"{titulo} - {str(fecha)[:10]}")
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")

        # 📌 Quitar grid
        ax.grid(False)

        # 📌 Mostrar el gráfico
        plt.show()

# 📌 Graficar mapas para cada variable con isolíneas cada **0.5** y máscara
graficar_mapa(sst_sept22_25, "Anomalía de Temperatura del Mar (°C)", "coolwarm", np.arange(-2, 2.5, 0.5))
graficar_mapa(temperature_sept22_25, "Temperatura del Océano (°C)", "inferno", np.arange(20, 31.5, 0.5))
graficar_mapa(salinity_sept22_25, "Salinidad (PSU)", "viridis", np.arange(32, 37.5, 0.5))



#################################################################
#################################################################
#################################################################
import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 📌 Ruta base
ruta_base = "/Volumes/LLACA/Python/PTM"

# 📌 Cargar cada archivo
archivo_sst = os.path.join(ruta_base, "cmems_mod_glo_phy_anfc_0.083deg-sst-anomaly_P1D-m_1737663955781.nc")
archivo_so = os.path.join(ruta_base, "cmems_mod_glo_phy-so_anfc_0.083deg_PT6H-i_1737663765616.nc")
archivo_thetao = os.path.join(ruta_base, "cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1737663696994.nc")

# 📌 Cargar los DataSets
ds_sst = xr.open_dataset(archivo_sst)  # Anomalía de temperatura
ds_so = xr.open_dataset(archivo_so)  # Salinidad
ds_thetao = xr.open_dataset(archivo_thetao)  # Temperatura

# 📌 Filtrar datos del 22 al 25 de septiembre
fecha_filtro = slice("2024-09-22", "2024-09-25")
sst_sept22_25 = ds_sst["sea_surface_temperature_anomaly"].sel(time=fecha_filtro)
salinity_sept22_25 = ds_so["so"].sel(time=fecha_filtro)
temperature_sept22_25 = ds_thetao["thetao"].sel(time=fecha_filtro)

# 📌 Definir límites de la máscara (Golfo de México)
lon_golfo_min, lon_golfo_max = -97, -80  # Longitudes del Golfo de México
lat_golfo_min, lat_golfo_max = 18, 30  # Latitudes del Golfo de México

# 📌 Aplicar máscara para ocultar el Golfo de México
def aplicar_mascara(data_array):
    return data_array.where(
        ~((data_array.longitude >= lon_golfo_min) & (data_array.longitude <= lon_golfo_max) &
          (data_array.latitude >= lat_golfo_min) & (data_array.latitude <= lat_golfo_max))
    )

# 📌 Aplicar la máscara a cada variable
sst_sept22_25 = aplicar_mascara(sst_sept22_25)
salinity_sept22_25 = aplicar_mascara(salinity_sept22_25)
temperature_sept22_25 = aplicar_mascara(temperature_sept22_25)

# 📌 Obtener valores mínimos y máximos de cada variable para asegurar **misma escala**
sst_vmin, sst_vmax = np.nanmin(sst_sept22_25.values), np.nanmax(sst_sept22_25.values)
temp_vmin, temp_vmax = np.nanmin(temperature_sept22_25.values), np.nanmax(temperature_sept22_25.values)
sal_vmin, sal_vmax = np.nanmin(salinity_sept22_25.values), np.nanmax(salinity_sept22_25.values)

# 📌 Definir niveles de isolíneas
sst_levels = np.arange(sst_vmin, sst_vmax, 0.5)
temp_levels = np.arange(temp_vmin, temp_vmax, 0.5)
sal_levels = np.arange(sal_vmin, sal_vmax, 0.5)

# 📌 Función para graficar mapas con máscara, costa e isolíneas
def graficar_mapa(data_array, titulo, cmap, vmin, vmax, levels):
    for fecha in data_array.time.values:
        var = data_array.sel(time=fecha).squeeze().values  # Eliminar dimensiones extra
        lon = data_array.longitude.values
        lat = data_array.latitude.values

        # 📌 Asegurar que lon y lat coincidan con la forma de var
        lon_2d, lat_2d = np.meshgrid(lon, lat)

        # 📌 Crear figura con Cartopy
        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()})

        # 📌 Graficar la variable con máscara y misma escala de color
        mesh = ax.pcolormesh(lon_2d, lat_2d, var, cmap=cmap, shading="nearest", vmin=vmin, vmax=vmax)

        # 📌 Agregar isolíneas
        contours = ax.contour(lon_2d, lat_2d, var, levels=levels, colors="k", linewidths=0.8, transform=ccrs.PlateCarree())
        ax.clabel(contours, inline=True, fontsize=8, fmt="%.1f")

        # 📌 Agregar línea de costa
        ax.add_feature(cfeature.COASTLINE, edgecolor="black", linewidth=1.2)

        # 📌 Configuración del mapa
        cbar = plt.colorbar(mesh, ax=ax, orientation="vertical", label=titulo)
        ax.set_title(f"{titulo} - {str(fecha)[:10]}")
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")

        # 📌 Quitar grid
        ax.grid(False)

        # 📌 Mostrar el gráfico
        plt.show()

# 📌 Graficar mapas con **misma escala** y isolíneas cada **0.5**
graficar_mapa(sst_sept22_25, "Anomalía de Temperatura del Mar (°C)", "Spectral", sst_vmin, sst_vmax, sst_levels)
graficar_mapa(temperature_sept22_25, "Temperatura del Océano (°C)", "RdYlBu", temp_vmin, temp_vmax, temp_levels)
graficar_mapa(salinity_sept22_25, "Salinidad (PSU)", "nipy_spectral", sal_vmin, sal_vmax, sal_levels)


#cividis, plasma, turbo, RdBu, Spectral, BrBg, magma, jet, hsv, ocean, rainbow
# invertir los colores en cualquier colormap, sólo agregar _r al final.