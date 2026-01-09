"""
Templates para Web Banner (1200x400).
"""
from typing import Dict, Optional
from PIL import Image, ImageDraw
import logging

from src.templates.base_template import BaseTemplate
from src.processors.color_processor import ColorProcessor
from src.processors.image_processor import ImageProcessor
from src.utils.helpers import get_text_color

logger = logging.getLogger(__name__)


class WebBannerMinimalist(BaseTemplate):
    """Template minimalista para Web Banner."""

    def __init__(self, color_processor: ColorProcessor):
        super().__init__("web_banner", "minimalist", color_processor)

    def generate(
        self,
        brand_data: Dict,
        product_data: Dict,
        texts: Dict[str, str],
        logo_image: Optional[Image.Image],
        product_image: Optional[Image.Image]
    ) -> Image.Image:
        """Gera criativo minimalista para Web Banner."""
        # Canvas claro
        canvas = self.create_canvas((255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        text_color = (45, 55, 72)
        accent_color = self.color_processor.get_accent_color()

        # Logo no topo esquerdo
        if logo_image:
            self.paste_logo(canvas, logo_image, "top_left")

        # Produto no lado direito
        if product_image:
            product_x = self.size[0] - 280
            product_y = self.size[1] // 2
            self.paste_product(canvas, product_image, (product_x, product_y))

        # Textos no lado esquerdo
        text_x = self.padding['outer'] + 30

        # Título
        title_y = 100
        self.draw_text_aligned(
            draw,
            texts['title'],
            (text_x, title_y),
            'title',
            text_color,
            align='left'
        )

        # Subtítulo
        subtitle_y = title_y + 80
        self.draw_text_aligned(
            draw,
            texts['subtitle'],
            (text_x, subtitle_y),
            'subtitle',
            text_color,
            align='left'
        )

        # Preço e CTA na mesma linha
        price_y = subtitle_y + 80
        self.draw_text_aligned(
            draw,
            texts['price'],
            (text_x, price_y),
            'price',
            accent_color,
            align='left'
        )

        # Badge de desconto
        if texts.get('discount'):
            badge_pos = (text_x + 200, price_y - 15)
            self.draw_discount_badge(canvas, texts['discount'], badge_pos, accent_color, (255, 255, 255))

        draw = ImageDraw.Draw(canvas)

        # CTA ao lado do preço
        cta_x = text_x + 380
        self.draw_cta_button(
            draw,
            texts['cta'],
            (cta_x, price_y + 36),
            accent_color,
            (255, 255, 255),
            width=240,
            height=55
        )

        return canvas


class WebBannerVibrant(BaseTemplate):
    """Template vibrante para Web Banner."""

    def __init__(self, color_processor: ColorProcessor):
        super().__init__("web_banner", "vibrant", color_processor)

    def generate(
        self,
        brand_data: Dict,
        product_data: Dict,
        texts: Dict[str, str],
        logo_image: Optional[Image.Image],
        product_image: Optional[Image.Image]
    ) -> Image.Image:
        """Gera criativo vibrante para Web Banner."""
        # Background com gradiente horizontal
        bg_color1 = self.color_processor.get_primary_color(0)
        bg_color2 = self.color_processor.get_darker_shade(bg_color1, 0.2)

        canvas = ImageProcessor.create_gradient_background(
            self.size,
            bg_color1,
            bg_color2,
            'horizontal'
        )

        text_color = get_text_color(bg_color1)

        # Produto no centro
        if product_image:
            product_x = self.size[0] // 2
            product_y = self.size[1] // 2
            self.paste_product(canvas, product_image, (product_x, product_y))

        # Logo no topo esquerdo
        if logo_image:
            self.paste_logo(canvas, logo_image, "top_left")

        draw = ImageDraw.Draw(canvas)

        # Textos no lado esquerdo
        text_x = self.padding['outer'] + 30

        # Título
        title_y = 100
        self.draw_text_aligned(
            draw,
            texts['title'],
            (text_x, title_y),
            'title',
            text_color,
            align='left'
        )

        # Subtítulo
        subtitle_y = title_y + 75
        self.draw_text_aligned(
            draw,
            texts['subtitle'],
            (text_x, subtitle_y),
            'subtitle',
            text_color,
            align='left'
        )

        # Preço
        price_y = subtitle_y + 70
        self.draw_text_aligned(
            draw,
            texts['price'],
            (text_x, price_y),
            'price',
            text_color,
            align='left'
        )

        # Badge de desconto no lado direito
        if texts.get('discount'):
            badge_pos = (self.size[0] - 120, 80)
            badge_color = self.color_processor.get_accent_color()
            self.draw_discount_badge(canvas, texts['discount'], badge_pos, badge_color, (255, 255, 255))

        draw = ImageDraw.Draw(canvas)

        # CTA na parte inferior direita
        cta_x = self.size[0] - 200
        cta_y = self.size[1] - 80
        cta_bg = text_color
        cta_text = bg_color1
        self.draw_cta_button(
            draw,
            texts['cta'],
            (cta_x, cta_y),
            cta_bg,
            cta_text,
            width=250,
            height=50
        )

        return canvas
