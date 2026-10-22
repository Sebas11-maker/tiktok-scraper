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
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        # INYECCIÓN DE COOKIES
        if os.path.exists(cookies_path):
            with open(cookies_path, "r", encoding="utf-8") as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
            print(f"🍪 Se inyectaron exitosamente {len(cookies)} cookies desde '{cookies_path}'.")
        else:
            print("⚠️ Advertencia: No se encontró 'data/cookies.json'. Ejecutando sin cookies inyectadas.")

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

        # 2. Scroll para cargar publicaciones
        await page.evaluate("window.scrollBy(0, 1000)")
        await page.wait_for_timeout(3000)

        # 3. Localizar los 10 primeros posts
        posts_data = []
        all_text_accumulated = bio + " "
        
        video_items = page.locator("[data-e2e='user-post-item']")
        count = await video_items.count()
        limit = min(10, count)

        for i in range(limit):
            item = video_items.nth(i)
            try:
                views = await item.locator("[data-e2e='video-views']").inner_text()
            except Exception:
                views = "N/A"
                
            try:
                link = await item.locator("a").get_attribute("href")
            except Exception:
                link = "N/A"

            try:
                img_alt = await item.locator("img").get_attribute("alt")
                caption = img_alt if img_alt else f"Post numero {i+1}"
            except Exception:
                caption = f"Post numero {i+1}"

            all_text_accumulated += f" {caption}"

            posts_data.append({
                "post_index": i + 1,
                "url": link,
                "vistas_o_likes_feed": views,
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

        # 5. Guardar archivos
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

        print("\n✅ ¡Scraping con Cookies y Análisis Big Five completado!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_scraper())