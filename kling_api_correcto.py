"""
Kling AI API Client - Oficial
==============================

Cliente para la API oficial de Kling AI.
Basado en: DOCUMENTACION_KLING.md

API:
  Domain: https://api-singapore.klingai.com
  Auth: JWT tokens (AccessKey + SecretKey)
  Feature: Image to Video
  
JWT Generation:
  import jwt
  headers = {"alg": "HS256", "typ": "JWT"}
  payload = {"iss": access_key, "exp": time+1800, "nbf": time-5}
  token = jwt.encode(payload, secret_key, headers=headers)

Endpoint:
  POST /v1/videos/image2video
  Headers: Authorization: Bearer {jwt_token}
  Payload: {model, image_base64, prompt, mode, duration, aspect_ratio}

Author: AI Assistant
Date: October 2025
"""

import time
import jwt
import requests
import json
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv
import os
from datetime import datetime


class KlingAPICorrect:
    """
    Cliente API correcto para Kling AI
    Basado en documentación oficial
    """
    
    def __init__(self, access_key: str, secret_key: str):
        """
        Inicializar cliente
        
        Args:
            access_key: AccessKey de Kling AI
            secret_key: SecretKey de Kling AI
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_domain = "https://api-singapore.klingai.com"
        
        # Output folder (relative to script location)
        self.outputs_folder = Path(__file__).parent / "outputs"
        self.outputs_folder.mkdir(exist_ok=True)
    
    def generate_jwt_token(self) -> str:
        """
        Genera JWT token según documentación oficial
        
        Returns:
            JWT token string
        """
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        
        payload = {
            "iss": self.access_key,
            "exp": int(time.time()) + 1800,  # 30 minutos
            "nbf": int(time.time()) - 5      # Empieza 5s antes
        }
        
        token = jwt.encode(payload, self.secret_key, headers=headers)
        return token
    
    def get_headers(self) -> Dict[str, str]:
        """
        Genera headers con JWT token
        
        Returns:
            Dictionary con headers
        """
        jwt_token = self.generate_jwt_token()
        
        return {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
    
    def image_to_video(
        self,
        image_path: str,
        prompt: str = "subtle realistic movement, preserve original image composition, natural cinematography, authentic lighting, cinematic realism, 4K detail, faithful to source image",
        duration: int = 10,
        mode: str = "pro",
        aspect_ratio: str = "9:16"
    ) -> Optional[str]:
        """
        Genera video desde imagen usando API oficial
        
        Args:
            image_path: Path a la imagen
            prompt: Prompt para generación
            duration: Duración en segundos (10 por defecto)
            mode: "std" o "pro" (professional tiene mejor calidad)
            aspect_ratio: "9:16" para Instagram Reels
            
        Returns:
            Task ID si exitoso, None si falla
        """
        
        print(f"\nGenerando video desde: {Path(image_path).name}")
        print(f"Prompt: {prompt}")
        print(f"Duración: {duration}s")
        print(f"Modo: {mode}")
        print(f"Aspect Ratio: {aspect_ratio}")
        
        # Read and encode image
        with open(image_path, 'rb') as f:
            import base64
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Prepare request
        url = f"{self.api_domain}/v1/videos/image2video"
        headers = self.get_headers()
        
        payload = {
            "model_name": "kling-v2-1",
            "image": image_data,
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, distorted, artifacts",
            "cfg_scale": 0.5,
            "mode": mode,
            "duration": duration,
            "aspect_ratio": aspect_ratio
        }
        
        print(f"\nEnviando request a: {url}")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract task ID
                task_id = result.get("data", {}).get("task_id")
                
                if task_id:
                    print(f"\n[OK] Video en generacion!")
                    print(f"Task ID: {task_id}")
                    return task_id
                else:
                    print(f"ERROR: No se obtuvo task_id")
                    print(f"Response: {json.dumps(result, indent=2)}")
                    return None
            else:
                print(f"ERROR: Status {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return None
    
    def check_task_status(self, task_id: str) -> Dict:
        """
        Verifica estado de la tarea
        
        Args:
            task_id: ID de la tarea
            
        Returns:
            Dictionary con estado y resultado
        """
        # Try different endpoints to find the correct one
        endpoints = [
            f"/v1/videos/image2video/{task_id}",
            f"/v1/tasks/{task_id}",
            f"/v1/videos/{task_id}"
        ]
        
        headers = self.get_headers()
        
        for endpoint in endpoints:
            url = f"{self.api_domain}{endpoint}"
            
            try:
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    continue  # Try next endpoint
                else:
                    return {"error": f"Status {response.status_code}: {response.text}"}
                    
            except Exception as e:
                continue
        
        # If all failed, return error
        return {"error": f"No valid endpoint found for task {task_id}"}
    
    def wait_for_completion(self, task_id: str, max_wait_minutes: int = 15) -> Optional[str]:
        """
        Espera a que el video se complete
        
        Args:
            task_id: ID de la tarea
            max_wait_minutes: Tiempo máximo de espera en minutos
            
        Returns:
            URL del video si exitoso, None si falla
        """
        max_attempts = max_wait_minutes * 6  # Check every 10 seconds
        attempt = 0
        
        print(f"\nEsperando generación (máx {max_wait_minutes} min)...")
        print(f"Task ID: {task_id}")
        
        while attempt < max_attempts:
            result = self.check_task_status(task_id)
            
            if "error" in result:
                if attempt == 0:
                    # First attempt failed, might need to wait for task to be processed
                    print(f"Esperando que la tarea se registre...")
                    time.sleep(30)
                    attempt += 1
                    continue
                else:
                    print(f"Error verificando estado: {result['error']}")
                    return None
            
            # Extract status from response
            code = result.get("code")
            data = result.get("data", {})
            status = data.get("task_status")
            
            print(f"Response code: {code}, Status: {status}")
            
            if status == "succeed":
                # Extract video URL
                task_result = data.get("task_result", {})
                videos = task_result.get("videos", [])
                
                if videos and len(videos) > 0:
                    video_url = videos[0].get("url")
                    
                    if video_url:
                        print(f"\n[OK] Generacion completada!")
                        print(f"Video URL: {video_url[:50]}...")
                        return video_url
                
                print("ERROR: No se encontró URL del video en la respuesta")
                print(f"Respuesta completa: {json.dumps(result, indent=2)}")
                return None
            
            elif status == "failed":
                print(f"ERROR: Generación falló")
                print(f"Resultado: {json.dumps(result, indent=2)}")
                return None
            
            else:
                # Still processing (submitted, processing, etc.)
                attempt += 1
                elapsed = attempt * 10
                print(f"Status: {status} - {elapsed}s transcurridos...")
                time.sleep(10)
        
        print("ERROR: Timeout esperando generación")
        return None
    
    def download_video(self, video_url: str, output_path: str) -> bool:
        """
        Descarga video
        
        Args:
            video_url: URL del video
            output_path: Path donde guardar
            
        Returns:
            True si exitoso
        """
        try:
            print(f"\nDescargando video...")
            response = requests.get(video_url, timeout=300)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                size_mb = Path(output_path).stat().st_size / (1024 * 1024)
                print(f"[OK] Video descargado: {size_mb:.2f}MB")
                print(f"[OK] Guardado en: {output_path}")
                
                return True
            else:
                print(f"ERROR: Download failed - Status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"ERROR descargando: {str(e)}")
            return False
    
    def generate_video_complete(
        self,
        image_path: str,
        clip_number: int,
        custom_prompt: str = ""
    ) -> Optional[Path]:
        """
        Proceso completo: generar y descargar video
        
        Args:
            image_path: Path a imagen
            clip_number: Número de clip
            custom_prompt: Personalización del prompt
            
        Returns:
            Path del video generado o None
        """
        # Build prompt
        base_prompt = "subtle realistic movement, preserve original image composition, natural cinematography, authentic lighting, cinematic realism, 4K detail, faithful to source image"
        if custom_prompt:
            full_prompt = f"{custom_prompt}, {base_prompt}"
        else:
            full_prompt = base_prompt
        
        # Output file
        output_file = self.outputs_folder / f"clip_{clip_number:02d}.mp4"
        
        print(f"\n{'='*70}")
        print(f"GENERANDO CLIP {clip_number:02d}")
        print(f"{'='*70}")
        
        # Generate
        task_id = self.image_to_video(
            image_path=image_path,
            prompt=full_prompt,
            duration=10,
            mode="pro",
            aspect_ratio="9:16"
        )
        
        if not task_id:
            return None
        
        # Wait for completion
        video_url = self.wait_for_completion(task_id)
        
        if not video_url:
            return None
        
        # Download
        if self.download_video(video_url, str(output_file)):
            # Save config
            self._save_config(clip_number, Path(image_path).name, full_prompt, task_id)
            return output_file
        else:
            return None
    
    def _save_config(self, clip_number, image_name, prompt, task_id):
        """Guarda configuración del clip"""
        config_file = self.outputs_folder / f"clip_{clip_number:02d}_config.txt"
        
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(f"Clip {clip_number:02d}\n")
            f.write("="*70 + "\n\n")
            f.write(f"Imagen: {image_name}\n")
            f.write(f"Task ID: {task_id}\n")
            f.write(f"Prompt: {prompt}\n\n")
            f.write(f"CONFIGURACIÓN:\n")
            f.write(f"  - API: api-singapore.klingai.com (oficial)\n")
            f.write(f"  - Modelo: Kling v2.1 Image2Video\n")
            f.write(f"  - Aspect Ratio: 9:16\n")
            f.write(f"  - Resolución: 1080p\n")
            f.write(f"  - Duración: 5 segundos\n")
            f.write(f"  - Estilo: Premium Cinematic\n")


def main():
    """Test del cliente"""
    
    print("\n" + "="*70)
    print("TEST KLING AI API CORRECTO")
    print("="*70 + "\n")
    
    load_dotenv()
    
    access_key = os.getenv("KLING_ACCESS_KEY")
    secret_key = os.getenv("KLING_SECRET_KEY")
    
    if not access_key or not secret_key:
        print("ERROR: Faltan credenciales en .env")
        print("\nNecesitas añadir a .env:")
        print("KLING_ACCESS_KEY=tu_access_key")
        print("KLING_SECRET_KEY=tu_secret_key")
        print("\nObtén tus keys en:")
        print("https://app.klingai.com/global/dev/api-key")
        return
    
    print(f"AccessKey: {access_key[:10]}...")
    print(f"SecretKey: {secret_key[:10]}...")
    
    # Initialize client
    client = KlingAPICorrect(access_key, secret_key)
    
    # Generate JWT token
    jwt_token = client.generate_jwt_token()
    print(f"\nJWT Token generado: {jwt_token[:50]}...")
    
    print("\n[OK] Cliente inicializado correctamente")
    print("[OK] Listo para generar videos")


if __name__ == "__main__":
    main()

