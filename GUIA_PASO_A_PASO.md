# 🎬 Guía Paso a Paso - Kling AI Video Generator

Esta guía te llevará desde cero hasta generar tu primer video con Kling AI.

---

## 📋 Requisitos Previos

- Python 3.8 o superior instalado
- Una cuenta en Kling AI
- Imágenes que quieras convertir en video

---

## Paso 1: Obtener tus API Keys de Kling AI

### 1.1 Crear cuenta en Kling AI
1. Ve a https://klingai.com
2. Crea una cuenta (si no la tienes)
3. Inicia sesión

### 1.2 Obtener las API Keys
1. Ve al portal de desarrolladores: https://app.klingai.com/global/dev/api-key
2. Verás dos keys importantes:
   - **AccessKey** - Identifica tu cuenta
   - **SecretKey** - Firma tus peticiones (¡mantenla en secreto!)
3. Copia ambas keys (las necesitarás en el siguiente paso)

> **⚠️ IMPORTANTE:** Nunca compartas tu SecretKey. Es como tu contraseña.

---

## Paso 2: Configurar el Proyecto

### 2.1 Clonar o descargar el proyecto
```bash
git clone https://github.com/TU_USUARIO/kling-video-generator.git
cd kling-video-generator
```

### 2.2 Instalar dependencias
```bash
pip install -r requirements.txt
```

Esto instalará:
- `requests` - Para hacer llamadas a la API
- `PyJWT` - Para generar tokens de autenticación
- `Pillow` - Para procesar imágenes
- `python-dotenv` - Para manejar variables de entorno

### 2.3 Configurar tus credenciales
1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Abre `.env` con tu editor favorito y pega tus keys:
   ```env
   KLING_ACCESS_KEY=tu_access_key_aqui
   KLING_SECRET_KEY=tu_secret_key_aqui
   ```

3. Guarda el archivo

### 2.4 Verificar la configuración
```bash
python verificar_configuracion.py
```

Deberías ver:
```
[OK] Archivo .env encontrado
[OK] KLING_ACCESS_KEY configurada
[OK] KLING_SECRET_KEY configurada
[OK] PyJWT instalado
[OK] requests instalado
...
[SUCCESS] TODO CONFIGURADO CORRECTAMENTE!
```

---

## Paso 3: Entender la Autenticación (JWT)

### ¿Qué es un JWT?
JWT (JSON Web Token) es un token de autenticación que prueba que eres tú haciendo la petición.

### ¿Cómo funciona?
1. Tu **AccessKey** dice "soy yo"
2. Tu **SecretKey** firma el token (como una firma digital)
3. El token tiene una expiración (30 minutos)
4. Kling AI verifica que el token sea válido

### Generar un JWT manualmente (opcional)
```bash
python generar_jwt.py
```

Esto te muestra:
- El token JWT generado
- Cuándo expira
- Cómo usarlo en herramientas como Postman

> **Nota:** No necesitas hacer esto manualmente. El script `generar_automatico.py` lo hace automáticamente.

---

## Paso 4: Preparar tus Imágenes

1. Coloca tus imágenes en la carpeta `images/`:
   ```
   images/
   ├── 1.png
   ├── 2.png
   ├── 3.jpg
   └── ...
   ```

2. Formatos soportados: PNG, JPG, JPEG

3. Recomendaciones:
   - **Resolución:** Mínimo 1080x1920 (9:16)
   - **Peso:** Menos de 10MB por imagen
   - **Contenido:** Imágenes claras y bien iluminadas

---

## Paso 5: Generar Videos con `generar_automatico.py`

### ¿Qué hace este script?

`generar_automatico.py` automatiza todo el proceso:

1. **Lee tus credenciales** del archivo `.env`
2. **Genera un JWT token** automáticamente
3. **Lee las imágenes** de la carpeta `images/`
4. **Te pregunta qué generar:**
   - 1 imagen específica
   - Las primeras 6 imágenes (para un reel de 60s)
   - Todas las imágenes
