"""
Templates para Instagram Story (1080x1920).
"""
from typing import Dict, Optional
from PIL import Image, ImageDraw
import logging

from src.templates.base_template import BaseTemplate
from src.processors.color_processor import ColorProcessor
from src.processors.image_processor import ImageProcessor
from src.utils.helpers import get_text_color

logger = logging.getLogger(__name__)


class InstagramStoryMinimalist(BaseTemplate):
    """Template minimalista para Instagram Story."""

    def __init__(self, color_processor: ColorProcessor):
        super().__init__("instagram_story", "minimalist", color_processor)

    def generate(
        self,
        brand_data: Dict,
        product_data: Dict,
        texts: Dict[str, str],
        logo_image: Optional[Image.Image],
        product_image: Optional[Image.Image]
    ) -> Image.Image:
        """Gera criativo minimalista para Instagram Story."""
        # Canvas claro
        canvas = self.create_canvas((255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        text_color = (45, 55, 72)
        accent_color = self.color_processor.get_accent_color()

        # Logo no topo
        if logo_image:
            self.paste_logo(canvas, logo_image, "top_left")

        # Título no topo (área de segurança)
        title_y = 200
        self.draw_text_centered(draw, texts['title'], title_y, 'title', text_color)

        # Produto no centro
        if product_image:
            product_y = self.size[1] // 2 - 100
            self.paste_product(canvas, product_image, (self.size[0] // 2, product_y))

        # Badge de desconto
        if texts.get('discount'):
            badge_pos = (self.size[0] - 120, 300)
            self.draw_discount_badge(canvas, texts['discount'], badge_pos, accent_color, (255, 255, 255))

        draw = ImageDraw.Draw(canvas)

        # Preço
        price_y = self.size[1] - 450
        self.draw_text_centered(draw, texts['price'], price_y, 'price', accent_color)

        # Subtítulo
        subtitle_y = price_y + 140
        self.draw_text_centered(draw, texts['subtitle'], subtitle_y, 'subtitle', text_color)

        # CTA na parte inferior
        cta_y = self.size[1] - 200
        self.draw_cta_button(
            draw,
            texts['cta'],
            (self.size[0] // 2, cta_y),
            accent_color,
            (255, 255, 255),
            width=400,
            height=80
        )

        return canvas


class InstagramStoryVibrant(BaseTemplate):
    """Template vibrante para Instagram Story."""

    def __init__(self, color_processor: ColorProcessor):
        super().__init__("instagram_story", "vibrant", color_processor)

    def generate(
        self,
        brand_data: Dict,
        product_data: Dict,
        texts: Dict[str, str],
        logo_image: Optional[Image.Image],
        product_image: Optional[Image.Image]
    ) -> Image.Image:
        """Gera criativo vibrante para Instagram Story."""
        # Background com gradiente
        bg_color1 = self.color_processor.get_primary_color(0)
        bg_color2 = self.color_processor.get_lighter_shade(bg_color1, 0.4)

        canvas = ImageProcessor.create_gradient_background(
            self.size,
            bg_color1,
            bg_color2,
            'vertical'
        )

        draw = ImageDraw.Draw(canvas)
        text_color = get_text_color(bg_color1)

        # Logo no topo
        if logo_image:
            self.paste_logo(canvas, logo_image, "top_right")

        # Título no topo
        title_y = 180
        self.draw_text_centered(draw, texts['title'], title_y, 'title', text_color)

        # Produto no centro superior
        if product_image:
            product_y = 700
            self.paste_product(canvas, product_image, (self.size[0] // 2, product_y))

        # Badge de desconto no topo esquerdo
        if texts.get('discount'):
            badge_pos = (120, 280)
            badge_color = self.color_processor.get_accent_color()
            self.draw_discount_badge(canvas, texts['discount'], badge_pos, badge_color, (255, 255, 255))

        draw = ImageDraw.Draw(canvas)

        # Área inferior com informações
        info_bg_y = self.size[1] - 500
        # Desenha retângulo semi-transparente para destacar informações
        overlay_color = (0, 0, 0) if text_color == (255, 255, 255) else (255, 255, 255)
        draw.rectangle(
            [(0, info_bg_y), (self.size[0], self.size[1])],
            fill=overlay_color + (180,)
        )

        # Cor de texto invertida na área de overlay
        info_text_color = (255, 255, 255) if overlay_color == (0, 0, 0) else (45, 55, 72)

        # Preço
        price_y = info_bg_y + 80
        self.draw_text_centered(draw, texts['price'], price_y, 'price', info_text_color)

        # Subtítulo
        subtitle_y = price_y + 130
        self.draw_text_centered(draw, texts['subtitle'], subtitle_y, 'subtitle', info_text_color)

        # CTA
        cta_y = self.size[1] - 150
        cta_bg = self.color_processor.get_accent_color()
        self.draw_cta_button(
            draw,
            texts['cta'],
            (self.size[0] // 2, cta_y),
            cta_bg,
            (255, 255, 255),
            width=420,
            height=85
        )

        return canvas
