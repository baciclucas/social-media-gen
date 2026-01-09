"""
Configurações e constantes do sistema gerador de criativos.
"""
import os
from typing import Dict, Tuple

# Diretórios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
EXAMPLES_DIR = os.path.join(ASSETS_DIR, "examples")

# Dimensões dos formatos (largura, altura)
FORMATS: Dict[str, Tuple[int, int]] = {
    "instagram_feed": (1080, 1080),
    "instagram_story": (1080, 1920),
    "facebook_ad": (1200, 628),
    "web_banner": (1200, 400),
}

# Limites de caracteres para textos
TEXT_LIMITS: Dict[str, Dict[str, int]] = {
    "instagram_feed": {"title": 40, "subtitle": 60},
    "instagram_story": {"title": 25, "subtitle": 60},
    "facebook_ad": {"title": 40, "subtitle": 60},
    "web_banner": {"title": 40, "subtitle": 60},
}

# Configurações de fontes
DEFAULT_FONT = "Arial"
FONT_SIZES: Dict[str, Dict[str, int]] = {
    "instagram_feed": {
        "title": 72,
        "subtitle": 36,
        "price": 96,
        "cta": 48,
        "brand": 28,
    },
    "instagram_story": {
        "title": 80,
        "subtitle": 40,
        "price": 110,
        "cta": 56,
        "brand": 32,
    },
    "facebook_ad": {
        "title": 64,
        "subtitle": 32,
        "price": 84,
        "cta": 44,
        "brand": 24,
    },
    "web_banner": {
        "title": 56,
        "subtitle": 28,
        "price": 72,
        "cta": 40,
        "brand": 22,
    },
}

# Configurações de cores
COLOR_DEFAULTS = {
    "text_dark": "#2D3748",
    "text_light": "#FFFFFF",
    "overlay_dark": "#00000080",  # 50% transparência
    "overlay_light": "#FFFFFF80",
    "shadow": "#00000040",
}

# Configurações de API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"

# Configurações de processamento
MAX_PROCESSING_TIME = 60  # segundos
SUPPORTED_IMAGE_FORMATS = [".png", ".jpg", ".jpeg", ".webp"]
IMAGE_QUALITY = 95  # Qualidade JPEG/PNG

# Prompts para geração de copy
COPY_GENERATION_PROMPTS = {
    "title": """Crie um texto persuasivo curto para um anúncio de {product_name}.
Descrição: {description}
Tipo de campanha: {campaign_type}
{price_info}

Requisitos:
- Máximo {char_limit} caracteres
- Tom: convencedor, amigável, direto
- {urgency_instruction}
- Destaque o benefício principal
- Retorne apenas o texto, sem aspas ou formatação adicional""",

    "subtitle": """Crie uma frase complementar curta para o produto {product_name}.
Descrição: {description}
Tipo de campanha: {campaign_type}

Requisitos:
- Máximo {char_limit} caracteres
- Tom: informativo e amigável
- Destaque uma característica ou benefício específico
- Retorne apenas o texto, sem aspas ou formatação adicional""",
}

# Configurações de template
TEMPLATE_CONFIGS = {
    "minimalist": {
        "product_scale": 0.6,  # 60% da área disponível
        "background_color": "light",
        "shadow_enabled": True,
        "border_enabled": False,
    },
    "vibrant": {
        "product_scale": 0.7,
        "background_color": "brand",
        "shadow_enabled": True,
        "border_enabled": True,
    },
}

# Margens e padding (em pixels)
PADDING = {
    "instagram_feed": {"outer": 60, "inner": 40},
    "instagram_story": {"outer": 80, "inner": 50},
    "facebook_ad": {"outer": 50, "inner": 35},
    "web_banner": {"outer": 40, "inner": 30},
}

# Configurações de logo
LOGO_CONFIG = {
    "max_width_ratio": 0.25,  # 25% da largura da imagem
    "max_height_ratio": 0.15,  # 15% da altura da imagem
    "position": "top_left",  # ou "top_right", "bottom_left", "bottom_right"
}

# Configurações de produto
PRODUCT_CONFIG = {
    "remove_background": True,  # Se True, tenta remover background
    "add_shadow": True,
    "shadow_offset": (10, 10),
    "shadow_blur": 20,
}

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
