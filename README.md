# TikTok Profile Scraper & Big Five Personality Analysis (Playwright & Python)

Este proyecto es una herramienta integral desarrollada en Python que combina **Web Scraping dinámico** con **Análisis de Conducta/Personalidad (Modelo Big Five / OCEAN)** a partir de datos públicos extraídos de TikTok.

## 🎯 Objetivos del Proyecto

1. Extraer métricas públicas del perfil de un usuario (Nombre, Seguidores, Me Gusta Totales, Biografía).
2. Scraping de los **10 primeros posts** publicados (URLs, vistas/likes en feed y descripciones).
3. Aplicar un algoritmo de procesamiento de lenguaje natural (NLP basico / léxico) para calcular los 5 rasgos del modelo de personalidad **Big Five (OCEAN)**.
4. Persistir la información en formatos **JSON** y **CSV**.

## 🧠 Modelo de Personalidad Big Five (OCEAN)

El script evalúa el texto acumulado del perfil y de las publicaciones clasificándolo en 5 dimensiones:
* **Openness (Apertura a la experiencia):** Creatividad, interés por el arte, deporte y experiencias nuevas.
* **Conscientiousness (Responsabilidad):** Foco, disciplina, trabajo y orientación a metas.
* **Extraversion (Extraversión):** Sociabilidad, festejos, entusiasmo y energía.
* **Agreeableness (Amabilidad):** Empatía, mensajes de unión, gratitud y valores.
* **Neuroticism (Inestabilidad emocional):** Expresión de presión, cansancio o momentos difíciles.

## 🛠️ Tecnologías Utilizadas

* **Python 3.x**: Lenguaje de programación base.
* **Playwright**: Automatización del motor Chromium para renderizado del DOM dinámico.
* **Regular Expressions (re)**: Extracción léxica para la puntuación del modelo Big Five.
* **JSON / CSV**: Formatos estructurados para el almacenamiento de datos.

## 📁 Estructura del Proyecto

```text
tiktok-scraper/
│
├── data/                                # Resultados generados
│   ├── neymarjr_full_analysis.json      # Dataset completo + Big Five
│   └── neymarjr_top10_posts.csv         # Tabla con los 10 posts
├── src/
│   └── scraper.py                       # Código fuente principal
├── .gitignore                           # Exclusión de venv y archivos basura
├── README.md                            # Documentación técnica
└── requirements.txt                     # Lista de dependencias