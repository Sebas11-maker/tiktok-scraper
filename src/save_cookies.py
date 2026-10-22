import asyncio
import json
import os
from playwright.async_api import async_playwright

async def save_tiktok_cookies():
    async with async_playwright() as p:
        # Abrimos el navegador visible para interactuar
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("Navegando a TikTok para capturar cookies...")
        await page.goto("https://www.tiktok.com", wait_until="domcontentloaded")
        
        print("\n-----------------------------------------------------------")
        print("AHORA: Si deseas iniciar sesión o aceptar cookies en la pantalla,")
        print("hazlo manualmente en la ventana del navegador que se abrió.")
        print("Tienes 30 segundos antes de que se guarden las cookies.")
        print("-----------------------------------------------------------\n")

        # Esperamos 30 segundos para que interactúes con la página si lo deseas
        await page.wait_for_timeout(30000)

        # Extraemos las cookies del contexto
        cookies = await context.cookies()

        # Guardamos las cookies en data/cookies.json
        os.makedirs("data", exist_ok=True)
        cookies_path = os.path.join("data", "cookies.json")
        
        with open(cookies_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=4)

        print(f"✅ ¡Cookies guardadas exitosamente en {cookies_path}!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(save_tiktok_cookies())