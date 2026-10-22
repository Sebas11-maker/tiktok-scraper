import asyncio
import json
import csv
import os
import re
from playwright.async_api import async_playwright

def analyze_big_five(text_content):
    """Calcula la puntuación del modelo Big Five (OCEAN) a partir del texto acumulado."""
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

def extract_hashtags_and_mentions(text):
    """Extrae listas de hashtags (#) y menciones (@) de un texto."""
    hashtags = re.findall(r'#\w+', text)
    mentions = re.findall(r'@\w+', text)
    return hashtags, mentions

async def run_scraper():
    username = "neymarjr" 
    url = f"https://www.tiktok.com/@{username}"
    cookies_path = os.path.join("data", "cookies.json")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        # Inyección de Cookies
        if os.path.exists(cookies_path):
            try:
                with open(cookies_path, "r", encoding="utf-8") as f:
                    cookies = json.load(f)
                if cookies:
                    cleaned_cookies = []
                    for c in cookies:
                        c_copy = c.copy()
                        if "sameSite" in c_copy and c_copy["sameSite"] not in ["Strict", "Lax", "None"]:
                            c_copy["sameSite"] = "Lax"
                        cleaned_cookies.append(c_copy)
                    
                    await context.add_cookies(cleaned_cookies)
                    print(f"🍪 Se inyectaron exitosamente {len(cleaned_cookies)} cookies en la sesión.")
            except Exception as e:
                print("⚠️ Error al cargar las cookies:", e)

        page = await context.new_page()
        print(f"Navegando al perfil oficial de @{username}...")
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception:
            await page.goto(url, timeout=60000)

        await page.wait_for_timeout(4000)

        # 1. Datos generales del perfil
        try:
            name = await page.locator("[data-e2e='user-title']").inner_text()
            followers = await page.locator("[data-e2e='followers-count']").inner_text()
            likes_totales = await page.locator("[data-e2e='likes-count']").inner_text()
            bio = await page.locator("[data-e2e='user-bio']").inner_text()
        except Exception:
            name, followers, likes_totales, bio = "N/A", "N/A", "N/A", "N/A"

        # 2. Scroll interactivo para renderizar la grilla
        print("Realizando scroll para cargar publicaciones...")
        for _ in range(4):
            await page.mouse.wheel(0, 600)
            await page.wait_for_timeout(1500)

        # 3. Captura de los enlaces de videos
        links = page.locator("a[href*='/video/']")
        count = await links.count()
        print(f"Buscando elementos de video... Detectados: {count}")

        posts_data = []
        all_text_accumulated = bio + " "
        all_hashtags = []
        all_mentions = []
        seen_urls = set()

        for i in range(count):
            if len(posts_data) >= 10:
                break
                
            item = links.nth(i)
            href = await item.get_attribute("href")

            if not href or "/video/" not in href:
                continue
            
            full_url = href if href.startswith("http") else f"https://www.tiktok.com{href}"
            
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            # Extraer descripción si existe
            caption = ""
            try:
                img = item.locator("img")
                if await img.count() > 0:
                    caption = await img.get_attribute("alt")
            except Exception:
                caption = ""

            if not caption:
                caption = f"Video de Neymar Jr #{len(posts_data) + 1}"

            hashtags, mentions = extract_hashtags_and_mentions(caption)
            all_hashtags.extend(hashtags)
            all_mentions.extend(mentions)
            all_text_accumulated += f" {caption}"

            posts_data.append({
                "post_index": len(posts_data) + 1,
                "vistas_o_likes_feed": "N/A",
                "url": full_url,
                "caption": caption,
                "hashtags": ", ".join(hashtags) if hashtags else "Ninguno",
                "menciones": ", ".join(mentions) if mentions else "Ninguno"
            })

        # 4. Análisis psicométrico Big Five
        big_five_results = analyze_big_five(all_text_accumulated)

        final_dataset = {
            "perfil": {
                "usuario": f"@{username}",
                "nombre": name,
                "seguidores": followers,
                "likes_totales": likes_totales,
                "biografia": bio.strip()
            },
            "metricas_avanzadas": {
                "total_posts_analizados": len(posts_data),
                "top_hashtags": list(set(all_hashtags)),
                "top_menciones": list(set(all_mentions))
            },
            "big_five_analysis": big_five_results,
            "posts_extraidos": posts_data
        }

        # 5. Exportar resultados en data/
        os.makedirs("data", exist_ok=True)
        
        json_path = os.path.join("data", f"{username}_full_analysis.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(final_dataset, f, ensure_ascii=False, indent=4)

        csv_path = os.path.join("data", f"{username}_top10_posts.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["post_index", "vistas_o_likes_feed", "url", "caption", "hashtags", "menciones"])
            writer.writeheader()
            for post in posts_data:
                writer.writerow(post)

        print(f"\n==========================================")
        print(f"✅ Scraping y Análisis completados exitosamente.")
        print(f"📊 Posts procesados: {len(posts_data)}")
        print(f"==========================================\n")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_scraper())