5. **Te pregunta el tipo de movimiento:**
   - Static (movimiento sutil, preserva composición)
   - Zoom In/Out
   - Tilt Up/Down
   - Movimientos aéreos (Forward, Rise, Orbit)
   - Custom (tu propio prompt)
6. **Genera cada video:**
   - Convierte la imagen a base64
   - Envía la petición a Kling AI
   - Espera a que se procese (puede tardar 5-10 minutos)
   - Descarga el video a `outputs/`
7. **Guarda metadata** de cada clip en `outputs/clip_XX_config.txt`

### Ejecutar el generador

```bash
python generar_automatico.py
```

### Ejemplo de sesión interactiva:

```
======================================================================
GENERADOR AUTOMÁTICO DE VIDEOS - KLING AI OFICIAL
IMAGE-TO-VIDEO - Faithful to Original Image
======================================================================

[OK] AccessKey: AerYh4mFpT...
[OK] SecretKey: fK33YR9nbf...
[OK] Cliente API inicializado
[OK] Domain: api-singapore.klingai.com

[OK] Encontradas 9 imagenes

 1. 1.png            - 1080x1920 - 2.34MB
 2. 2.png            - 1080x1920 - 3.12MB
 3. 3.png            - 1080x1920 - 2.87MB
 ...

----------------------------------------------------------------------
OPCIONES:
1. Generar UNA imagen específica
2. Generar las primeras 6 (reel de 60s)
3. Generar TODAS (9 videos)

Selecciona opción (1-3): 1

Número de imagen (1-9): 1

MOVIMIENTOS DE CÁMARA - SUTILES Y NATURALES:

[MOVIMIENTOS BÁSICOS]
1. Static - Movimiento respiratorio sutil, preserva composición
2. Zoom In - Acercamiento suave, revela detalles
3. Zoom Out - Alejamiento suave, revela contexto
4. Tilt Up - Inclinación vertical hacia arriba
5. Tilt Down - Inclinación vertical hacia abajo

[MOVIMIENTOS AÉREOS]
7. Aerial Forward - Movimiento aéreo hacia adelante
8. Aerial Rise - Elevación aérea vertical
9. Aerial Orbit - Rotación orbital suave

6. Custom - Prompt personalizado

Selecciona movimiento (1-9, Enter=Static): 1

======================================================================
CONFIRMACIÓN
======================================================================
Se generarán: 1 video(s)
Clips: 01 - 01
Movimiento: static camera, gentle subtle movement, preserve composition
Tiempo estimado: ~10 minutos

¿Continuar? (s/N): s

======================================================================
GENERACIÓN AUTOMÁTICA INICIADA
======================================================================

[1/1] Procesando 1.png...

Generando video desde: 1.png
Prompt: static camera, gentle subtle movement...
Duración: 10s
Modo: pro
Aspect Ratio: 9:16

Enviando request a: https://api-singapore.klingai.com/v1/videos/image2video
Status: 200

[OK] Video en generacion!
Task ID: abc123def456

Esperando generación (máx 15 min)...
Task ID: abc123def456
Status: processing - 10s transcurridos...
Status: processing - 20s transcurridos...
...
Status: succeed

[OK] Generacion completada!
Video URL: https://...

Descargando video...
[OK] Video descargado: 45.32MB
[OK] Guardado en: C:\Proyectos\Kling\outputs\clip_01.mp4

[OK] Clip 01 completado!

======================================================================
GENERACIÓN COMPLETA
======================================================================
Exitosos:  1
Fallidos:  0
Total:     1

Videos guardados en: ./outputs

[OK] LISTOS PARA CAPCUT!
```

---

## Paso 6: Revisar tus Videos

Los videos generados estarán en:
```
outputs/
├── clip_01.mp4          # Tu video
├── clip_01_config.txt   # Metadata (imagen usada, prompt, etc.)
├── clip_02.mp4
├── clip_02_config.txt
└── ...
```

### Especificaciones de los videos:
- **Modelo:** Kling v2.1 Pro
- **Formato:** MP4
- **Aspect Ratio:** 9:16 (perfecto para Instagram Reels, TikTok, YouTube Shorts)
- **Resolución:** 1080p
- **Duración:** 10 segundos
- **Calidad:** 4K detail, cinematic

