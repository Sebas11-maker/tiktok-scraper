# 🎵 TikTok Profile Scraper & Psychological Big Five Analyzer

Este proyecto es una herramienta avanzada desarrollada en **Python** utilizando **Playwright** para la extracción automatizada de métricas públicas de perfiles de TikTok, gestión de sesiones mediante cookies, análisis léxico de hashtags y minería de texto aplicada al **Modelo Psicométrico Big Five (OCEAN)**.

---

## 🌟 Características Principales

* 🍪 **Gestión Avanzada de Cookies:** Módulo independiente (`save_cookies.py`) para capturar la sesión del navegador e inyectarla (`context.add_cookies()`) evitando bloqueos de anti-bots.
* 📜 **Scroll Interactivo Automático:** Simulación de movimiento humano de mouse y desplazamientos de rueda para forzar la carga dinámica del DOM.
* 📊 **Extracción de Top 10 Posts:** Captura de URLs directas, descripciones (*captions*), reproducciones/vistas en feed.
* 🏷️ **Minería de Hashtags y Menciones:** Detección en tiempo real de tendencias e interacciones (`#hashtags` y `@menciones`).
* 🧠 **Análisis de Conducta (Big Five / OCEAN):** Evaluación léxica sobre los textos recopilados asignando puntuaciones del 0 al 100 en:
  * **Openness (Apertura a experiencias)**
  * **Conscientiousness (Responsabilidad / Foco)**
  * **Extraversion (Extraversión / Sociabilidad)**
  * **Agreeableness (Amabilidad / Empatía)**
  * **Neuroticism (Inestabilidad Emocional)**
* 💾 **Exportación Multiformato:** Generación automática de reportes estructurados en **JSON** y **CSV** dentro de la carpeta `data/`.

---

## 🛠️ Arquitectura y Tecnologías

* **Python 3.x**: Lenguaje de desarrollo.
* **Playwright**: Engine de automatización del navegador Chromium.
* **Regular Expressions (`re`)**: Extracción de entidades y patrones lingüísticos.
* **JSON / CSV**: Formatos de persistencia de datos.

---

## 📁 Estructura del Repositorio

```text
tiktok-scraper/
│
├── data/                                # Archivos generados
│   ├── cookies.json                     # Cookies de sesión persistidas
│   ├── neymarjr_full_analysis.json      # Dataset completo + Big Five + Hashtags
│   └── neymarjr_top10_posts.csv         # Tabla estructurada de las 10 publicaciones
│
├── src/
│   ├── save_cookies.py                  # Capturador de cookies del navegador
│   └── scraper.py                       # Script principal de Scraping y NLP
│
├── .gitignore                           # Exclusión de entorno virtual y temporales
├── README.md                            # Documentación técnica
└── requirements.txt                     # Lista de dependencias