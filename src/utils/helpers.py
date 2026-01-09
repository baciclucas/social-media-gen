"""
Funções auxiliares para o sistema gerador de criativos.
"""
import re
import logging
from typing import Tuple, Optional
from datetime import datetime
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Converte cor hexadecimal para RGB.

    Args:
        hex_color: String com cor em formato hexadecimal (#RRGGBB ou RRGGBB)

    Returns:
        Tupla (R, G, B) com valores de 0-255

    Raises:
        ValueError: Se o formato hexadecimal for inválido
    """
    # Remove o # se presente
    hex_color = hex_color.lstrip('#')

    # Valida o formato
    if not re.match(r'^[0-9A-Fa-f]{6}$', hex_color):
        raise ValueError(f"Formato hexadecimal inválido: {hex_color}")

    # Converte para RGB
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """
    Converte RGB para hexadecimal.

    Args:
        rgb: Tupla (R, G, B) com valores de 0-255

    Returns:
        String em formato hexadecimal #RRGGBB
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def calculate_luminance(rgb: Tuple[int, int, int]) -> float:
    """
    Calcula a luminância relativa de uma cor RGB.
    Útil para determinar se texto deve ser claro ou escuro.

    Args:
        rgb: Tupla (R, G, B) com valores de 0-255

    Returns:
        Valor de luminância entre 0 (preto) e 1 (branco)
    """
    # Converte para valores 0-1
    r, g, b = [x / 255.0 for x in rgb]

    # Aplica correção gamma
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

    # Calcula luminância
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_text_color(background_rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Determina se texto deve ser claro ou escuro baseado no background.

    Args:
        background_rgb: Cor de fundo em RGB

    Returns:
        Cor de texto em RGB (preto ou branco)
    """
    luminance = calculate_luminance(background_rgb)
    # Se luminância > 0.5, usar texto escuro, senão usar texto claro
    return (45, 55, 72) if luminance > 0.5 else (255, 255, 255)


def validate_image_path(path: str) -> bool:
    """
    Valida se o caminho da imagem existe e tem formato suportado.

    Args:
        path: Caminho para o arquivo de imagem

    Returns:
        True se válido, False caso contrário
    """
    if not os.path.exists(path):
        logger.error(f"Arquivo não encontrado: {path}")
        return False

    from src.config import SUPPORTED_IMAGE_FORMATS
    ext = os.path.splitext(path)[1].lower()
    if ext not in SUPPORTED_IMAGE_FORMATS:
        logger.error(f"Formato de imagem não suportado: {ext}")
        return False

    return True


def create_output_directory(base_dir: str) -> str:
    """
    Cria diretório de output com timestamp.

    Args:
        base_dir: Diretório base para output

    Returns:
        Caminho completo do diretório criado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(base_dir, timestamp)
    os.makedirs(output_path, exist_ok=True)
    logger.info(f"Diretório de output criado: {output_path}")
    return output_path


def format_price(price: float, show_currency: bool = True) -> str:
    """
    Formata preço para exibição.

    Args:
        price: Valor do preço
        show_currency: Se deve incluir símbolo de moeda

    Returns:
        String formatada do preço
    """
    if show_currency:
        return f"R$ {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calculate_discount_percentage(original: float, promotional: float) -> int:
    """
    Calcula percentual de desconto.

    Args:
        original: Preço original
        promotional: Preço promocional

    Returns:
        Percentual de desconto arredondado
    """
    if original <= 0 or promotional >= original:
        return 0
    return int(((original - promotional) / original) * 100)


def truncate_text(text: str, max_length: int, ellipsis: str = "...") -> str:
    """
    Trunca texto para comprimento máximo.

    Args:
        text: Texto original
        max_length: Comprimento máximo
        ellipsis: String a adicionar quando truncado

    Returns:
        Texto truncado se necessário
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(ellipsis)] + ellipsis


def resize_to_fit(
    original_size: Tuple[int, int],
    target_size: Tuple[int, int],
    maintain_aspect: bool = True
) -> Tuple[int, int]:
    """
    Calcula novo tamanho mantendo proporções.

    Args:
        original_size: Tamanho original (width, height)
        target_size: Tamanho alvo (width, height)
        maintain_aspect: Se deve manter aspect ratio

    Returns:
        Novo tamanho (width, height)
    """
    if not maintain_aspect:
        return target_size

    orig_w, orig_h = original_size
    target_w, target_h = target_size

    # Calcula ratios
    ratio_w = target_w / orig_w
    ratio_h = target_h / orig_h

    # Usa o menor ratio para garantir que cabe no target
    ratio = min(ratio_w, ratio_h)

    new_w = int(orig_w * ratio)
    new_h = int(orig_h * ratio)

    return (new_w, new_h)


def blend_colors(
    color1: Tuple[int, int, int],
    color2: Tuple[int, int, int],
    ratio: float = 0.5
) -> Tuple[int, int, int]:
    """
    Mistura duas cores RGB.

    Args:
        color1: Primeira cor RGB
        color2: Segunda cor RGB
        ratio: Proporção da segunda cor (0.0 a 1.0)

    Returns:
        Cor resultante RGB
    """
    ratio = max(0.0, min(1.0, ratio))
    return tuple(
        int(c1 * (1 - ratio) + c2 * ratio)
        for c1, c2 in zip(color1, color2)
    )


def validate_hex_colors(colors: list) -> bool:
    """
    Valida lista de cores hexadecimais.

    Args:
        colors: Lista de strings em formato hexadecimal

    Returns:
        True se todas são válidas, False caso contrário
    """
    for color in colors:
        try:
            hex_to_rgb(color)
        except ValueError:
            logger.error(f"Cor hexadecimal inválida: {color}")
            return False
    return True
