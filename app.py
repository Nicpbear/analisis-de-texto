import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator
from streamlit_lottie import st_lottie

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Texto Simple",
    page_icon="🔍",
    layout="wide"
)

# Título y descripción
st.title("📜 Analizador de Texto con TextBlob")
st.markdown("""
Esta aplicación utiliza TextBlob para analizar texto:
- 📊 **Sentimiento y subjetividad**
- 🔑 **Palabras clave**
- 📈 **Frecuencia de palabras**
""")

# Barra lateral
st.sidebar.title("⚙️ Opciones")
modo = st.sidebar.selectbox(
    "📥 Selecciona el modo de entrada:",
    ["✍️ Texto directo", "📂 Archivo de texto"]
)

# Inicializar el traductor
translator = Translator()

# Función para traducir texto del español al inglés
def traducir_texto(texto):
    try:
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"❌ Error al traducir: {e}")
        return texto

# Función para procesar el texto con TextBlob
def procesar_texto(texto):
    texto_original = texto
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }

import json
with open ("gato.json") as source:
  animation=json.load(source)
st.lottie(animation,width = 350)


# Función para mostrar resultados
def mostrar_resultados(resultados):
    st.subheader("📊 Resultados del análisis")
    sentimiento_norm = (resultados["sentimiento"] + 1) / 2
    st.write("**Sentimiento:**", "😊" if resultados["sentimiento"] > 0 else "😠")
    st.progress(sentimiento_norm)
    
    st.write("**Subjetividad:**", "📖 Alta" if resultados["subjetividad"] > 0.5 else "🎯 Baja")
    
    st.subheader("🌍 Traducción del Texto")
    st.markdown(f"🔤 **Original:** {resultados['texto_original']}")
    st.markdown(f"🗣️ **Inglés:** {resultados['texto_traducido']}")

# Entrada de texto
if modo == "✍️ Texto directo":
    texto_usuario = st.text_area("📝 Ingresa el texto aquí:")
    if st.button("🔎 Analizar") and texto_usuario:
        resultados = procesar_texto(texto_usuario)
        mostrar_resultados(resultados)

elif modo == "📂 Archivo de texto":
    archivo = st.file_uploader("📤 Sube un archivo de texto", type=["txt"])
    if archivo:
        texto_archivo = archivo.read().decode("utf-8")
        if st.button("🔎 Analizar"):
            resultados = procesar_texto(texto_archivo)
            mostrar_resultados(resultados)

