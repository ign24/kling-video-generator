"""
Generador Automático de Videos - Kling AI
==========================================

GENERA VIDEOS AUTOMÁTICAMENTE usando la API oficial de Kling AI.
Convierte cualquier imagen en video con movimientos sutiles y naturales.

Configuración necesaria en .env:
  KLING_ACCESS_KEY=tu_access_key
  KLING_SECRET_KEY=tu_secret_key

Obtener keys: https://app.klingai.com/global/dev/api-key

Uso:
  python generar_automatico.py

Selecciona:
  - 1 imagen específica
  - 6 imágenes (reel 60s)
  - Todas las imágenes

Output: ./outputs/clip_XX.mp4

Configuración de videos:
  - Modelo: Kling v2.1 Pro (Image2Video)
  - Aspect Ratio: 9:16 (Instagram Reels)
  - Resolución: 1080p - 4K Detail
  - Duración: 10 segundos
  - Movimientos Básicos: Static, Zoom In/Out, Tilt Up/Down
  - Movimientos Aéreos: Aerial Forward, Aerial Rise, Aerial Orbit
  - Estilo: Fiel a la imagen original, movimientos sutiles y naturales
  - Prompt: Minimalista, preserva composición original

Author: AI Assistant
Date: October 2025
"""

import os
import sys
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
from kling_api_correcto import KlingAPICorrect


def list_images():
    """Lista imágenes disponibles"""
    images_folder = Path("images")
    if not images_folder.exists():
        print("ERROR: Carpeta 'images' no encontrada!")
        return []

    images = list(images_folder.glob("*.png")) + list(images_folder.glob("*.jpg"))
    images.sort(key=lambda x: x.name)

    return images


def get_next_clip_number():
    """Obtiene siguiente número de clip disponible"""
    outputs_folder = Path(__file__).parent / "outputs"
    outputs_folder.mkdir(exist_ok=True)

    existing = list(outputs_folder.glob("clip_*.mp4"))
    if not existing:
        return 1

    # Extraer números de los clips existentes
    numbers = []
    for clip in existing:
        try:
            num = int(clip.stem.split('_')[1])
            numbers.append(num)
        except (IndexError, ValueError):
            continue

    # Retornar el número más alto + 1
    return max(numbers) + 1 if numbers else 1


