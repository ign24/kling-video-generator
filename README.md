# Kling AI Video Generator

Generate videos from images using the official Kling AI API.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure credentials
cp .env.example .env
# Edit .env with your API keys

# 3. Generate videos
python generar_automatico.py
```

## Setup

### Get API Keys

1. Go to https://app.klingai.com/global/dev/api-key
2. Copy your `AccessKey` and `SecretKey`
3. Add them to `.env` file:

```env
KLING_ACCESS_KEY=your_access_key_here
KLING_SECRET_KEY=your_secret_key_here
```

### Add Images

Place your images (PNG/JPG) in the `images/` folder.

## Usage

### Generate Videos

```bash
python generar_automatico.py
```

Options:
- Generate 1 specific image
- Generate first 6 images (60s reel)
- Generate all images

### Verify Configuration

```bash
python verificar_configuracion.py
```

### Generate JWT Token (for testing)

```bash
python generar_jwt.py
```

## Video Settings

- **Model:** Kling v2.1 Pro
- **Aspect Ratio:** 9:16 (Instagram Reels)
- **Resolution:** 1080p
- **Duration:** 10 seconds
- **Style:** Faithful to original image with subtle movements

## Project Structure

```
Kling/
├── images/                    # Your input images
├── outputs/                   # Generated videos
├── generar_automatico.py      # Main script
├── kling_api_correcto.py      # API client
├── verificar_configuracion.py # Config checker
├── generar_jwt.py             # JWT generator
├── requirements.txt           # Dependencies
└── README.md
```

## Troubleshooting

**"Credentials not configured"**
- Add `KLING_ACCESS_KEY` and `KLING_SECRET_KEY` to `.env`

**"PyJWT not installed"**
- Run: `pip install -r requirements.txt`

**"Status 401"**
- Check your API keys are correct

## Documentation

See `DOCUMENTACION_KLING.md` for API details.

## License

MIT
