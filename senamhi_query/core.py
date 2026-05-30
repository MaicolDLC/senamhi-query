import requests
import re


def get_station(criterio_busqueda="", categoria=None, imprimir=False):

    CATEGORIAS_SENAMHI = {
        "CP": "Climatológica Principal",
        "CO": "Climatológica Ordinaria",
        "MAP": "Meteorológica Agrícola Principal",
        "PLU": "Pluviométrica",
        "HLM": "Hidrológica Limnimétrica",
        "HLG": "Hidrológica Limnigráfica",
        "EMA": "Meteorológica Automática",
        "EAMA": "Agrometeorológica Automática",
        "EHA": "Hidrológica Automática",
        "EHMA": "Hidrometeorológica Automática",
        "EAA": "Ambiental Automática",
        "SIN": "Sinóptica",
        "O": "Oceanográfica Automática",
        "PE": "Propósito Específico"
    }

    url = "https://www.senamhi.gob.pe/mapas/mapa-estaciones-2/"

    try:
        html = requests.get(url, timeout=20).text
    except Exception as e:
        print(f"Error de conexión: {e}")
        return []

    buscar_por_codigo = str(criterio_busqueda).isdigit()
    criterio = str(criterio_busqueda).upper()
    cat_target = categoria.upper() if categoria else None

    bloques = html.split('"nom":')
    estaciones_encontradas = []

    for bloque in bloques[1:]:

        nombre = bloque.split('"')[1]
        partes = bloque.split(',')

        est = {"estacion": nombre}

        # =====================================================
        # EXTRAER DATOS DEL MAPA PRINCIPAL
        # =====================================================
        for p in partes:

            if '"cod":' in p:
                est["codigo"] = re.sub(r"\D", "", p)

            elif '"cate":' in p:
                est["categoria"] = p.replace('"cate":', '').strip().strip('"')

            elif '"estado":' in p:
                est["estado_srv"] = p.replace('"estado":', '').strip().strip('"')
                est["estado_raw"] = re.sub(r"[^A-Z]", "", est["estado_srv"].upper())

            elif '"ico":' in p:
                est["ico"] = p.replace('"ico":', '').strip().strip('"')

            elif '"lat":' in p:
                est["lat"] = float(p.replace('"lat":', '').strip())

            elif '"lon":' in p:
                est["lon"] = float(p.replace('"lon":', '').strip())

        # =====================================================
        # FILTROS
        # =====================================================
        coincide = False

        if not criterio:
            coincide = True
        elif buscar_por_codigo and est.get("codigo") == criterio:
            coincide = True
        elif not buscar_por_codigo and criterio in nombre.upper():
            coincide = True

        if not coincide:
            continue

        if cat_target and est.get("categoria", "").upper() != cat_target:
            continue

        # =====================================================
        # ESTADO LEGIBLE
        # =====================================================
        estado_raw = est.get("estado_raw", "")

        if "AUTO" in estado_raw:
            estado_final = "AUTOMATICA"
        elif "REAL" in estado_raw:
            estado_final = "REAL (CONV)"
        elif "DIF" in estado_raw:
            estado_final = "DIFERIDO (CONV)"
        else:
            estado_final = "NO DEFINIDO"

        est["estado"] = estado_final

        # =====================================================
        # DESCRIPCIÓN CATEGORÍA
        # =====================================================
        sigla_cat = est.get("categoria", "ND")
        est["categoria_desc"] = CATEGORIAS_SENAMHI.get(sigla_cat, "No definida por SENAMHI")

        # =====================================================
        # SEGUNDA CONSULTA
        # =====================================================
        try:

            url_detalle = (
                "https://www.senamhi.gob.pe/mapas/"
                "mapa-estaciones-2/"
                f"map_red_graf.php?"
                f"cod={est['codigo']}"
                f"&estado={est['estado_srv']}"
                f"&tipo_esta=M"
                f"&cate={est['categoria']}"
                "&cod_old="
            )

            html_detalle = requests.get(url_detalle, timeout=20).text

            # ==========================================
            # EXTRAER SUBTITLE
            # ==========================================
            m = re.search(r'text:\s*"([^"]+)"', html_detalle, re.S)

            if m:

                subtitle = m.group(1)

                m_dep = re.search(r"Dep\.\:\s*(.*?)\s+Prov\.\:", subtitle)
                m_prov = re.search(r"Prov\.\:\s*(.*?)\s+Dist\.\:", subtitle)
                m_dist = re.search(r"Dist\.\:\s*(.*?)<br>", subtitle)
                m_alt = re.search(r"Alt\.\:\s*(.*?)<br>", subtitle)

                est["departamento"] = m_dep.group(1).strip() if m_dep else None
                est["provincia"] = m_prov.group(1).strip() if m_prov else None
                est["distrito"] = m_dist.group(1).strip() if m_dist else None
                est["altitud"] = m_alt.group(1).strip() if m_alt else None

            else:

                est["departamento"] = None
                est["provincia"] = None
                est["distrito"] = None
                est["altitud"] = None

        except Exception:

            est["departamento"] = None
            est["provincia"] = None
            est["distrito"] = None
            est["altitud"] = None

        # =====================================================
        # IMPRIMIR
        # =====================================================
        if imprimir:

            print("─" * 75)
            print(f"Estación   : {est['estacion']}")
            print(f"Código     : {est.get('codigo')}")
            print(f"Categoría  : {sigla_cat} → {est['categoria_desc']}")
            print(f"Estado     : {estado_final}")
            print(f"Lat / Lon  : {est.get('lat')} , {est.get('lon')}")
            print(
                f"Dpto/Prov/Dist : "
                f"{est.get('departamento')} | "
                f"{est.get('provincia')} | "
                f"{est.get('distrito')}"
            )
            print(f"Altitud    : {est.get('altitud')}")

        estaciones_encontradas.append(est)

    if imprimir:
        print("─" * 75)
        print(f"Total estaciones encontradas: {len(estaciones_encontradas)}")

    return estaciones_encontradas 
