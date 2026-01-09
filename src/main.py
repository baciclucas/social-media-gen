"""
Sistema gerador de criativos de mídia para e-commerce.
"""
import os
import json
import time
import logging
from typing import Dict, List
from datetime import datetime

from src.config import OUTPUT_DIR
from src.processors.image_processor import ImageProcessor
from src.processors.color_processor import ColorProcessor
from src.processors.text_generator import TextGenerator
from src.utils.helpers import (
    create_output_directory,
    validate_image_path,
    validate_hex_colors
)

# Importa todos os templates
from src.templates.instagram_feed import InstagramFeedMinimalist, InstagramFeedVibrant
from src.templates.instagram_story import InstagramStoryMinimalist, InstagramStoryVibrant
from src.templates.facebook_ad import FacebookAdMinimalist, FacebookAdVibrant
from src.templates.web_banner import WebBannerMinimalist, WebBannerVibrant

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CreativeGenerator:
    """Gerador principal de criativos."""

    def __init__(self, api_key: str = None):
        """
        Inicializa o gerador de criativos.

        Args:
            api_key: Chave da API Anthropic (opcional)
        """
        self.text_generator = TextGenerator(api_key)
        logger.info("CreativeGenerator inicializado")

    def validate_input(self, data: Dict) -> bool:
        """
        Valida os dados de entrada.

        Args:
            data: Dados de entrada

        Returns:
            True se válido, False caso contrário
        """
        # Valida estrutura básica
        if "brand" not in data or "product" not in data:
            logger.error("Dados de entrada devem conter 'brand' e 'product'")
            return False

        brand = data["brand"]
        product = data["product"]

        # Valida brand
        if "logo_path" in brand:
            if not validate_image_path(brand["logo_path"]):
                return False

        if "primary_colors" not in brand or not brand["primary_colors"]:
            logger.error("Brand deve conter 'primary_colors'")
            return False

        if not validate_hex_colors(brand["primary_colors"]):
            return False

        # Valida product
        if "image_path" not in product:
            logger.error("Product deve conter 'image_path'")
            return False

        if not validate_image_path(product["image_path"]):
            return False

        if "name" not in product or "price_original" not in product:
            logger.error("Product deve conter 'name' e 'price_original'")
            return False

        return True

    def generate_creatives(self, data: Dict, output_dir: str = None) -> Dict:
        """
        Gera todos os criativos.

        Args:
            data: Dados de entrada
            output_dir: Diretório de saída (opcional)

        Returns:
            Dicionário com informações sobre os arquivos gerados
        """
        start_time = time.time()

        # Valida entrada
        if not self.validate_input(data):
            raise ValueError("Dados de entrada inválidos")

        logger.info("Iniciando geração de criativos...")

        # Cria diretório de output
        if output_dir is None:
            output_dir = create_output_directory(OUTPUT_DIR)
        else:
            os.makedirs(output_dir, exist_ok=True)

        # Extrai dados
        brand_data = data["brand"]
        product_data = data["product"]
        campaign_type = data.get("campaign_type", "standard")
        product_data["campaign_type"] = campaign_type

        # Inicializa processador de cores
        color_processor = ColorProcessor(brand_data["primary_colors"])

        # Processa logo
        logo_image = None
        if "logo_path" in brand_data and brand_data["logo_path"]:
            logger.info("Processando logo...")
            # Usa tamanho médio para processar logo (será redimensionado por cada template)
            logo_image = ImageProcessor.process_logo(
                brand_data["logo_path"],
                (1080, 1080)
            )

        # Processa produto
        logger.info("Processando imagem do produto...")
        product_image = ImageProcessor.process_product(
            product_data["image_path"],
            (800, 800),
            remove_bg=False  # Por padrão False, pode ser configurado
        )

        if product_image is None:
            raise ValueError("Falha ao processar imagem do produto")

        # Mapa de templates
        templates_map = {
            "instagram_feed": [
                ("v1", InstagramFeedMinimalist),
                ("v2", InstagramFeedVibrant)
            ],
            "instagram_story": [
                ("v1", InstagramStoryMinimalist),
                ("v2", InstagramStoryVibrant)
            ],
            "facebook_ad": [
                ("v1", FacebookAdMinimalist),
                ("v2", FacebookAdVibrant)
            ],
            "web_banner": [
                ("v1", WebBannerMinimalist),
                ("v2", WebBannerVibrant)
            ]
        }

        # Resultado
        result = {
            "output_dir": output_dir,
            "files": [],
            "texts_generated": {},
            "processing_time": 0
        }

        # Gera criativos para cada formato
        for format_type, template_variants in templates_map.items():
            logger.info(f"Gerando criativos para {format_type}...")

            # Gera textos para este formato
            texts = self.text_generator.generate_all_texts(product_data, format_type)
            result["texts_generated"][format_type] = texts

            # Gera variações
            for variant_name, template_class in template_variants:
                template = template_class(color_processor)

                # Gera criativo
                creative = template.generate(
                    brand_data,
                    product_data,
                    texts,
                    logo_image,
                    product_image
                )

                # Salva arquivo
                filename = f"{format_type}_{variant_name}.png"
                filepath = os.path.join(output_dir, filename)
                creative.save(filepath, quality=95)

                result["files"].append(filepath)
                logger.info(f"Criativo salvo: {filename}")

        # Salva metadata
        metadata = {
            "brand": brand_data.get("name", "Unknown"),
            "product": product_data.get("name"),
            "campaign_type": campaign_type,
            "colors_used": brand_data["primary_colors"],
            "texts_generated": result["texts_generated"],
            "files_generated": [os.path.basename(f) for f in result["files"]],
            "generation_date": datetime.now().isoformat(),
            "processing_time_seconds": time.time() - start_time
        }

        metadata_path = os.path.join(output_dir, "metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        result["processing_time"] = time.time() - start_time
        result["metadata_path"] = metadata_path

        logger.info(f"✓ Geração concluída em {result['processing_time']:.2f}s")
        logger.info(f"✓ {len(result['files'])} criativos gerados em: {output_dir}")

        return result


def generate_from_json(json_path: str, api_key: str = None) -> Dict:
    """
    Gera criativos a partir de arquivo JSON.

    Args:
        json_path: Caminho para o arquivo JSON
        api_key: Chave da API Anthropic (opcional)

    Returns:
        Dicionário com informações sobre os arquivos gerados
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    generator = CreativeGenerator(api_key)
    return generator.generate_creatives(data)


def generate_from_dict(data: Dict, api_key: str = None) -> Dict:
    """
    Gera criativos a partir de dicionário Python.

    Args:
        data: Dicionário com os dados
        api_key: Chave da API Anthropic (opcional)

    Returns:
        Dicionário com informações sobre os arquivos gerados
    """
    generator = CreativeGenerator(api_key)
    return generator.generate_creatives(data)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python -m src.main <caminho_json>")
        print("Exemplo: python -m src.main assets/examples/test_case_1.json")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Erro: Arquivo não encontrado: {json_path}")
        sys.exit(1)

    try:
        result = generate_from_json(json_path)
        print(f"\n✓ Sucesso! {len(result['files'])} criativos gerados.")
        print(f"✓ Output: {result['output_dir']}")
        print(f"✓ Tempo: {result['processing_time']:.2f}s")
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        logger.exception("Erro ao gerar criativos")
        sys.exit(1)
