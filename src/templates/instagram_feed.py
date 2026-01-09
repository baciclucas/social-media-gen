"""
Templates para Instagram Feed (1080x1080).
"""
from typing import Dict, Optional
from PIL import Image, ImageDraw
import logging

from src.templates.base_template import BaseTemplate
from src.processors.color_processor import ColorProcessor
from src.utils.helpers import get_text_color

logger = logging.getLogger(__name__)


class InstagramFeedMinimalist(BaseTemplate):
    """Template minimalista para Instagram Feed."""

    def __init__(self, color_processor: ColorProcessor):
        super().__init__("instagram_feed", "minimalist", color_processor)

    def generate(
        self,
        brand_data: Dict,
        product_data: Dict,
        texts: Dict[str, str],
        logo_image: Optional[Image.Image],
        product_image: Optional[Image.Image]
    ) -> Image.Image:
        """Gera criativo minimalista para Instagram Feed."""
        # Canvas branco/claro
        canvas = self.create_canvas((250, 250, 250))
        draw = ImageDraw.Draw(canvas)

        # Cola logo no topo esquerdo
        if logo_image:
            self.paste_logo(canvas, logo_image, "top_left")

        # Cola produto no centro
        if product_image:
            product_y = self.size[1] // 2 - 50
            self.paste_product(canvas, product_image, (self.size[0] // 2, product_y))

        # Cor de texto escura
        text_color = (45, 55, 72)
        accent_color = self.color_processor.get_accent_color()

        # Título acima do produto
        title_y = 120
        self.draw_text_centered(draw, texts['title'], title_y, 'title', text_color)

        # Preço abaixo do produto
        price_y = self.size[1] - 240

        if texts.get('discount'):
            # Desenha badge de desconto
            badge_pos = (self.size[0] - 100, 100)
            self.draw_discount_badge(canvas, texts['discount'], badge_pos, accent_color, (255, 255, 255))

        # Desenha preço
        draw = ImageDraw.Draw(canvas)  # Recria draw após badge
        self.draw_text_centered(draw, texts['price'], price_y, 'price', accent_color)

        # Subtítulo
        subtitle_y = price_y + 120
        self.draw_text_centered(draw, texts['subtitle'], subtitle_y, 'subtitle', text_color)

        # CTA button
        cta_y = self.size[1] - 100
        self.draw_cta_button(
            draw,
            texts['cta'],
            (self.size[0] // 2, cta_y),
            accent_color,
            (255, 255, 255)
        )

        return canvas


class InstagramFeedVibrant(BaseTemplate):
    """Template vibrante para Instagram Feed."""

    def __init__(self, color_processor: ColorProcessor):
        super().__init__("instagram_feed", "vibrant", color_processor)

    def generate(
        self,
        brand_data: Dict,
        product_data: Dict,
        texts: Dict[str, str],
        logo_image: Optional[Image.Image],
        product_image: Optional[Image.Image]
    ) -> Image.Image:
        """Gera criativo vibrante para Instagram Feed."""
        # Background com cor da marca
        bg_color = self.color_processor.get_background_color("vibrant")
        canvas = self.create_canvas(bg_color)
        draw = ImageDraw.Draw(canvas)

        # Determina cor de texto baseada no background
        text_color = get_text_color(bg_color)
        accent_color = self.color_processor.get_lighter_shade(bg_color, 0.3) if text_color == (255, 255, 255) else self.color_processor.get_darker_shade(bg_color, 0.3)

        # Cola logo no topo direito
        if logo_image:
            self.paste_logo(canvas, logo_image, "top_right")

        # Área do produto - lado esquerdo
        if product_image:
            product_x = self.size[0] // 3
            product_y = self.size[1] // 2
            self.paste_product(canvas, product_image, (product_x, product_y))

        draw = ImageDraw.Draw(canvas)

        # Textos no lado direito
        text_x_start = self.size[0] * 2 // 3
        text_area_width = self.size[0] - text_x_start - self.padding['outer']

        # Título
        title_y = 200
        self.draw_text_aligned(
            draw,
            texts['title'],
            (text_x_start, title_y),
            'title',
            text_color,
            align='left'
        )

        # Subtítulo
        subtitle_y = title_y + 100
        self.draw_text_aligned(
            draw,
            texts['subtitle'],
            (text_x_start, subtitle_y),
            'subtitle',
            text_color,
            align='left'
        )

        # Preço
        price_y = subtitle_y + 100
        self.draw_text_aligned(
            draw,
            texts['price'],
            (text_x_start, price_y),
            'price',
            text_color,
            align='left'
        )

        # Badge de desconto
        if texts.get('discount'):
            badge_pos = (100, 100)
            badge_bg = accent_color if text_color == (255, 255, 255) else (255, 87, 51)
            self.draw_discount_badge(canvas, texts['discount'], badge_pos, badge_bg, (255, 255, 255))

        # CTA
        draw = ImageDraw.Draw(canvas)
        cta_y = self.size[1] - 120
        cta_x = text_x_start + text_area_width // 2
        self.draw_cta_button(
            draw,
            texts['cta'],
            (cta_x, cta_y),
            text_color,
            bg_color,
            width=int(text_area_width * 0.9)
        )

        return canvas
