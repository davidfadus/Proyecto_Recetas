import streamlit as st
import json
import os

# Configuración de la página (Optimizada para celular)
st.set_page_config(page_title="Mis Recetas IA", page_icon="🍳", layout="centered")

st.title("🍳 Mi Recetario Inteligente")
st.write("Buscá y filtrá entre todas tus recetas extraídas automáticamente.")

# 1. Cargar la base de datos JSON de forma segura
archivo_datos = "mis_recetas_extraidas.json"

if not os.path.exists(archivo_datos):
    st.warning("⚠️ Todavía se está creando la base de datos... ¡Esperá a que el script termine o procese las primeras recetas!")
    st.stop()

with open(archivo_datos, "r", encoding="utf-8") as f:
    recetas = json.load(f)

if not recetas:
    st.info("La lista está vacía por ahora. Esperando datos...")
    st.stop()

# 2. Recolectar todos los ingredientes únicos para el filtro avanzado
todos_los_ingredientes = set()
for r in recetas:
    if "tags_ingredientes" in r and r["tags_ingredientes"]:
        for ing in r["tags_ingredientes"]:
            todos_los_ingredientes.add(ing.strip().capitalize())
lista_ingredientes_ordenada = sorted(list(todos_los_ingredientes))

# 3. FILTROS (Interfaz de usuario limpia y compacta)
st.sidebar.header("🔍 Filtros Avanzados")

# Buscador por texto en el título
busqueda_titulo = st.text_input("Buscar por nombre de receta:", "")

# Filtro multi-selección de ingredientes
filtro_ingredientes = st.sidebar.multiselect(
    "Filtrar por ingrediente/s:", 
    options=lista_ingredientes_ordenada
)

# Filtros desplegables de atributos
filtro_dificultad = st.sidebar.selectbox("Dificultad:", ["Todas", "fácil", "intermedio", "difícil"])
filtro_comida = st.sidebar.selectbox("Momento del día:", ["Todas", "desayuno", "merienda", "desayuno/merienda", "almuerzo/cena"])
filtro_saludable = st.sidebar.selectbox("Calidad Alimenticia:", ["Todas", "muy saludable", "medianamente saludable", "poco saludable"])

# 4. APLICAR FILTROS A LA LISTA
recetas_filtradas = []

for r in recetas:
    # Filtro por título
    if busqueda_titulo and busqueda_titulo.lower() not in r.get("titulo", "").lower():
        continue
        
    # Filtro por ingredientes (debe contener TODOS los seleccionados)
    if filtro_ingredientes:
        ingredientes_receta = [i.strip().capitalize() for i in r.get("tags_ingredientes", [])]
        if not all(ing in ingredientes_receta for ing in filtro_ingredientes):
            continue
            
    # Filtro por dificultad
    if filtro_dificultad != "Todas" and r.get("dificultad") != filtro_dificultad:
        continue
        
    # Filtro por momento del día
    if filtro_comida != "Todas" and r.get("comida") != filtro_comida:
        continue
        
    # Filtro por calidad alimenticia
    if filtro_saludable != "Todas" and r.get("calidad_alimenticia") != filtro_saludable:
        continue
        
    recetas_filtradas.append(r)

# 5. MOSTRAR RESULTADOS (Ultra liviano en formato acordeón)
st.subheader(f"Recetas encontradas: {len(recetas_filtradas)}")

for r in recetas_filtradas:
    # Creamos un desplegable para cada receta
    with st.expander(f"📖 {r.get('titulo', 'Sin Título')} | ({r.get('comida', 'General')})"):
        
        # Tags rápidos de información
        col1, col2, col3 = st.columns(3)
        col1.write(f"**Dificultad:** {r.get('dificultad', 'N/A')}")
        col2.write(f"**Salud:** {r.get('calidad_alimenticia', 'N/A')}")
        col3.write(f"**Disponibilidad:** {r.get('disponibilidad_santa_fe', 'N/A')}")
        
        st.write("---")
        
        # Lista de ingredientes
        st.write("**Ingredientes principales:**")
        st.write(", ".join(r.get("tags_ingredientes", [])))
        
        # Paso a paso
        st.write("**Pasos de preparación:**")
        for paso in r.get("pasos", []):
            st.write(f"- {paso}")
            
        st.write("---")
        
        # EL ENLACE A YOUTUBE REQUERIDO
        # Creamos un botón limpio que abre el video original en una pestaña nueva
        url_video = r.get("url_original", "https://www.youtube.com")
        st.link_button("📺 Ver video original en YouTube", url_video)