def main():
    """Función principal"""

    print("\n" + "="*70)
    print("GENERADOR AUTOMÁTICO DE VIDEOS - KLING AI OFICIAL")
    print("IMAGE-TO-VIDEO - Faithful to Original Image")
    print("Kling v2.1 Pro - 9:16 - 10s - 4K Detail")
    print("Movimientos: Static | Zoom | Tilt | Aerial Forward | Rise | Orbit")
    print("="*70 + "\n")

    # Load credentials from .env
    load_dotenv()

    access_key = os.getenv("KLING_ACCESS_KEY")
    secret_key = os.getenv("KLING_SECRET_KEY")

    if not access_key or not secret_key:
        print("ERROR: Credenciales no configuradas en .env!")
        print("\nDebes añadir a tu archivo .env:")
        print("KLING_ACCESS_KEY=tu_access_key")
        print("KLING_SECRET_KEY=tu_secret_key")
        print("\nObtén tus keys en:")
        print("https://app.klingai.com/global/dev/api-key")
        print("\nNOTA: Necesitas AMBAS keys (AccessKey y SecretKey)")
        return

    print(f"[OK] AccessKey: {access_key[:10]}...")
    print(f"[OK] SecretKey: {secret_key[:10]}...")

    # Initialize client
    client = KlingAPICorrect(access_key, secret_key)
    print(f"[OK] Cliente API inicializado")
    print(f"[OK] Domain: api-singapore.klingai.com")

    # List images
    images = list_images()

    if not images:
        return

    print(f"\n[OK] Encontradas {len(images)} imagenes\n")

    # Show images
    for i, img_path in enumerate(images, 1):
        img = Image.open(img_path)
        w, h = img.size
        size_mb = img_path.stat().st_size / (1024 * 1024)
        print(f"{i:2d}. {img_path.name:<15} - {w}x{h} - {size_mb:.2f}MB")

    print("\n" + "-"*70)
    print("OPCIONES:")
    print("1. Generar UNA imagen específica")
    print("2. Generar las primeras 6 (reel de 60s)")
    print("3. Generar TODAS (25 videos)")

    option = input("\nSelecciona opción (1-3): ").strip()

    selected_images = []

    if option == "1":
        img_num = int(input(f"\nNúmero de imagen (1-{len(images)}): ").strip())
        if img_num < 1 or img_num > len(images):
            print("ERROR: Número inválido")
            return
        selected_images = [images[img_num - 1]]

    elif option == "2":
        selected_images = images[:6]

    elif option == "3":
        selected_images = images

    else:
        print("ERROR: Opción inválida")
        return

    # Camera movement selection
    print(f"\nMOVIMIENTOS DE CÁMARA - SUTILES Y NATURALES:")
    print("\n[MOVIMIENTOS BÁSICOS]")
    print("1. Static - Movimiento respiratorio sutil, preserva composición")
    print("2. Zoom In - Acercamiento suave, revela detalles")
    print("3. Zoom Out - Alejamiento suave, revela contexto")
    print("4. Tilt Up - Inclinación vertical hacia arriba")
    print("5. Tilt Down - Inclinación vertical hacia abajo")
    print("\n[MOVIMIENTOS AÉREOS]")
    print("7. Aerial Forward - Movimiento aéreo hacia adelante")
    print("8. Aerial Rise - Elevación aérea vertical")
    print("9. Aerial Orbit - Rotación orbital suave")
    print("\n6. Custom - Prompt personalizado")

    movement_option = input("\nSelecciona movimiento (1-9, Enter=Static): ").strip() or "1"

    movements = {
        "1": "static camera, gentle subtle movement, preserve composition, natural breathing effect",
        "2": "slow subtle zoom in, gentle approach, reveal details, smooth natural movement",
        "3": "slow subtle zoom out, gentle pullback, reveal context, smooth expansive view",
        "4": "slow subtle tilt up, gentle vertical rise, reveal upper elements, natural upward flow",
        "5": "slow subtle tilt down, gentle vertical descent, reveal lower elements, natural downward flow",
        "6": "",
        "7": "subtle aerial movement forward, gentle floating effect, smooth forward glide, natural aerial perspective",
        "8": "subtle aerial rise, gentle vertical lift, smooth elevation, natural ascending movement",
        "9": "subtle orbital movement, gentle circular rotation, smooth panoramic reveal, natural rotating perspective"
    }

    if movement_option == "6":
        custom = input("Prompt personalizado: ").strip()
    else:
        custom = movements.get(movement_option, movements["1"])

    # Confirm
    next_clip = get_next_clip_number()
    last_clip = next_clip + len(selected_images) - 1

    print(f"\n{'='*70}")
    print("CONFIRMACIÓN")
    print(f"{'='*70}")
    print(f"Se generarán: {len(selected_images)} video(s)")
    print(f"Clips: {next_clip:02d} - {last_clip:02d}")
    print(f"Movimiento: {custom}")
    print(f"Tiempo estimado: ~{len(selected_images) * 10} minutos")

    confirm = input("\n¿Continuar? (s/N): ").strip().lower()
    if confirm != 's':
        print("Cancelado.")
        return

    # Generate videos
    print(f"\n{'='*70}")
    print("GENERACIÓN AUTOMÁTICA INICIADA")
    print(f"{'='*70}")

    successful = 0
    failed = 0

    for i, image_path in enumerate(selected_images):
        clip_number = next_clip + i

        print(f"\n[{i+1}/{len(selected_images)}] Procesando {Path(image_path).name}...")

        result = client.generate_video_complete(
            str(image_path),
            clip_number,
            custom
        )

        if result:
            successful += 1
            print(f"\n[OK] Clip {clip_number:02d} completado!")
        else:
            failed += 1
            print(f"\n[X] Clip {clip_number:02d} fallo")

        # Delay entre videos
        if i < len(selected_images) - 1:
            print("\nEsperando 15 segundos antes del siguiente...")
            import time
            time.sleep(15)

    # Summary
    print(f"\n{'='*70}")
    print("GENERACIÓN COMPLETA")
    print(f"{'='*70}")
    print(f"Exitosos:  {successful}")
    print(f"Fallidos:  {failed}")
    print(f"Total:     {len(selected_images)}")
    print(f"\nVideos guardados en: ./outputs")
    print("\n[OK] LISTOS PARA CAPCUT!")


if __name__ == "__main__":
    main()

