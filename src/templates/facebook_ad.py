"""
Templates para Facebook Ads (1200x628).
"""
from typing import Dict, Optional
from PIL import Image, ImageDraw
import logging

from src.templates.base_template import BaseTemplate
from src.processors.color_processor import ColorProcessor
from src.processors.image_processor import ImageProcessor
from src.utils.helpers import get_text_color

logger = logging.getLogger(__name__)


class FacebookAdMinimalist(BaseTemplate):
    """Template minimalista para Facebook Ad."""

    def __init__(self, color_processor: ColorProcessor):
        super().__init__("facebook_ad", "minimalist", color_processor)

    def generate(
        self,
        brand_data: Dict,
        product_data: Dict,
        texts: Dict[str, str],
        logo_image: Optional[Image.Image],
        product_image: Optional[Image.Image]
    ) -> Image.Image:
        """Gera criativo minimalista para Facebook Ad."""
        # Canvas claro
        canvas = self.create_canvas((248, 248, 250))
        draw = ImageDraw.Draw(canvas)

        text_color = (45, 55, 72)
        accent_color = self.color_processor.get_accent_color()

        # Logo no topo esquerdo
        if logo_image:
            self.paste_logo(canvas, logo_image, "top_left")

        # Produto no lado esquerdo
        if product_image:
            product_x = self.size[0] // 3 - 50
            product_y = self.size[1] // 2
            self.paste_product(canvas, product_image, (product_x, product_y))

        # Textos no lado direito
        text_x_start = self.size[0] * 2 // 3
        padding_right = self.padding['outer']

        # Título
        title_y = 100
        self.draw_text_aligned(
            draw,
            texts['title'],
            (text_x_start, title_y),
            'title',
            text_color,
            align='left'
        )

        # Subtítulo
        subtitle_y = title_y + 90
        self.draw_text_aligned(
            draw,
            texts['subtitle'],
            (text_x_start, subtitle_y),
            'subtitle',
            text_color,
            align='left'
        )

        # Preço
        price_y = subtitle_y + 80
        self.draw_text_aligned(
            draw,
            texts['price'],
            (text_x_start, price_y),
            'price',
            accent_color,
            align='left'
        )

        # Badge de desconto
        if texts.get('discount'):
            badge_pos = (product_x + 150, 100)
            self.draw_discount_badge(canvas, texts['discount'], badge_pos, accent_color, (255, 255, 255))

        draw = ImageDraw.Draw(canvas)

        # CTA
        cta_y = self.size[1] - 100
        cta_x = text_x_start + 150
        self.draw_cta_button(
            draw,
            texts['cta'],
            (cta_x, cta_y),
            accent_color,
            (255, 255, 255),
            width=280,
            height=60
        )

        return canvas


class FacebookAdVibrant(BaseTemplate):
    """Template vibrante para Facebook Ad."""

    def __init__(self, color_processor: ColorProcessor):
        super().__init__("facebook_ad", "vibrant", color_processor)

    def generate(
        self,
        brand_data: Dict,
        product_data: Dict,
        texts: Dict[str, str],
        logo_image: Optional[Image.Image],
        product_image: Optional[Image.Image]
    ) -> Image.Image:
        """Gera criativo vibrante para Facebook Ad."""
        # Background com cor da marca
        bg_color = self.color_processor.get_background_color("vibrant")
        canvas = self.create_canvas(bg_color)

        text_color = get_text_color(bg_color)

        # Produto no centro-direita com destaque
        if product_image:
            product_x = self.size[0] * 3 // 4
            product_y = self.size[1] // 2
            self.paste_product(canvas, product_image, (product_x, product_y))

        # Logo no topo direito
        if logo_image:
            self.paste_logo(canvas, logo_image, "top_right")

        draw = ImageDraw.Draw(canvas)

        # Textos no lado esquerdo
        text_x = self.padding['outer'] + 30
        text_max_width = self.size[0] // 2

        # Título
        title_y = 120
        self.draw_text_aligned(
            draw,
            texts['title'],
            (text_x, title_y),
            'title',
            text_color,
            align='left'
        )

        # Subtítulo
        subtitle_y = title_y + 90
        self.draw_text_aligned(
            draw,
            texts['subtitle'],
            (text_x, subtitle_y),
            'subtitle',
            text_color,
            align='left'
        )

        # Preço grande e destacado
        price_y = subtitle_y + 90
        self.draw_text_aligned(
            draw,
            texts['price'],
            (text_x, price_y),
            'price',
            text_color,
            align='left'
        )

        # Badge de desconto
        if texts.get('discount'):
            badge_pos = (text_x + 80, title_y - 40)
            badge_color = self.color_processor.get_accent_color()
            self.draw_discount_badge(canvas, texts['discount'], badge_pos, badge_color, (255, 255, 255))

        draw = ImageDraw.Draw(canvas)

        # CTA na parte inferior esquerda
        cta_y = self.size[1] - 90
        cta_x = text_x + 140
        cta_bg = text_color
        cta_text = bg_color
        self.draw_cta_button(
            draw,
            texts['cta'],
            (cta_x, cta_y),
            cta_bg,
            cta_text,
            width=260,
            height=60
        )

        return canvas
