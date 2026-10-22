import asyncio
import json
import csv
import os
import re
from playwright.async_api import async_playwright

def analyze_big_five(text_content):
    text = text_content.lower()
    keywords = {
        "Openness": ["arte", "sueño", "crear", "nuevo", "viaje", "mundo", "musica", "futbol", "vida", "magia", "foto"],
        "Conscientiousness": ["trabajo", "meta", "entrenar", "foco", "disciplina", "dios", "siempre", "hoy", "exito"],
        "Extraversion": ["familia", "amigos", "fiesta", "equipo", "alegria", "gracias", "show", "vamos", "gente", "feliz"],
        "Agreeableness": ["amor", "paz", "gracias", "union", "apoyo", "juntos", "corazon", "bendicion", "respeto"],
        "Neuroticism": ["dificil", "cansado", "problema", "miedo", "triste", "presion", "error", "culpa", "caos"]
    }
    
    scores = {}
    for trait, words in keywords.items():
        matches = sum(len(re.findall(r'\b' + word + r'\b', text)) for word in words)
        score = min(100, 50 + (matches * 8))
        scores[trait] = round(score, 2)
        
    return scores

async def run_scraper():
    username = "neymarjr" 
    url = f"https://www.tiktok.com/@{username}"
    cookies_path = os.path.join("data", "cookies.json")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        # Cargar cookies si existen y no están vacías
        if os.path.exists(cookies_path):
            try:
                with open(cookies_path, "r", encoding="utf-8") as f:
                    cookies = json.load(f)
                if cookies:
                    await context.add_cookies(cookies)
                    print(f"🍪 Se inyectaron {len(cookies)} cookies en la sesión.")
            except Exception as e:
                print("⚠️ No se pudieron cargar las cookies:", e)

        page = await context.new_page()
        print(f"Navegando al perfil oficial de @{username}...")
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("⚠️ Reintentando carga de página...")
            await page.goto(url, timeout=60000)

        await page.wait_for_timeout(4000)

        # 1. Extraer datos del perfil
        try:
            name = await page.locator("[data-e2e='user-title']").inner_text()
            followers = await page.locator("[data-e2e='followers-count']").inner_text()
            likes_totales = await page.locator("[data-e2e='likes-count']").inner_text()
            bio = await page.locator("[data-e2e='user-bio']").inner_text()
        except Exception:
            name, followers, likes_totales, bio = "N/A", "N/A", "N/A", "N/A"

        # 2. Hacer scroll progresivo para forzar la carga de la grilla de videos
        print("Haciendo scroll para cargar publicaciones...")
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 800)")
            await page.wait_for_timeout(2000)

        # 3. Extraer contenedores de videos con selectores combinados
        video_elements = page.locator("[data-e2e='user-post-item'], a[href*='/video/']")
        
        # Esperar a que exista al menos 1 elemento
        try:
            await video_elements.first.wait_for(timeout=5000)
        except Exception:
            pass

        count = await video_elements.count()
        print(f"Buscando elementos de video... Detectados: {count}")

        posts_data = []
        all_text_accumulated = bio + " "
        seen_urls = set()

        for i in range(count):
            if len(posts_data) >= 10:
                break
                
            item = video_elements.nth(i)
            
            # Obtener el enlace del video
            href = await item.get_attribute("href")
            if not href:
                a_tag = item.locator("a")
                if await a_tag.count() > 0:
                    href = await a_tag.get_attribute("href")

            # Evitar enlaces duplicados o vacíos
            if not href or href in seen_urls or "/video/" not in href:
                continue
            
            seen_urls.add(href)

            # Intentar obtener el título o alt de la imagen
            try:
                img = item.locator("img")
                caption = await img.get_attribute("alt") if await img.count() > 0 else ""
            except Exception:
                caption = ""

            if not caption:
                caption = f"Video de Neymar Jr #{len(posts_data) + 1}"

            all_text_accumulated += f" {caption}"

            posts_data.append({
                "post_index": len(posts_data) + 1,
                "vistas_o_likes_feed": "N/A",
                "url": href if href.startswith("http") else f"https://www.tiktok.com{href}",
                "caption": caption
            })

        # 4. Análisis Big Five
        big_five_results = analyze_big_five(all_text_accumulated)

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

        # 5. Guardar archivos en data/
        os.makedirs("data", exist_ok=True)
        
        json_path = os.path.join("data", f"{username}_full_analysis.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(final_dataset, f, ensure_ascii=False, indent=4)

        csv_path = os.path.join("data", f"{username}_top10_posts.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["post_index", "vistas_o_likes_feed", "url", "caption"])
            writer.writeheader()
            for post in posts_data:
                writer.writerow(post)

        print(f"\n✅ ¡Scraping completado! {len(posts_data)} posts guardados en CSV y JSON.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_scraper())