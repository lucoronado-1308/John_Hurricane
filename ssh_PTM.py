#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 12:27:28 2025

@author: lucoronado
"""

import os
import xarray as xr

# Ruta del archivo
directorio = "/Volumes/LLACA/Python/PTM"
archivo = "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_1737738981574.nc"
ruta = os.path.join(directorio, archivo)

# Abrir el archivo NetCDF
ds = xr.open_dataset(ruta)

# Mostrar información general del archivo
print("\n--- Información General ---\n")
print(ds)

# Listar variables disponibles
print("\n--- Variables Disponibles ---\n")
for var in ds.data_vars:
    print(f"- {var}: {ds[var].attrs.get('long_name', 'No disponible')} ({ds[var].attrs.get('units', 'Sin unidades')})")

# Dimensiones del archivo
print("\n--- Dimensiones ---\n")
print(ds.dims)

# Coordenadas del archivo
print("\n--- Coordenadas ---\n")
print(ds.coords)

# Atributos globales
print("\n--- Atributos Globales ---\n")
for attr, value in ds.attrs.items():
    print(f"{attr}: {value}")

# Cerrar el archivo
print("\nExploración completada.")
#################################################################
#################################################################
#################################################################

import os
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd

# Ruta del archivo
directorio = "/Volumes/LLACA/Python/PTM"
archivo = "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_1737738981574.nc"
ruta = os.path.join(directorio, archivo)

# Abrir el archivo NetCDF
ds = xr.open_dataset(ruta)

# Seleccionar la variable zos (SSH)
zos = ds["zos"]

# Filtrar las fechas del 1 al 30 de septiembre de 2024
zos = zos.sel(time=slice("2024-09-01", "2024-09-30"))

# Calcular el promedio, mínimo y máximo diarios
zos_daily_mean = zos.resample(time="1D").mean(dim=["latitude", "longitude"])
zos_daily_min = zos.resample(time="1D").min(dim=["latitude", "longitude"])
zos_daily_max = zos.resample(time="1D").max(dim=["latitude", "longitude"])

# Extraer valores y fechas
dates = zos_daily_mean["time"].values
mean_values = zos_daily_mean.values
min_values = zos_daily_min.values
max_values = zos_daily_max.values

# Graficar la serie de tiempo
plt.figure(figsize=(12, 6))
plt.plot(dates, mean_values, label="Promedio diario", color="black", linestyle="--", marker="o")
plt.plot(dates, min_values, label="Mínimos diarios", color="red", linestyle="--", marker="x")
plt.plot(dates, max_values, label="Máximos diarios", color="blue", linestyle="--", marker="x")

# Configuración del eje X para reflejar días del mes
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%Y-%m-%d"))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=2))  # Mostrar cada 2 días
plt.xlim(pd.to_datetime(["2024-09-01", "2024-09-30"]))  # Limitar el rango al mes de septiembre

# Configuración general del gráfico
plt.title("Serie de tiempo de SSH (m) - Septiembre 2024")
plt.xlabel("Fecha")
plt.ylabel("SSH (m)")
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()

# Mostrar el gráfico
plt.show()

# Crear mapas diarios para fechas seleccionadas
fechas = ["2024-09-22", "2024-09-23", "2024-09-24", "2024-09-25"]
for fecha in fechas:
    # Filtrar datos horarios del día y promediar
    zos_dia = zos.sel(time=slice(f"{fecha}T00:00", f"{fecha}T23:59")).mean(dim="time")
    
    # Graficar el mapa
    plt.figure(figsize=(10, 6))
    zos_dia.plot(cmap="coolwarm", cbar_kwargs={"label": "SSH (m)"})
    plt.title(f"Mapa de SSH (m) - {fecha}")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid()
    plt.tight_layout()
    plt.show()
    
    
    
    ###########
    ###########
    
    
    
import matplotlib.pyplot as plt
import pandas as pd

# Fechas ajustadas: rango diario desde el 1 al 30 de septiembre de 2024
dates = pd.date_range(start="2024-09-01", periods=len(mean_values), freq="D")

# Graficar solo el rango de septiembre de 2024
plt.figure(figsize=(12, 6))
plt.plot(dates, mean_values, label="Promedio diario", color="black", linestyle="--", marker="o")
plt.plot(dates, min_values, label="Mínimos diarios", color="red", linestyle="--", marker="x")
plt.plot(dates, max_values, label="Máximos diarios", color="blue", linestyle="--", marker="x")

# Configuración del eje X para reflejar días del mes
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%Y-%m-%d"))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=2))  # Mostrar cada 2 días
plt.xlim(pd.to_datetime(["2024-09-01", "2024-09-30"]))  # Limitar el rango al mes de septiembre

# Configuración general del gráfico
plt.title("Serie de tiempo de SSH (m) - Septiembre 2024")
plt.xlabel("Fecha")
plt.ylabel("SSH (m)")
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()

# Mostrar el gráfico
plt.show()

#################################################################
#################################################################
#################################################################

import os
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd

# 📌 Ruta del archivo NetCDF
directorio = "/Volumes/LLACA/Python/PTM"
archivo = "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_1737738981574.nc"
ruta = os.path.join(directorio, archivo)

# 📌 Abrir el archivo NetCDF
ds = xr.open_dataset(ruta)

# 📌 Seleccionar la variable zos (SSH)
zos = ds["zos"]

# 📌 Convertir las fechas a datetime
zos["time"] = pd.to_datetime(zos["time"].values)

# 📌 Convertir a DataFrame
df = zos.to_dataframe().reset_index()

# 📌 Renombrar la variable zos a ssh
df = df.rename(columns={"zos": "ssh"})

# 📌 Gráfica para TODO septiembre (1 al 30)
plt.figure(figsize=(12, 6))
plt.scatter(df["time"], df["ssh"], color="blue", alpha=0.5, label="SSH (m)")
plt.title("Serie de tiempo de SSH (m) - Todo septiembre 2024")
plt.xlabel("Fecha")
plt.ylabel("SSH (m)")
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

# 📌 Filtrar SOLO del 22 al 25 de septiembre
df_filtered = df[(df["time"] >= "2024-09-22") & (df["time"] <= "2024-09-25")]

# 📌 Gráfica para SOLO el 22 al 25 de septiembre
plt.figure(figsize=(12, 6))
plt.scatter(df_filtered["time"], df_filtered["ssh"], color="red", alpha=0.5, label="SSH (m)")
plt.title("Serie de tiempo de SSH (m) - 22 al 25 de septiembre 2024")
plt.xlabel("Fecha")
plt.ylabel("SSH (m)")
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()


#################################################################
#################################################################
#################################################################
import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# 📌 Ruta del archivo NetCDF
directorio = "/Volumes/LLACA/Python/PTM"
archivo = "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_1737738981574.nc"
ruta = os.path.join(directorio, archivo)

# 📌 Abrir el archivo NetCDF
ds = xr.open_dataset(ruta)

# 📌 Seleccionar la variable zos (SSH)
zos = ds["zos"]

# 📌 Filtrar las fechas del 22 al 25 de septiembre de 2024
fechas = ["2024-09-22", "2024-09-23", "2024-09-24", "2024-09-25"]

# 📌 Crear mapas para cada fecha
for fecha in fechas:
    # Filtrar datos horarios del día y promediar
    zos_dia = zos.sel(time=slice(f"{fecha}T00:00", f"{fecha}T23:59")).mean(dim="time")

    # 📌 Asegurar que `zos_dia` tenga dimensiones (lat, lon) eliminando dimensiones extra
    zos_dia = zos_dia.squeeze()

    # 📌 Obtener coordenadas de latitud y longitud
    lon = zos_dia.longitude.values
    lat = zos_dia.latitude.values
    ssh_values = zos_dia.values

    # 📌 Crear la figura
    plt.figure(figsize=(10, 6))

    # 📌 Graficar SSH como mapa de colores
    ssh_plot = plt.pcolormesh(lon, lat, ssh_values, cmap="coolwarm", shading="nearest")

    # 📌 Agregar isolineas cada 0.2m
    contours = plt.contour(lon, lat, ssh_values, levels=np.arange(np.nanmin(ssh_values), np.nanmax(ssh_values), 0.2), colors="k", linewidths=0.8)
    plt.clabel(contours, inline=True, fontsize=8, fmt="%.2f")

    # 📌 Configuración del mapa
    plt.colorbar(ssh_plot, label="SSH (m)")
    plt.title(f"Mapa de SSH (m) - {fecha}")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")

    # 📌 Quitar grid
    plt.grid(False)

    # 📌 Mostrar el gráfico
    plt.show()


################################################################
#################################################################
#################################################################

import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 📌 Ruta del archivo NetCDF
ruta_base = "/Volumes/LLACA/Python/PTM"
archivo_ssh = os.path.join(ruta_base, "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_1737738981574.nc")

# 📌 Cargar dataset de SSH
ds_ssh = xr.open_dataset(archivo_ssh)
ssh = ds_ssh["zos"]

# 📌 Filtrar fechas del 22 al 25 de septiembre
fecha_filtro = slice("2024-09-22", "2024-09-25")
ssh_sept22_25 = ssh.sel(time=fecha_filtro)

# 📌 Definir límites de la máscara (Golfo de México)
lon_golfo_min, lon_golfo_max = -97, -80  # Longitud del Golfo
lat_golfo_min, lat_golfo_max = 18, 30  # Latitud del Golfo

# 📌 Aplicar máscara para eliminar el Golfo de México
ssh_sept22_25 = ssh_sept22_25.where(
    ~((ssh_sept22_25.longitude >= lon_golfo_min) & (ssh_sept22_25.longitude <= lon_golfo_max) &
      (ssh_sept22_25.latitude >= lat_golfo_min) & (ssh_sept22_25.latitude <= lat_golfo_max))
)

# 📌 Obtener valores mínimos y máximos de SSH para la misma escala
ssh_min_val = np.nanmin(ssh_sept22_25.values)
ssh_max_val = np.nanmax(ssh_sept22_25.values)

# 📌 Definir niveles de isolíneas cada 0.2 m
contour_levels = np.arange(ssh_min_val, ssh_max_val, 0.2)

# 📌 Función para graficar mapas con isolíneas y máscara
def graficar_mapa(data_array, titulo, cmap, vmin, vmax, levels):
    for fecha in data_array.time.values:
        var = data_array.sel(time=fecha).squeeze().values  # Eliminar dimensiones extra
        lon = data_array.longitude.values
        lat = data_array.latitude.values

        # 📌 Asegurar que lon y lat coincidan con la forma de var
        lon_2d, lat_2d = np.meshgrid(lon, lat)

        # 📌 Crear figura con Cartopy
        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()})

        # 📌 Graficar SSH con máscara y misma escala de color
        mesh = ax.pcolormesh(lon_2d, lat_2d, var, cmap=cmap, shading="nearest", vmin=vmin, vmax=vmax)

        # 📌 Agregar isolíneas cada 0.2 m
        contours = ax.contour(lon_2d, lat_2d, var, levels=levels, colors="k", linewidths=0.8, transform=ccrs.PlateCarree())
        ax.clabel(contours, inline=True, fontsize=8, fmt="%.2f")

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

# 📌 Graficar mapas de SSH con misma escala de color e isolíneas cada 0.2 m
graficar_mapa(ssh_sept22_25, "Altura de la Superficie del Mar (m)", "coolwarm", ssh_min_val, ssh_max_val, contour_levels)




################################################################
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
archivo_ssh = os.path.join(ruta_base, "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_1737738981574.nc")

# 📌 Cargar dataset de SSH
ds_ssh = xr.open_dataset(archivo_ssh)
ssh = ds_ssh["zos"]

# 📌 Filtrar fechas del 22 al 25 de septiembre
fecha_filtro = slice("2024-09-22", "2024-09-25")
ssh_sept22_25 = ssh.sel(time=fecha_filtro)

# 📌 Definir límites de la máscara (Golfo de México)
lon_golfo_min, lon_golfo_max = -97, -80  # Rango de longitud del Golfo
lat_golfo_min, lat_golfo_max = 18, 30  # Rango de latitud del Golfo

# 📌 Función para aplicar la máscara
def aplicar_mascara(data_array):
    return data_array.where(
        ~((data_array.longitude >= lon_golfo_min) & (data_array.longitude <= lon_golfo_max) &
          (data_array.latitude >= lat_golfo_min) & (data_array.latitude <= lat_golfo_max))
    )

# 📌 Aplicar la máscara a SSH
ssh_sept22_25 = aplicar_mascara(ssh_sept22_25)

# 📌 Función para graficar mapas con isolíneas y máscara
def graficar_mapa(data_array, titulo, cmap, levels):
    for fecha in data_array.time.values:
        var = data_array.sel(time=fecha).squeeze().values  # Eliminar dimensiones extra
        lon = data_array.longitude.values
        lat = data_array.latitude.values

        # 📌 Asegurar que lon y lat coincidan con la forma de var
        lon_2d, lat_2d = np.meshgrid(lon, lat)

        # 📌 Crear figura con Cartopy
        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()})

        # 📌 Graficar SSH con máscara
        mesh = ax.pcolormesh(lon_2d, lat_2d, var, cmap=cmap, shading="nearest")

        # 📌 Agregar isolíneas cada 0.2 m
        contours = ax.contour(lon_2d, lat_2d, var, levels=levels, colors="k", linewidths=0.8, transform=ccrs.PlateCarree())
        ax.clabel(contours, inline=True, fontsize=8, fmt="%.2f")

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

# 📌 Graficar mapas de SSH con isolíneas cada 0.2 m
graficar_mapa(ssh_sept22_25, "Altura de la Superficie del Mar (m)", "coolwarm", np.arange(-1, 1.2, 0.2))


###############################################################
#################################################################
#



import os
import xarray as xr
import pandas as pd

# Ruta del archivo
directorio = "/Volumes/LLACA/Python/PTM"
archivo = "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_1737738981574.nc"
ruta = os.path.join(directorio, archivo)

# Abrir el archivo NetCDF
ds = xr.open_dataset(ruta)

# Seleccionar la variable zos (SSH)
zos = ds["zos"]

# Convertir las fechas a formato datetime para compatibilidad
zos["time"] = pd.to_datetime(zos["time"].values)

# Convertir los datos a un DataFrame con las columnas requeridas
df = zos.to_dataframe().reset_index()

# Filtrar las fechas del 1 al 30 de septiembre de 2024
df = df[(df["time"] >= "2024-09-01") & (df["time"] <= "2024-09-30")]

# Cambiar el formato de la columna time a 'yyyy-mm-dd' y renombrar zos a ssh
df["time"] = df["time"].dt.strftime("%Y-%m-%d")
df = df.rename(columns={"zos": "ssh"})

# Guardar el DataFrame en un archivo CSV con las columnas requeridas
output_file = "ssh_septiembre_2024.csv"
df[["time", "longitude", "latitude", "ssh"]].to_csv(output_file, index=False)

print(f"Archivo CSV guardado como {output_file}")






import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 📌 Ruta del archivo NetCDF
ruta_base = "/Volumes/LLACA/Python/PTM"
archivo_ssh = os.path.join(ruta_base, "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_1737738981574.nc")

# 📌 Cargar dataset de SSH
ds_ssh = xr.open_dataset(archivo_ssh)
ssh = ds_ssh["zos"]

# 📌 Filtrar fechas del 22 al 25 de septiembre
fecha_filtro = slice("2024-09-22", "2024-09-25")
ssh_sept22_25 = ssh.sel(time=fecha_filtro)

# 📌 Definir límites de la máscara (Golfo de México)
lon_golfo_min, lon_golfo_max = -97, -80  # Longitud del Golfo
lat_golfo_min, lat_golfo_max = 18, 30  # Latitud del Golfo

# 📌 Aplicar máscara para eliminar el Golfo de México
ssh_sept22_25 = ssh_sept22_25.where(
    ~((ssh_sept22_25.longitude >= lon_golfo_min) & (ssh_sept22_25.longitude <= lon_golfo_max) &
      (ssh_sept22_25.latitude >= lat_golfo_min) & (ssh_sept22_25.latitude <= lat_golfo_max))
)

# 📌 Obtener valores mínimos y máximos de SSH para la misma escala
ssh_min_val = np.nanmin(ssh_sept22_25.values)
ssh_max_val = np.nanmax(ssh_sept22_25.values)

# 📌 Definir niveles de isolíneas cada 0.2 m
contour_levels = np.arange(ssh_min_val, ssh_max_val, 0.2)

# 📌 Función para graficar mapas con isolíneas y máscara
def graficar_mapa(data_array, titulo, cmap, vmin, vmax, levels):
    for fecha in data_array.time.values:
        var = data_array.sel(time=fecha).squeeze().values  # Eliminar dimensiones extra
        lon = data_array.longitude.values
        lat = data_array.latitude.values

        # 📌 Asegurar que lon y lat coincidan con la forma de var
        lon_2d, lat_2d = np.meshgrid(lon, lat)

        # 📌 Crear figura con Cartopy
        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()})

        # 📌 Graficar SSH con máscara y misma escala de color
        mesh = ax.pcolormesh(lon_2d, lat_2d, var, cmap=cmap, shading="nearest", vmin=vmin, vmax=vmax)

        # 📌 Agregar isolíneas cada 0.2 m
        contours = ax.contour(lon_2d, lat_2d, var, levels=levels, colors="k", linewidths=0.8, transform=ccrs.PlateCarree())
        ax.clabel(contours, inline=True, fontsize=8, fmt="%.2f")

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

# 📌 Graficar mapas de SSH con misma escala de color e isolíneas cada 0.2 m
graficar_mapa(ssh_sept22_25, "Altura de la Superficie del Mar (m)", "coolwarm", ssh_min_val, ssh_max_val, contour_levels)