---

## 🔧 Troubleshooting (Solución de Problemas)

### Error: "Credenciales no configuradas en .env"
- Verifica que el archivo `.env` existe
- Verifica que tiene las dos keys correctas
- No dejes espacios antes o después del `=`

### Error: "Status 401"
- Tus API keys son incorrectas
- Regenera las keys en el portal de Kling AI
- Verifica que copiaste ambas keys completas

### Error: "PyJWT NO instalado"
```bash
pip install PyJWT
```

### Error: "No se obtuvo task_id"
- La API de Kling puede estar caída (espera unos minutos)
- Verifica tu saldo/créditos en Kling AI
- Revisa que la imagen no sea demasiado grande (< 10MB)

### El video tarda mucho
- Es normal. La generación puede tardar 5-15 minutos
- El script espera automáticamente (máximo 15 minutos)
- Si pasa de 15 minutos, el video puede estar en tu cuenta de Kling AI

### Error: "Timeout esperando generación"
- Inicia sesión en https://klingai.com
- Ve a tu historial
- El video podría estar ahí procesándose

---

## 💡 Tips y Mejores Prácticas

### Para mejores resultados:
1. **Imágenes de calidad:** Usa imágenes bien iluminadas y nítidas
2. **Composición clara:** Kling funciona mejor con sujetos definidos
3. **Movimientos sutiles:** Los movimientos "Static" y "Zoom" suelen dar mejores resultados
4. **Paciencia:** La generación toma tiempo, es normal

### Gestión de créditos:
- Cada video consume créditos de tu cuenta Kling AI
- Genera de uno en uno al principio para probar
- Luego genera en batch las que necesites

### Organización:
- Los clips se numeran automáticamente (clip_01, clip_02...)
- El script detecta el siguiente número disponible
- Puedes borrar clips y volver a generar

---

## 🎥 Flujo Completo Resumido

```
1. Obtener API Keys → klingai.com/dev/api-key
2. Configurar .env → Pegar tus keys
3. Verificar setup → python verificar_configuracion.py
4. Añadir imágenes → Copiar a images/
5. Generar videos → python generar_automatico.py
6. Esperar (5-15 min por video)
7. Encontrar videos en outputs/
8. ¡Editar y publicar!
```

---

## 📚 Archivos del Proyecto Explicados

| Archivo | Propósito |
|---------|-----------|
| `generar_automatico.py` | Script principal - Genera videos automáticamente |
| `kling_api_correcto.py` | Cliente de la API - Maneja comunicación con Kling |
| `generar_jwt.py` | Utilidad - Genera tokens JWT manualmente (opcional) |
| `verificar_configuracion.py` | Diagnóstico - Verifica que todo esté bien configurado |
| `.env` | Configuración - Tus API keys (NO SUBIR A GIT) |
| `requirements.txt` | Dependencias - Librerías Python necesarias |
| `README.md` | Documentación general del proyecto |
| `DOCUMENTACION_KLING.md` | Documentación técnica de la API de Kling |

---

## ❓ Preguntas Frecuentes

**Q: ¿Cuánto cuesta?**  
A: Depende de tu plan en Kling AI. Cada generación consume créditos de tu cuenta.

**Q: ¿Puedo usar esto comercialmente?**  
A: Depende de los términos de servicio de Kling AI. Revisa su documentación.

**Q: ¿Funciona con videos de entrada?**  
A: No, este script es solo para Image-to-Video.

**Q: ¿Puedo cambiar la duración del video?**  
A: Sí, edita el parámetro `duration` en `kling_api_correcto.py` (línea 350).

**Q: ¿Puedo cambiar el aspect ratio?**  
A: Sí, cambia `aspect_ratio="9:16"` por `"16:9"`, `"1:1"`, etc.

---

## 🆘 Soporte

Si tienes problemas:
1. Ejecuta `python verificar_configuracion.py`
2. Revisa el archivo `DOCUMENTACION_KLING.md`
3. Revisa los logs en la terminal
4. Abre un issue en GitHub

---

**¡Listo para generar tus primeros videos! 🎬**

