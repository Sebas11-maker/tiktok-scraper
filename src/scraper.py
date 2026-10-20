import asyncio
import json
import csv
import os
from playwright.async_api import async_playwright

async def run_scraper():
    username = "neymarjr" 
    url = f"https://www.tiktok.com/@{username}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = await context.new_page()
        print(f"Navegando al perfil oficial de @{username}...")
        
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)

        try:
            name_locator = page.locator("[data-e2e='user-title']")
            name = await name_locator.inner_text() if await name_locator.count() > 0 else "No disponible"

            following_locator = page.locator("[data-e2e='following-count']")
            following = await following_locator.inner_text() if await following_locator.count() > 0 else "No disponible"

            followers_locator = page.locator("[data-e2e='followers-count']")
            followers = await followers_locator.inner_text() if await followers_locator.count() > 0 else "No disponible"

            likes_locator = page.locator("[data-e2e='likes-count']")
            likes = await likes_locator.inner_text() if await likes_locator.count() > 0 else "No disponible"

            bio_locator = page.locator("[data-e2e='user-bio']")
            bio = await bio_locator.inner_text() if await bio_locator.count() > 0 else "Sin biografía"

            profile_data = {
                "usuario": f"@{username}",
                "nombre": name,
                "siguiendo": following,
                "seguidores": followers,
                "likes_totales": likes,
                "biografia": bio.strip()
            }

            print("\n==========================================")
            print("      DATOS DEL PERFIL DE NEYMAR JR       ")
            print("==========================================")
            for k, v in profile_data.items():
                print(f"{k.capitalize()}: {v}")
            print("==========================================\n")

            # Crear carpeta data/ si no existe
            os.makedirs("data", exist_ok=True)

            # 1. Guardar en JSON
            json_path = os.path.join("data", f"{username}_profile.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(profile_data, f, ensure_ascii=False, indent=4)
            print(f"✅ Datos guardados en JSON: {json_path}")

            # 2. Guardar en CSV
            csv_path = os.path.join("data", f"{username}_profile.csv")
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=profile_data.keys())
                writer.writeheader()
                writer.writerow(profile_data)
            print(f"✅ Datos guardados en CSV: {csv_path}")

        except Exception as e:
            print("Ocurrió un error durante la extracción:", e)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_scraper())