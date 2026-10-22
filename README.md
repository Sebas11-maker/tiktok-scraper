# TikTok Profile Scraper & Big Five Personality Analysis

Este repositorio contiene una herramienta automatizada desarrollada en Python con **Playwright** para la extracción de publicaciones, métricas y análisis comportamental de perfiles de TikTok.

El proyecto implementa un mecanismo de **persistencia de sesión e inyección de cookies HTTP** para evitar restricciones de autenticación y detección de bots, procesando la información extraída a través de un modelo de evaluación psicométrica basado en el **Big Five (OCEAN)**.

---

## 📌 Características Principales

* **Inyección e Ingesta de Cookies de Sesión:** Carga de tokens esenciales (`sessionid`, `ttwid`, `msToken`, etc.) desde `data/cookies.json` para mantener una sesión de navegador autenticada de forma transparente.
* **Scraping Dinámico Asíncrono:** Utiliza `asyncio` y Playwright para emular el comportamiento de un usuario real, manejando el renderizado dinámico en JavaScript mediante scroll controlado.
* **Extracción de Métricas y Metadatos:** Captura de URLs únicas, captions, hashtags (`#`) y menciones (`@`) del perfil objetivo (por defecto: `@neymarjr`).
* **Análisis de Personalidad Big Five (OCEAN):** Procesamiento de lenguaje sobre los textos acumulados para medir los rasgos:
  * **O**penness (Apertura a la experiencia)
  * **C**onscientiousness (Responsabilidad / Tesón)
  * **E**xtraversion (Extraversión)
  * **A**greeableness (Amabilidad)
  * **N**euroticism (Inestabilidad emocional)
* **Exportación Multiformato:** Generación de datasets en `data/` estructurados en formato **CSV** y **JSON**.

---

## 📁 Estructura del Proyecto

```text
tiktok-scraper/
│
├── data/
│   ├── cookies.json               # Contenedor de cookies de sesión autenticadas
│   ├── neymarjr_full_analysis.json# Dataset completo en JSON (Perfil + Big Five + Posts)
│   └── neymarjr_top10_posts.csv   # Dataset estructurado de los 10 posts procesados
│
├── src/
│   ├── save_cookies.py            # Módulo interactivo para captura de sesión y cookies
│   └── scraper.py                 # Script principal de scraping, extracción y análisis
│
├── .gitignore                     # Filtro de archivos no rastreables
├── README.md                      # Documentación del proyecto
└── requirements.txt               # Dependencias del entorno en Python