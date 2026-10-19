import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def get_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
    if not api_key or api_key.startswith("tu_"):
        raise ValueError(
            "No se encontró una API key válida. Configura GEMINI_API_KEY o API_KEY "
            "en el archivo .env en la raíz del proyecto."
        )
    return api_key


def main() -> None:
    try:
        api_key = get_api_key()
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-3.8-flash")
        response = model.generate_content(
            "Responde con una frase breve confirmando que la autenticación con Gemini funciona."
        )

        print(response.text)
    except Exception as exc:
        print(f"Error al autenticar con Gemini: {exc}")
        raise


if __name__ == "__main__":
    main()
