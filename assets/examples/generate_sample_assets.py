"""
Script para gerar assets de exemplo (logos e produtos).
"""
from PIL import Image, ImageDraw, ImageFont
import os


def create_logo(name: str, color: tuple, output_path: str):
    """Cria um logo simples."""
    img = Image.new('RGBA', (400, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Círculo com initial
    circle_color = color + (255,)
    draw.ellipse([(20, 20), (130, 130)], fill=circle_color)

    # Inicial
    initial = name[0].upper()
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), initial, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = 75 - text_width // 2
    text_y = 75 - text_height // 2

    draw.text((text_x, text_y), initial, font=font, fill=(255, 255, 255))

    # Nome da loja
    try:
        font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font_name = ImageFont.load_default()

    draw.text((150, 50), name, font=font_name, fill=color + (255,))

    img.save(output_path)
    print(f"Logo criado: {output_path}")


def create_product(product_type: str, color: tuple, output_path: str):
    """Cria uma imagem de produto simples."""
    img = Image.new('RGB', (600, 600), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    if product_type == "camiseta":
        # Desenha camiseta simples
        # Corpo
        draw.rectangle([(150, 200), (450, 500)], fill=color)
        # Mangas
        draw.rectangle([(80, 200), (150, 350)], fill=color)
        draw.rectangle([(450, 200), (520, 350)], fill=color)
        # Gola
        draw.ellipse([(250, 180), (350, 220)], fill=(100, 100, 100))

    elif product_type == "creme":
        # Desenha frasco de creme
        # Frasco
        draw.rounded_rectangle([(200, 250), (400, 500)], radius=20, fill=color)
        # Tampa
        draw.rectangle([(220, 200), (380, 250)], fill=(150, 150, 150))
        # Label
        draw.ellipse([(250, 350), (350, 450)], fill=(255, 255, 255))

    elif product_type == "fone":
        # Desenha fone de ouvido
        # Arco
        draw.arc([(200, 150), (400, 350)], 180, 360, fill=color, width=30)
        # Fones
        draw.ellipse([(170, 300), (250, 380)], fill=color)
        draw.ellipse([(350, 300), (430, 380)], fill=color)
        # Almofadas
        draw.ellipse([(185, 315), (235, 365)], fill=(50, 50, 50))
        draw.ellipse([(365, 315), (415, 365)], fill=(50, 50, 50))

    img.save(output_path)
    print(f"Produto criado: {output_path}")


if __name__ == "__main__":
    # Cria diretórios se não existem
    os.makedirs("assets/examples", exist_ok=True)

    # Caso 1: Moda
    create_logo("ModaStyle", (255, 107, 107), "assets/examples/logo_moda.png")
    create_product("camiseta", (255, 107, 107), "assets/examples/produto_camiseta.png")

    # Caso 2: Beleza
    create_logo("BelaVida", (255, 229, 229), "assets/examples/logo_beleza.png")
    create_product("creme", (212, 165, 165), "assets/examples/produto_creme.png")

    # Caso 3: Eletrônicos
    create_logo("TechSound", (45, 55, 72), "assets/examples/logo_tech.png")
    create_product("fone", (66, 153, 225), "assets/examples/produto_fone.png")

    print("\nTodos os assets de exemplo foram criados!")
