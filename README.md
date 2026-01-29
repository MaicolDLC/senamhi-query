# 🌦️ ESTACIONES SENAMHI

Consulta de Estaciones SENAMHI en Python

Este repositorio contiene un script en Python para consultar estaciones meteorológicas del **SENAMHI (Perú)** directamente desde el portal web, permitiendo buscar estaciones por **nombre** o por **código**, y mostrando información clave como:

- Nombre de la estación  
- Código  
- Tipo / categoría  
- Estado de operación (automática, convencional, diferida, etc.)  
- Latitud y longitud  

Es una herramienta útil para meteorólogos, hidrólogos, estudiantes e investigadores que trabajan con datos de estaciones en el Perú.

---

## 📌 Características

- ✅ Búsqueda por nombre parcial de estación (ej. `"CUTERVO"`)  
- ✅ Búsqueda por código de estación (ej. `"106057"`)  
- ✅ Clasificación automática del tipo de estación (CP, CO, EMA, etc.)  
- ✅ Normalización del estado de la estación (AUTOMÁTICA, REAL, DIFERIDO)  
- ✅ Extracción de coordenadas geográficas (lat/lon)  
- ✅ No requiere API oficial (scraping ligero del portal SENAMHI)  

---

## 🛠️ Requisitos

- Python 3.8 o superior  
- Librerías:

```python
pip install requests
pip install git+https://github.com/MaicolDLC/senamhi-query.git
```
```python
from senamhi_query import get_station
```

## 🚀 Uso básico

## Buscar por nombre de estación
```python
estacion = get_station("cutervo")
```
## Ejemplo de salida 

```text
---------------------------------------------------------------------------
───────────────────────────────────────────────────────────────────────────
Estación   : CUTERVO
Código     : 106057
Categoría  : CO → Climatológica Ordinaria
Estado     : REAL (CONV)
Lat / Lon  : -6.37964 , -78.80512
───────────────────────────────────────────────────────────────────────────
Estación   : CUTERVO
Código     : 4726602
Categoría  : EMA → Meteorológica Automática
Estado     : AUTOMATICA
Lat / Lon  : -6.37914 , -78.81339
───────────────────────────────────────────────────────────────────────────
---------------------------------------------------------------------------
```

## Buscar por código de estación 
```python
estacion = get_station("106057")
o
estacion = get_station(106057)
```
## Ejemplo de salida 

```text
---------------------------------------------------------------------------
Estación   : CUTERVO
Código     : 106057
Categoría  : CO → Climatológica Ordinaria
Estado     : REAL (CONV)
Lat / Lon  : -6.37964 , -78.80512
---------------------------------------------------------------------------
```

## Buscar por segmento de palabra 
```python
estacion = get_station("tocache")
```

## Ejemplo de salida 

```text
---------------------------------------------------------------------------
───────────────────────────────────────────────────────────────────────────
Estación   : PUENTE TOCACHE
Código     : 230700
Categoría  : HLG → Hidrológica Limnigráfica
Estado     : REAL (CONV)
Lat / Lon  : -8.18475 , -76.50789
───────────────────────────────────────────────────────────────────────────
Estación   : TOCACHE
Código     : 472456
Categoría  : EHMA → Hidrometeorológica Automática
Estado     : AUTOMATICA
Lat / Lon  : -8.18475 , -76.50789
───────────────────────────────────────────────────────────────────────────
---------------------------------------------------------------------------
```
## Observar todas las estaciones 
```python
todas = get_station("")
```
## Observar todas las EMA  
```python
ema = get_station(categoria_filtro = "EMA") 
```
## Observar todas las estaciones que contengan "PUENTE" y sean EMA 
```python
puente_ema = get_station("PUENTE", categoria_filtro = "EMA") 
```

## Utilizar variable 
```python
codigos = [e["codigo"] for e in estacion]
print("Códigos encontrados:", codigos)
```
```text
Códigos encontrados: ['106057', '4726602']
```
```python
# Tomar solo estaciones automáticas
emas = [e for e in estacion if e["estado"] == "AUTOMATICA"]

for e in emas:
    print("EMA:", e["codigo"]) 
```
```text
EMA: 4726602
```
## Variables existentes 
```python
estacion[0].keys()
```
```text
dict_keys(['estacion', 'categoria', 'lat', 'lon', 'ico', 'codigo', 'estado_srv', 'estado_raw', 'estado']) 
```

## 📊 Tipos de estaciones SENAMHI 

| Sigla | Tipo de estación             |
| ----- | ---------------------------- |
| CP    | Climatológica Principal      |
| CO    | Climatológica Ordinaria      |
| EMA   | Meteorológica Automática     |
| EAMA  | Agrometeorológica Automática |
| PLU   | Pluviométrica                |
| HLM   | Hidrológica Limnimétrica     |
| HLG   | Hidrológica Limnigráfica     |
| SIN   | Sinóptica                    |
| O     | Oceanográfica Automática     |
| PE    | Propósito Específico         |


---
⚠️ Notas importantes

- ✅ Este script obtiene la información directamente desde el portal web del SENAMHI.
- ✅ Si el portal cambia su estructura, el script puede requerir ajustes.
- ✅ No es una API oficial.
- ✅ Uso recomendado para fines académicos, técnicos y de investigación. 

📈 Posibles mejoras futuras

- ✅ Exportar resultados a CSV o JSON
- ✅ Integrar descarga automática de variables meteorológicas

---
👨‍💻 Autor : Michael De La Cruz 

✉️ : michael.dlc.lr@gmail.com / 20180176@lamolina.edu.pe 

Mi pequeño aporte para la comunidad Meteorológica del Perú. 
--- 
