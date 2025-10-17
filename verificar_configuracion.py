"""
Verificador de Configuración
============================

Verifica que todo esté configurado correctamente.

Author: AI Assistant
Date: October 2025
"""

import os
from pathlib import Path
from dotenv import load_dotenv


def verificar():
    """Verifica configuración completa"""
    
    print("\n" + "="*70)
    print("VERIFICADOR DE CONFIGURACIÓN - KLING AI")
    print("="*70 + "\n")
    
    checks = []
    
    # 1. Check .env file
    env_file = Path(".env")
    if env_file.exists():
        checks.append(("[OK]", "Archivo .env encontrado"))
    else:
        checks.append(("[X]", "Archivo .env NO encontrado"))
        print("ERROR: Necesitas crear archivo .env")
        return False
    
    # 2. Load .env
    load_dotenv()
    
    # 3. Check AccessKey
    access_key = os.getenv("KLING_ACCESS_KEY")
    if access_key:
        checks.append(("[OK]", f"KLING_ACCESS_KEY configurada: {access_key[:10]}..."))
    else:
        checks.append(("[X]", "KLING_ACCESS_KEY NO configurada"))
    
    # 4. Check SecretKey
    secret_key = os.getenv("KLING_SECRET_KEY")
    if secret_key:
        checks.append(("[OK]", f"KLING_SECRET_KEY configurada: {secret_key[:10]}..."))
    else:
        checks.append(("[X]", "KLING_SECRET_KEY NO configurada"))
    
    # 5. Check PyJWT
    try:
        import jwt
        checks.append(("[OK]", "PyJWT instalado"))
    except ImportError:
        checks.append(("[X]", "PyJWT NO instalado"))
    
    # 6. Check requests
    try:
        import requests
        checks.append(("[OK]", "requests instalado"))
    except ImportError:
        checks.append(("[X]", "requests NO instalado"))
    
    # 7. Check images folder
    images_folder = Path("images")
    if images_folder.exists():
        images = list(images_folder.glob("*.png")) + list(images_folder.glob("*.jpg"))
        checks.append(("[OK]", f"Carpeta images con {len(images)} imagenes"))
    else:
        checks.append(("[X]", "Carpeta images NO encontrada"))
    
    # 8. Check outputs folder
    outputs_folder = Path("outputs")
    outputs_folder.mkdir(exist_ok=True)
    checks.append(("[OK]", "Carpeta outputs configurada"))
    
    # 9. Check API client
    try:
        from kling_api_correcto import KlingAPICorrect
        checks.append(("[OK]", "Cliente API correcto disponible"))
    except ImportError:
        checks.append(("[X]", "Cliente API NO disponible"))
    
    # Print results
    print("VERIFICACIÓN DE COMPONENTES:\n")
    
    for symbol, message in checks:
        print(f"{symbol} {message}")
    
    # Test JWT generation
    if access_key and secret_key:
        try:
            from kling_api_correcto import KlingAPICorrect
            client = KlingAPICorrect(access_key, secret_key)
            token = client.generate_jwt_token()
            checks.append(("[OK]", f"JWT token generado: {token[:30]}..."))
            print(f"\n[OK] JWT token generado correctamente")
        except Exception as e:
            checks.append(("[X]", f"Error generando JWT: {str(e)}"))
            print(f"\n[X] Error generando JWT: {str(e)}")
    
    # Summary
    failed = len([c for c in checks if c[0] == "[X]"])
    
    print(f"\n{'='*70}")
    
    if failed == 0:
        print("[SUCCESS] TODO CONFIGURADO CORRECTAMENTE!")
        print(f"{'='*70}\n")
        print("Siguiente paso:")
        print("  python generar_automatico.py\n")
        return True
    else:
        print(f"[WARNING] {failed} PROBLEMAS ENCONTRADOS")
        print(f"{'='*70}\n")
        print("Soluciones:")
        
        if not access_key or not secret_key:
            print("\n1. Obtén tus keys en:")
            print("   https://app.klingai.com/global/dev/api-key")
            print("\n2. Añádelas a tu archivo .env:")
            print("   KLING_ACCESS_KEY=tu_access_key")
            print("   KLING_SECRET_KEY=tu_secret_key")
        
        if "PyJWT" in str(checks):
            print("\n3. Instala PyJWT:")
            print("   pip install PyJWT")
        
        return False


if __name__ == "__main__":
    verificar()

