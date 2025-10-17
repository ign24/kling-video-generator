"""
Generador de JWT Token para Kling AI
====================================

Genera un JWT token válido para usar en la consola de Kling AI.

Uso:
  python generar_jwt.py

El token es válido por 30 minutos.

Author: AI Assistant
Date: October 2025
"""

import time
import jwt
from dotenv import load_dotenv
import os


def generar_jwt():
    """Genera JWT token para Kling AI"""
    
    # Load keys from .env
    load_dotenv()
    
    access_key = os.getenv("KLING_ACCESS_KEY")
    secret_key = os.getenv("KLING_SECRET_KEY")
    
    if not access_key or not secret_key:
        print("ERROR: Keys no configuradas en .env")
        print("\nDebes tener en .env:")
        print("KLING_ACCESS_KEY=tu_access_key")
        print("KLING_SECRET_KEY=tu_secret_key")
        return None
    
    # Generate JWT token según documentación oficial
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    payload = {
        "iss": access_key,
        "exp": int(time.time()) + 1800,  # Válido por 30 minutos
        "nbf": int(time.time()) - 5       # Empieza 5s antes
    }
    
    token = jwt.encode(payload, secret_key, headers=headers)
    
    return token


def main():
    print("\n" + "="*70)
    print("GENERADOR DE JWT TOKEN - KLING AI")
    print("="*70 + "\n")
    
    token = generar_jwt()
    
    if token:
        print("[OK] JWT Token generado exitosamente\n")
        print("="*70)
        print("TU JWT TOKEN (válido 30 minutos):")
        print("="*70)
        print(f"\n{token}\n")
        print("="*70)
        
        print("\nUSO EN CONSOLA DE KLING:")
        print("\n1. En tu terminal/Postman/Insomnia:")
        print("\n   Authorization: Bearer " + token[:50] + "...")
        print("\n2. Domain: https://api-singapore.klingai.com")
        print("\n3. Endpoint: POST /v1/videos/image2video")
        
        print("\n" + "="*70)
        print("INFORMACIÓN:")
        print("="*70)
        print(f"AccessKey: {os.getenv('KLING_ACCESS_KEY')[:10]}...")
        print(f"SecretKey: {os.getenv('KLING_SECRET_KEY')[:10]}...")
        print(f"Expira en: 30 minutos")
        print(f"Tiempo actual: {int(time.time())}")
        print(f"Expira en timestamp: {int(time.time()) + 1800}")
    else:
        print("[X] No se pudo generar el token")
        print("Configura tus keys en .env")


if __name__ == "__main__":
    main()

