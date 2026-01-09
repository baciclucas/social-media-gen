"""
Módulo para processamento e manipulação de imagens.
"""
from typing import Tuple, Optional
import logging
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
import os

from src.config import LOGO_CONFIG, PRODUCT_CONFIG
from src.utils.helpers import resize_to_fit

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Processa imagens para os criativos."""

    @staticmethod
    def load_image(image_path: str) -> Optional[Image.Image]:
        """
        Carrega imagem do caminho especificado.

        Args:
            image_path: Caminho para a imagem

        Returns:
            Objeto Image ou None em caso de erro
        """
        try:
            img = Image.open(image_path)
            return img.convert('RGBA')
        except Exception as e:
            logger.error(f"Erro ao carregar imagem {image_path}: {e}")
            return None

    @staticmethod
    def resize_image(
        image: Image.Image,
        target_size: Tuple[int, int],
        maintain_aspect: bool = True
    ) -> Image.Image:
        """
        Redimensiona imagem.

        Args:
            image: Imagem PIL
            target_size: Tamanho alvo (width, height)
            maintain_aspect: Se deve manter aspect ratio

        Returns:
            Imagem redimensionada
        """
        if maintain_aspect:
            new_size = resize_to_fit(image.size, target_size, True)
            return image.resize(new_size, Image.Resampling.LANCZOS)
        return image.resize(target_size, Image.Resampling.LANCZOS)

    @staticmethod
    def add_shadow(
        image: Image.Image,
        offset: Tuple[int, int] = (10, 10),
        blur_radius: int = 20,
        shadow_color: Tuple[int, int, int, int] = (0, 0, 0, 100)
    ) -> Image.Image:
        """
        Adiciona sombra à imagem.

        Args:
            image: Imagem PIL com canal alpha
            offset: Deslocamento da sombra (x, y)
            blur_radius: Raio do blur da sombra
            shadow_color: Cor da sombra em RGBA

        Returns:
            Imagem com sombra
        """
        # Cria uma nova imagem maior para acomodar a sombra
        shadow_offset_x, shadow_offset_y = offset
        new_width = image.width + abs(shadow_offset_x) + blur_radius * 2
        new_height = image.height + abs(shadow_offset_y) + blur_radius * 2

        # Cria camada de sombra
        shadow = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))

        # Posição da sombra
        shadow_x = blur_radius + max(0, shadow_offset_x)
        shadow_y = blur_radius + max(0, shadow_offset_y)

        # Cria máscara da sombra a partir do canal alpha da imagem
        shadow_mask = image.split()[3]  # Canal alpha
        shadow_layer = Image.new('RGBA', image.size, shadow_color)
        shadow_layer.putalpha(shadow_mask)

        # Cola a sombra
        shadow.paste(shadow_layer, (shadow_x, shadow_y), shadow_layer)

        # Aplica blur
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

        # Posição da imagem original
        img_x = blur_radius + max(0, -shadow_offset_x)
        img_y = blur_radius + max(0, -shadow_offset_y)

        # Cola a imagem original sobre a sombra
        result = Image.new('RGBA', shadow.size, (0, 0, 0, 0))
        result.paste(shadow, (0, 0), shadow)
        result.paste(image, (img_x, img_y), image)

        return result

    @staticmethod
    def remove_background_simple(image: Image.Image, threshold: int = 240) -> Image.Image:
        """
        Remove background simples (backgrounds brancos/claros).
        Fallback quando rembg não está disponível.

        Args:
            image: Imagem PIL
            threshold: Threshold para considerar pixel como background

        Returns:
            Imagem com background removido
        """
        img = image.convert('RGBA')
        datas = img.getdata()

        new_data = []
        for item in datas:
            # Se pixel é branco/claro, torna transparente
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        img.putdata(new_data)
        return img

    @staticmethod
    def process_logo(
        logo_path: str,
        canvas_size: Tuple[int, int]
    ) -> Optional[Image.Image]:
        """
        Processa logo para tamanho apropriado.

        Args:
            logo_path: Caminho para o logo
            canvas_size: Tamanho do canvas (para calcular proporções)

        Returns:
            Logo processado ou None
        """
        logo = ImageProcessor.load_image(logo_path)
        if not logo:
            return None

        # Calcula tamanho máximo do logo
        max_width = int(canvas_size[0] * LOGO_CONFIG['max_width_ratio'])
        max_height = int(canvas_size[1] * LOGO_CONFIG['max_height_ratio'])

        # Redimensiona mantendo proporções
        logo = ImageProcessor.resize_image(
            logo,
            (max_width, max_height),
            maintain_aspect=True
        )

        return logo

    @staticmethod
    def process_product(
        product_path: str,
        target_size: Tuple[int, int],
        remove_bg: bool = False
    ) -> Optional[Image.Image]:
        """
        Processa imagem do produto.

        Args:
            product_path: Caminho para imagem do produto
            target_size: Tamanho alvo
            remove_bg: Se deve tentar remover background

        Returns:
            Produto processado ou None
        """
        product = ImageProcessor.load_image(product_path)
        if not product:
            return None

        # Remove background se solicitado
        if remove_bg:
            try:
                # Tenta usar rembg se disponível
                from rembg import remove
                product_data = product.tobytes()
                product = Image.open(io.BytesIO(remove(product_data)))
            except ImportError:
                logger.warning("rembg não disponível, usando remoção simples")
                product = ImageProcessor.remove_background_simple(product)
            except Exception as e:
                logger.warning(f"Erro ao remover background: {e}")

        # Redimensiona
        product = ImageProcessor.resize_image(
            product,
            target_size,
            maintain_aspect=True
        )

        # Adiciona sombra se configurado
        if PRODUCT_CONFIG['add_shadow']:
            product = ImageProcessor.add_shadow(
                product,
                offset=PRODUCT_CONFIG['shadow_offset'],
                blur_radius=PRODUCT_CONFIG['shadow_blur']
            )

        return product

    @staticmethod
    def create_gradient_background(
        size: Tuple[int, int],
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int],
        direction: str = 'vertical'
    ) -> Image.Image:
        """
        Cria background com gradiente.

        Args:
            size: Tamanho da imagem (width, height)
            color1: Primeira cor RGB
            color2: Segunda cor RGB
            direction: Direção do gradiente ('vertical', 'horizontal', 'diagonal')

        Returns:
            Imagem com gradiente
        """
        width, height = size
        base = Image.new('RGB', size, color1)
        draw = ImageDraw.Draw(base)

        if direction == 'vertical':
            for y in range(height):
                ratio = y / height
                r = int(color1[0] + (color2[0] - color1[0]) * ratio)
                g = int(color1[1] + (color2[1] - color1[1]) * ratio)
                b = int(color1[2] + (color2[2] - color1[2]) * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))

        elif direction == 'horizontal':
            for x in range(width):
                ratio = x / width
                r = int(color1[0] + (color2[0] - color1[0]) * ratio)
                g = int(color1[1] + (color2[1] - color1[1]) * ratio)
                b = int(color1[2] + (color2[2] - color1[2]) * ratio)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))

        elif direction == 'diagonal':
            for y in range(height):
                for x in range(width):
                    ratio = (x + y) / (width + height)
                    r = int(color1[0] + (color2[0] - color1[0]) * ratio)
                    g = int(color1[1] + (color2[1] - color1[1]) * ratio)
                    b = int(color1[2] + (color2[2] - color1[2]) * ratio)
                    draw.point((x, y), fill=(r, g, b))

        return base

    @staticmethod
    def add_rounded_corners(
        image: Image.Image,
        radius: int = 20
    ) -> Image.Image:
        """
        Adiciona cantos arredondados à imagem.

        Args:
            image: Imagem PIL
            radius: Raio dos cantos

        Returns:
            Imagem com cantos arredondados
        """
        # Cria máscara com cantos arredondados
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            [(0, 0), image.size],
            radius=radius,
            fill=255
        )

        # Aplica máscara
        result = Image.new('RGBA', image.size, (0, 0, 0, 0))
        result.paste(image, (0, 0))
        result.putalpha(mask)

        return result

    @staticmethod
    def get_font(font_name: str, size: int) -> ImageFont.FreeTypeFont:
        """
        Obtém fonte para desenho de texto.

        Args:
            font_name: Nome da fonte
            size: Tamanho da fonte

        Returns:
            Objeto ImageFont
        """
        try:
            # Tenta carregar fonte do sistema
            return ImageFont.truetype(font_name, size)
        except:
            try:
                # Tenta algumas fontes comuns no Linux
                common_fonts = [
                    f"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                    f"/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                    f"/System/Library/Fonts/Helvetica.ttc",
                    "arial.ttf",
                    "Arial.ttf"
                ]
                for font_path in common_fonts:
                    if os.path.exists(font_path):
                        return ImageFont.truetype(font_path, size)
            except:
                pass

            # Fallback para fonte padrão
            logger.warning(f"Fonte {font_name} não encontrada, usando padrão")
            return ImageFont.load_default()

    @staticmethod
    def draw_text_with_outline(
        draw: ImageDraw.Draw,
        position: Tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        fill_color: Tuple[int, int, int],
        outline_color: Tuple[int, int, int] = (0, 0, 0),
        outline_width: int = 2
    ):
        """
        Desenha texto com contorno.

        Args:
            draw: Objeto ImageDraw
            position: Posição (x, y)
            text: Texto a desenhar
            font: Fonte
            fill_color: Cor do preenchimento
            outline_color: Cor do contorno
            outline_width: Largura do contorno
        """
        x, y = position

        # Desenha contorno
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)

        # Desenha texto principal
        draw.text((x, y), text, font=font, fill=fill_color)
