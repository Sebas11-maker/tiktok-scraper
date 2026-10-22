import asyncio
import json
import os
from playwright.async_api import async_playwright

async def save_tiktok_cookies():
    async with async_playwright() as p:
        # Iniciamos Chromium desactivando las banderas de automatización para reducir la detección
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport=None
        )
        
        page = await context.new_page()

        print("Navegando a la página de Login con QR de TikTok...")
        await page.goto("https://www.tiktok.com/login/qrcode", wait_until="domcontentloaded")
        
        print("\n===========================================================")
        print("INSTRUCCIONES:")
        print("1. Escanea el CÓDIGO QR desde la App de TikTok de tu celular.")
        print("2. Una vez que hayas iniciado sesión y veas tu feed/inicio,")
        print("   haz clic en esta terminal y presiona ENTER.")
        print("===========================================================\n")

        # Espera interactiva
        await asyncio.get_event_loop().run_in_executor(None, input, "👉 Presiona ENTER aquí cuando hayas escaneado el QR... ")

        # Extraemos las cookies
        cookies = await context.cookies()

        os.makedirs("data", exist_ok=True)
        cookies_path = os.path.join("data", "cookies.json")
        
        with open(cookies_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=4)

        print(f"\n✅ ¡Sesión guardada exitosamente! Se registraron {len(cookies)} cookies.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(save_tiktok_cookies())