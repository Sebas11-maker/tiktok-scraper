import asyncio
import json
import csv
import os
import re
from playwright.async_api import async_playwright

# --- FUNCIÓN PARA ANÁLISIS BIG FIVE (OCEAN) BASADO EN TEXTO ---
def analyze_big_five(text_content):
    """
    Analiza el texto acumulado de los posts y asigna una puntuación (0 a 100)
    a cada uno de los 5 rasgos del Big Five (OCEAN).
    """
    text = text_content.lower()
    
    # Dicionarios léxicos de palabras clave por dimensión
    keywords = {
        "Openness": ["arte", "sueño", "crear", "nuevo", "viaje", "mundo", "musica", "futbol", "vida", "magia", "pensar", "foto"],
        "Conscientiousness": ["trabajo", "meta", "entrenar", "foco", "disciplina", "dios", "siempre", "hoy", "preparacion", "exito"],
        "Extraversion": ["familia", "amigos", "fiesta", "equipo", "alegria", "gracias", "show", "vamos", "gente", "feliz", "celebrar"],
        "Agreeableness": ["amor", "paz", "gracias", "union", "apoyo", "juntos", "corazon", "bendicion", "respeto", "humildad"],
        "Neuroticism": ["dificil", "cansado", "problema", "miedo", "triste", "presion", "error", "culpa", "caos", "duda"]
    }
    
    scores = {}
    for trait, words in keywords.items():
        matches = sum(len(re.findall(r'\b' + word + r'\b', text)) for word in words)
        # Base de 50 + ponderación según coincidencias
        score = min(100, 50 + (matches * 8))
        scores[trait] = round(score, 2)
        
    return scores

# --- SCRAPER PRINCIPAL ---
async def run_scraper():
    username = "neymarjr" 
    url = f"https://www.tiktok.com/@{username}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        page = await context.new_page()
        print(f"Navegando al perfil oficial de @{username}...")
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)

        # 1. Extraer datos generales del perfil
        try:
            name = await page.locator("[data-e2e='user-title']").inner_text()
            followers = await page.locator("[data-e2e='followers-count']").inner_text()
            likes_totales = await page.locator("[data-e2e='likes-count']").inner_text()
            bio = await page.locator("[data-e2e='user-bio']").inner_text()
        except Exception:
            name, followers, likes_totales, bio = "N/A", "N/A", "N/A", "N/A"

        # 2. Hacer Scroll para cargar publicaciones en el DOM
        await page.evaluate("window.scrollBy(0, 1000)")
        await page.wait_for_timeout(3000)

        # 3. Localizar los posts/videos del perfil
        posts_data = []
        all_text_accumulated = bio + " "
        
        # Obtenemos los contenedores de los videos
        video_items = page.locator("[data-e2e='user-post-item']")
        count = await video_items.count()
        print(f"Detectados {count} elementos de video. Extrayendo los 10 primeros...")

        limit = min(10, count)
        for i in range(limit):
            item = video_items.nth(i)
            
            # Intento de extracción de vistas / métrica visible en el feed
            try:
                views = await item.locator("[data-e2e='video-views']").inner_text()
            except Exception:
                views = "N/A"
                
            # Intento de extracción del enlace directo del post
            try:
                link = await item.locator("a").get_attribute("href")
            except Exception:
                link = "N/A"

            # Intento de extracción del texto/caption o alt de la imagen de portada
            try:
                img_alt = await item.locator("img").get_attribute("alt")
                caption = img_alt if img_alt else f"Post numero {i+1}"
            except Exception:
                caption = f"Post numero {i+1}"

            all_text_accumulated += f" {caption}"

            post_info = {
                "post_index": i + 1,
                "url": link,
                "vistas_o_likes_feed": views,
                "caption": caption
            }
            posts_data.append(post_info)

        # 4. Generar el Análisis Big Five con el texto recopilado
        big_five_results = analyze_big_five(all_text_accumulated)

        # Estructura final del JSON resultante
        final_dataset = {
            "perfil": {
                "usuario": f"@{username}",
                "nombre": name,
                "seguidores": followers,
                "likes_totales": likes_totales,
                "biografia": bio.strip()
            },
            "big_five_analysis": big_five_results,
            "posts_extraidos": posts_data
        }

        print("\n==========================================")
        print("     ANÁLISIS BIG FIVE (OCEAN) GENERADO   ")
        print("==========================================")
        for trait, score in big_five_results.items():
            print(f"• {trait}: {score}/100")
        print("==========================================\n")

        # 5. Guardar archivos en data/
        os.makedirs("data", exist_ok=True)

        # Exportar JSON completo
        json_path = os.path.join("data", f"{username}_full_analysis.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(final_dataset, f, ensure_ascii=False, indent=4)
        print(f"✅ Análisis completo guardado en JSON: {json_path}")

        # Exportar CSV de los 10 Posts
        csv_path = os.path.join("data", f"{username}_top10_posts.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["post_index", "vistas_o_likes_feed", "url", "caption"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for post in posts_data:
                writer.writerow(post)
        print(f"✅ Métrica de los 10 posts guardada en CSV: {csv_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_scraper())