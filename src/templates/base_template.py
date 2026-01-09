"""
Classe base abstrata para templates de criativos.
"""
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional
from PIL import Image, ImageDraw
import logging

from src.processors.image_processor import ImageProcessor
from src.processors.color_processor import ColorProcessor
from src.config import FORMATS, FONT_SIZES, PADDING

logger = logging.getLogger(__name__)


class BaseTemplate(ABC):
    """Classe base para todos os templates de criativos."""

    def __init__(
        self,
        format_type: str,
        template_style: str,
        color_processor: ColorProcessor
    ):
        """
        Inicializa o template.

        Args:
            format_type: Tipo do formato ("instagram_feed", etc.)
            template_style: Estilo do template ("minimalist" ou "vibrant")
            color_processor: Processador de cores
        """
        self.format_type = format_type
        self.template_style = template_style
        self.color_processor = color_processor
        self.size = FORMATS[format_type]
        self.padding = PADDING[format_type]
        self.font_sizes = FONT_SIZES[format_type]

        logger.info(f"Template {self.__class__.__name__} inicializado: {format_type}/{template_style}")

    @abstractmethod
    def generate(
        self,
        brand_data: Dict,
        product_data: Dict,
        texts: Dict[str, str],
        logo_image: Optional[Image.Image],
        product_image: Optional[Image.Image]
    ) -> Image.Image:
        """
        Gera o criativo.

        Args:
            brand_data: Dados da marca
            product_data: Dados do produto
            texts: Textos gerados (title, subtitle, cta, price, discount)
            logo_image: Imagem do logo processada
            product_image: Imagem do produto processada

        Returns:
            Imagem do criativo gerado
        """
        pass

    def create_canvas(self, background_color: Optional[Tuple[int, int, int]] = None) -> Image.Image:
        """
        Cria canvas base para o criativo.

        Args:
            background_color: Cor de fundo (opcional)

        Returns:
            Canvas vazio
        """
        if background_color is None:
            background_color = self.color_processor.get_background_color(self.template_style)

        canvas = Image.new('RGB', self.size, background_color)
        return canvas

    def paste_logo(
        self,
        canvas: Image.Image,
        logo: Image.Image,
        position: str = "top_left"
    ):
        """
        Cola logo no canvas.

        Args:
            canvas: Canvas onde colar
            logo: Imagem do logo
            position: Posição ("top_left", "top_right", "bottom_left", "bottom_right")
        """
        padding = self.padding['outer']

        if position == "top_left":
            x, y = padding, padding
        elif position == "top_right":
            x = canvas.width - logo.width - padding
            y = padding
        elif position == "bottom_left":
            x = padding
            y = canvas.height - logo.height - padding
        elif position == "bottom_right":
            x = canvas.width - logo.width - padding
            y = canvas.height - logo.height - padding
        else:
            x, y = padding, padding

        canvas.paste(logo, (x, y), logo if logo.mode == 'RGBA' else None)

    def paste_product(
        self,
        canvas: Image.Image,
        product: Image.Image,
        position: Tuple[int, int]
    ):
        """
        Cola produto no canvas.

        Args:
            canvas: Canvas onde colar
            product: Imagem do produto
            position: Posição (x, y) - centro da imagem
        """
        x = position[0] - product.width // 2
        y = position[1] - product.height // 2

        canvas.paste(product, (x, y), product if product.mode == 'RGBA' else None)

    def draw_text_centered(
        self,
        draw: ImageDraw.Draw,
        text: str,
        y_position: int,
        font_size_key: str,
        color: Tuple[int, int, int],
        font_name: str = "Arial"
    ) -> int:
        """
        Desenha texto centralizado horizontalmente.

        Args:
            draw: Objeto ImageDraw
            text: Texto a desenhar
            y_position: Posição Y
            font_size_key: Chave do tamanho da fonte no config
            color: Cor do texto
            font_name: Nome da fonte

        Returns:
            Altura do texto desenhado
        """
        font_size = self.font_sizes[font_size_key]
        font = ImageProcessor.get_font(font_name, font_size)

        # Calcula posição centralizada
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (self.size[0] - text_width) // 2

        # Desenha texto
        draw.text((x, y_position), text, font=font, fill=color)

        return text_height

    def draw_text_aligned(
        self,
        draw: ImageDraw.Draw,
        text: str,
        position: Tuple[int, int],
        font_size_key: str,
        color: Tuple[int, int, int],
        align: str = "left",
        font_name: str = "Arial"
    ) -> Tuple[int, int]:
        """
        Desenha texto com alinhamento específico.

        Args:
            draw: Objeto ImageDraw
            text: Texto a desenhar
            position: Posição base (x, y)
            font_size_key: Chave do tamanho da fonte
            color: Cor do texto
            align: Alinhamento ("left", "center", "right")
            font_name: Nome da fonte

        Returns:
            Tupla (largura, altura) do texto desenhado
        """
        font_size = self.font_sizes[font_size_key]
        font = ImageProcessor.get_font(font_name, font_size)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x, y = position

        if align == "center":
            x = x - text_width // 2
        elif align == "right":
            x = x - text_width

        draw.text((x, y), text, font=font, fill=color)

        return (text_width, text_height)

    def draw_price_with_strike(
        self,
        draw: ImageDraw.Draw,
        position: Tuple[int, int],
        price_current: str,
        price_original: Optional[str],
        color_current: Tuple[int, int, int],
        color_original: Tuple[int, int, int],
        font_name: str = "Arial"
    ):
        """
        Desenha preço com riscado no preço original (se houver).

        Args:
            draw: Objeto ImageDraw
            position: Posição base
            price_current: Preço atual
            price_original: Preço original (opcional)
            color_current: Cor do preço atual
            color_original: Cor do preço original
            font_name: Nome da fonte
        """
        x, y = position

        # Desenha preço atual (maior)
        font_current = ImageProcessor.get_font(font_name, self.font_sizes['price'])
        draw.text((x, y), price_current, font=font_current, fill=color_current)

        # Se há preço original, desenha acima com strike-through
        if price_original:
            font_original = ImageProcessor.get_font(font_name, int(self.font_sizes['price'] * 0.6))
            bbox_original = draw.textbbox((0, 0), price_original, font=font_original)
            text_width = bbox_original[2] - bbox_original[0]

            # Posição acima do preço atual
            y_original = y - 40

            # Desenha texto
            draw.text((x, y_original), price_original, font=font_original, fill=color_original)

            # Desenha linha através do texto
            line_y = y_original + (bbox_original[3] - bbox_original[1]) // 2
            draw.line([(x, line_y), (x + text_width, line_y)], fill=color_original, width=3)

    def draw_discount_badge(
        self,
        canvas: Image.Image,
        discount_text: str,
        position: Tuple[int, int],
        bg_color: Tuple[int, int, int],
        text_color: Tuple[int, int, int]
    ):
        """
        Desenha badge de desconto.

        Args:
            canvas: Canvas onde desenhar
            discount_text: Texto do desconto (ex: "-30%")
            position: Posição (x, y) do centro do badge
            bg_color: Cor de fundo do badge
            text_color: Cor do texto
        """
        # Cria layer para o badge
        badge_layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(badge_layer)

        # Desenha círculo
        radius = 50
        x, y = position
        draw.ellipse(
            [(x - radius, y - radius), (x + radius, y + radius)],
            fill=bg_color + (255,)
        )

        # Desenha texto
        font = ImageProcessor.get_font("Arial", 36)
        bbox = draw.textbbox((0, 0), discount_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = x - text_width // 2
        text_y = y - text_height // 2

        draw.text((text_x, text_y), discount_text, font=font, fill=text_color + (255,))

        # Combina com canvas
        canvas.paste(badge_layer, (0, 0), badge_layer)

    def draw_cta_button(
        self,
        draw: ImageDraw.Draw,
        text: str,
        position: Tuple[int, int],
        bg_color: Tuple[int, int, int],
        text_color: Tuple[int, int, int],
        width: int = 300,
        height: int = 70,
        radius: int = 35
    ):
        """
        Desenha botão de call-to-action.

        Args:
            draw: Objeto ImageDraw
            text: Texto do botão
            position: Posição do centro do botão
            bg_color: Cor de fundo
            text_color: Cor do texto
            width: Largura do botão
            height: Altura do botão
            radius: Raio dos cantos arredondados
        """
        x, y = position

        # Calcula coordenadas do retângulo
        left = x - width // 2
        top = y - height // 2
        right = x + width // 2
        bottom = y + height // 2

        # Desenha retângulo arredondado
        draw.rounded_rectangle(
            [(left, top), (right, bottom)],
            radius=radius,
            fill=bg_color
        )

        # Desenha texto centralizado
        font = ImageProcessor.get_font("Arial", self.font_sizes['cta'])
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = x - text_width // 2
        text_y = y - text_height // 2

        draw.text((text_x, text_y), text, font=font, fill=text_color)
