# TikTok Profile Scraper (Playwright & Python)

Este proyecto es un scraper automatizado desarrollado en Python utilizando **Playwright** para extraer métricas y datos públicos de cuentas de TikTok sin la necesidad de extensiones de navegador ni APIs de terceros.

## 🛠️ Tecnologías Utilizadas

* **Python 3.x**: Lenguaje principal de desarrollo.
* **Playwright**: Automatización e interacción con el motor del navegador (Chromium).
* **JSON / CSV**: Formatos de exportación de los datos extraídos.

## 📁 Estructura del Proyecto

```text
tiktok-scraper/
│
├── data/                    # Archivos generados (.json y .csv)
│   ├── neymarjr_profile.csv
│   └── neymarjr_profile.json
├── src/
│   └── scraper.py           # Código fuente principal del scraper
├── .gitignore               # Archivos excluidos del repositorio
├── README.md                # Documentación del proyecto
└── requirements.txt         # Dependencias del proyecto