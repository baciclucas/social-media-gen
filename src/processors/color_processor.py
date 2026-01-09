"""
Módulo para processamento e harmonização de cores.
"""
from typing import List, Tuple, Optional
import logging
from PIL import Image
from src.utils.helpers import hex_to_rgb, rgb_to_hex, calculate_luminance

logger = logging.getLogger(__name__)


class ColorProcessor:
    """Processa e harmoniza cores para os criativos."""

    def __init__(self, primary_colors: List[str]):
        """
        Inicializa o processador de cores.

        Args:
            primary_colors: Lista de cores em formato hexadecimal
        """
        self.primary_colors_hex = primary_colors
        self.primary_colors_rgb = [hex_to_rgb(c) for c in primary_colors]
        logger.info(f"ColorProcessor inicializado com {len(primary_colors)} cores")

    def get_primary_color(self, index: int = 0) -> Tuple[int, int, int]:
        """
        Retorna cor primária por índice.

        Args:
            index: Índice da cor (0-based)

        Returns:
            Cor em formato RGB
        """
        if 0 <= index < len(self.primary_colors_rgb):
            return self.primary_colors_rgb[index]
        return self.primary_colors_rgb[0]

    def get_complementary_color(self, rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """
        Gera cor complementar (oposta no círculo cromático).

        Args:
            rgb: Cor base em RGB

        Returns:
            Cor complementar em RGB
        """
        r, g, b = rgb
        return (255 - r, 255 - g, 255 - b)

    def get_analogous_colors(
        self,
        rgb: Tuple[int, int, int],
        count: int = 2
    ) -> List[Tuple[int, int, int]]:
        """
        Gera cores análogas (adjacentes no círculo cromático).

        Args:
            rgb: Cor base em RGB
            count: Número de cores análogas a gerar

        Returns:
            Lista de cores em RGB
        """
        # Simplificação: gera variações mais claras e escuras
        colors = []
        r, g, b = rgb

        for i in range(1, count + 1):
            factor = 1 + (i * 0.15)
            lighter = tuple(min(255, int(c * factor)) for c in (r, g, b))
            colors.append(lighter)

        return colors

    def get_lighter_shade(
        self,
        rgb: Tuple[int, int, int],
        amount: float = 0.3
    ) -> Tuple[int, int, int]:
        """
        Gera versão mais clara da cor.

        Args:
            rgb: Cor base em RGB
            amount: Quantidade de claridade (0.0 a 1.0)

        Returns:
            Cor mais clara em RGB
        """
        amount = max(0.0, min(1.0, amount))
        return tuple(
            int(c + (255 - c) * amount) for c in rgb
        )

    def get_darker_shade(
        self,
        rgb: Tuple[int, int, int],
        amount: float = 0.3
    ) -> Tuple[int, int, int]:
        """
        Gera versão mais escura da cor.

        Args:
            rgb: Cor base em RGB
            amount: Quantidade de escuridão (0.0 a 1.0)

        Returns:
            Cor mais escura em RGB
        """
        amount = max(0.0, min(1.0, amount))
        return tuple(
            int(c * (1 - amount)) for c in rgb
        )

    def extract_colors_from_image(
        self,
        image_path: str,
        num_colors: int = 5
    ) -> List[Tuple[int, int, int]]:
        """
        Extrai cores dominantes de uma imagem.

        Args:
            image_path: Caminho para a imagem
            num_colors: Número de cores a extrair

        Returns:
            Lista de cores em RGB
        """
        try:
            # Abre e redimensiona imagem para performance
            img = Image.open(image_path)
            img = img.resize((150, 150))
            img = img.convert('RGB')

            # Obtém pixels
            pixels = list(img.getdata())

            # Agrupa cores similares (simplificação)
            color_count = {}
            for pixel in pixels:
                # Arredonda para reduzir variações
                rounded = tuple((c // 32) * 32 for c in pixel)
                color_count[rounded] = color_count.get(rounded, 0) + 1

            # Ordena por frequência
            sorted_colors = sorted(
                color_count.items(),
                key=lambda x: x[1],
                reverse=True
            )

            # Retorna as cores mais comuns
            return [color for color, count in sorted_colors[:num_colors]]

        except Exception as e:
            logger.error(f"Erro ao extrair cores da imagem: {e}")
            return []

    def get_gradient_colors(
        self,
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int],
        steps: int = 5
    ) -> List[Tuple[int, int, int]]:
        """
        Gera gradiente entre duas cores.

        Args:
            color1: Primeira cor em RGB
            color2: Segunda cor em RGB
            steps: Número de passos no gradiente

        Returns:
            Lista de cores formando o gradiente
        """
        gradient = []
        for i in range(steps):
            ratio = i / (steps - 1) if steps > 1 else 0
            color = tuple(
                int(c1 + (c2 - c1) * ratio)
                for c1, c2 in zip(color1, color2)
            )
            gradient.append(color)
        return gradient

    def get_color_palette(
        self,
        palette_type: str = "monochromatic"
    ) -> List[Tuple[int, int, int]]:
        """
        Gera paleta de cores baseada nas cores primárias.

        Args:
            palette_type: Tipo de paleta ("monochromatic", "complementary", "analogous")

        Returns:
            Lista de cores em RGB
        """
        base_color = self.primary_colors_rgb[0]

        if palette_type == "monochromatic":
            return [
                self.get_darker_shade(base_color, 0.4),
                self.get_darker_shade(base_color, 0.2),
                base_color,
                self.get_lighter_shade(base_color, 0.2),
                self.get_lighter_shade(base_color, 0.4),
            ]

        elif palette_type == "complementary":
            comp = self.get_complementary_color(base_color)
            return [
                base_color,
                self.get_lighter_shade(base_color, 0.3),
                comp,
                self.get_lighter_shade(comp, 0.3),
            ]

        elif palette_type == "analogous":
            return [base_color] + self.get_analogous_colors(base_color, 4)

        return self.primary_colors_rgb

    def get_background_color(self, template_style: str) -> Tuple[int, int, int]:
        """
        Retorna cor de background apropriada para o estilo de template.

        Args:
            template_style: Estilo do template ("minimalist" ou "vibrant")

        Returns:
            Cor de background em RGB
        """
        if template_style == "minimalist":
            # Background claro/neutro
            return (250, 250, 250)
        elif template_style == "vibrant":
            # Usa cor primária ou versão mais clara
            base = self.primary_colors_rgb[0]
            luminance = calculate_luminance(base)

            # Se cor é muito escura, clareia para o background
            if luminance < 0.3:
                return self.get_lighter_shade(base, 0.6)
            return base
        else:
            return (255, 255, 255)

    def get_accent_color(self) -> Tuple[int, int, int]:
        """
        Retorna cor de destaque (para CTAs, preços, etc.).

        Returns:
            Cor de destaque em RGB
        """
        # Usa segunda cor primária se disponível, senão usa complementar
        if len(self.primary_colors_rgb) > 1:
            return self.primary_colors_rgb[1]
        return self.get_complementary_color(self.primary_colors_rgb[0])

    def ensure_contrast(
        self,
        foreground: Tuple[int, int, int],
        background: Tuple[int, int, int],
        min_ratio: float = 4.5
    ) -> Tuple[int, int, int]:
        """
        Ajusta cor de foreground para garantir contraste adequado.

        Args:
            foreground: Cor do texto/foreground
            background: Cor do background
            min_ratio: Ratio mínimo de contraste (WCAG AA = 4.5)

        Returns:
            Cor de foreground ajustada
        """
        fg_lum = calculate_luminance(foreground)
        bg_lum = calculate_luminance(background)

        # Calcula contrast ratio
        lighter = max(fg_lum, bg_lum)
        darker = min(fg_lum, bg_lum)
        contrast_ratio = (lighter + 0.05) / (darker + 0.05)

        # Se contraste é adequado, retorna cor original
        if contrast_ratio >= min_ratio:
            return foreground

        # Caso contrário, retorna branco ou preto dependendo do background
        return (255, 255, 255) if bg_lum < 0.5 else (0, 0, 0)
