"""
Módulo para geração de textos usando Claude API.
"""
from typing import Dict, Optional
import logging
from anthropic import Anthropic

from src.config import ANTHROPIC_API_KEY, CLAUDE_MODEL, COPY_GENERATION_PROMPTS, TEXT_LIMITS
from src.utils.helpers import truncate_text, calculate_discount_percentage, format_price

logger = logging.getLogger(__name__)


class TextGenerator:
    """Gera textos persuasivos para os criativos usando Claude API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o gerador de textos.

        Args:
            api_key: Chave da API Anthropic (opcional, usa env var se não fornecida)
        """
        self.api_key = api_key or ANTHROPIC_API_KEY
        if not self.api_key:
            logger.warning("API key da Anthropic não configurada")
            self.client = None
        else:
            self.client = Anthropic(api_key=self.api_key)
            logger.info("TextGenerator inicializado com sucesso")

    def generate_copy(
        self,
        product_name: str,
        description: str,
        campaign_type: str,
        price_original: float,
        price_promotional: Optional[float],
        format_type: str,
        text_type: str = "title"
    ) -> str:
        """
        Gera copy para o criativo.

        Args:
            product_name: Nome do produto
            description: Descrição do produto
            campaign_type: Tipo de campanha ("promotional" ou "standard")
            price_original: Preço original
            price_promotional: Preço promocional (opcional)
            format_type: Tipo de formato ("instagram_feed", "instagram_story", etc.)
            text_type: Tipo de texto ("title" ou "subtitle")

        Returns:
            Texto gerado
        """
        # Se API não está configurada, gera texto simples
        if not self.client:
            return self._generate_fallback_copy(
                product_name,
                description,
                campaign_type,
                price_original,
                price_promotional,
                text_type
            )

        try:
            # Prepara informações de preço
            if price_promotional and price_promotional < price_original:
                discount_pct = calculate_discount_percentage(price_original, price_promotional)
                price_info = f"Preço original: {format_price(price_original)}, Preço promocional: {format_price(price_promotional)} ({discount_pct}% OFF)"
            else:
                price_info = f"Preço: {format_price(price_original)}"

            # Informação de urgência
            urgency_instruction = "Inclua urgência e senso de oportunidade" if campaign_type == "promotional" else "Mantenha tom informativo e convidativo"

            # Limite de caracteres para o formato
            char_limit = TEXT_LIMITS[format_type][text_type]

            # Monta o prompt
            prompt_template = COPY_GENERATION_PROMPTS[text_type]
            prompt = prompt_template.format(
                product_name=product_name,
                description=description,
                campaign_type=campaign_type,
                price_info=price_info,
                char_limit=char_limit,
                urgency_instruction=urgency_instruction
            )

            # Chama Claude API
            message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=200,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extrai texto da resposta
            generated_text = message.content[0].text.strip()

            # Remove aspas se presentes
            generated_text = generated_text.strip('"').strip("'")

            # Garante que está dentro do limite
            generated_text = truncate_text(generated_text, char_limit)

            logger.info(f"Texto gerado com sucesso para {format_type}/{text_type}")
            return generated_text

        except Exception as e:
            logger.error(f"Erro ao gerar texto com Claude API: {e}")
            return self._generate_fallback_copy(
                product_name,
                description,
                campaign_type,
                price_original,
                price_promotional,
                text_type
            )

    def _generate_fallback_copy(
        self,
        product_name: str,
        description: str,
        campaign_type: str,
        price_original: float,
        price_promotional: Optional[float],
        text_type: str
    ) -> str:
        """
        Gera texto simples sem usar IA (fallback).

        Args:
            product_name: Nome do produto
            description: Descrição do produto
            campaign_type: Tipo de campanha
            price_original: Preço original
            price_promotional: Preço promocional (opcional)
            text_type: Tipo de texto

        Returns:
            Texto gerado
        """
        if text_type == "title":
            if campaign_type == "promotional" and price_promotional:
                discount = calculate_discount_percentage(price_original, price_promotional)
                return f"{product_name} - {discount}% OFF!"
            return f"{product_name}"
        else:  # subtitle
            return description[:60] if description else "Produto de qualidade premium"

    def generate_cta(self, campaign_type: str, custom_cta: Optional[str] = None) -> str:
        """
        Gera ou valida call-to-action.

        Args:
            campaign_type: Tipo de campanha
            custom_cta: CTA customizado (opcional)

        Returns:
            CTA para usar no criativo
        """
        if custom_cta:
            return custom_cta

        ctas = {
            "promotional": [
                "Compre Agora!",
                "Aproveite!",
                "Garanta o Seu!",
                "Oferta Limitada!"
            ],
            "standard": [
                "Compre Agora",
                "Saiba Mais",
                "Confira",
                "Ver Produto"
            ]
        }

        return ctas.get(campaign_type, ctas["standard"])[0]

    def generate_all_texts(
        self,
        product_data: Dict,
        format_type: str
    ) -> Dict[str, str]:
        """
        Gera todos os textos necessários para um criativo.

        Args:
            product_data: Dados do produto
            format_type: Tipo de formato

        Returns:
            Dicionário com todos os textos gerados
        """
        campaign_type = product_data.get("campaign_type", "standard")

        texts = {
            "title": self.generate_copy(
                product_data["name"],
                product_data.get("description", ""),
                campaign_type,
                product_data["price_original"],
                product_data.get("price_promotional"),
                format_type,
                "title"
            ),
            "subtitle": self.generate_copy(
                product_data["name"],
                product_data.get("description", ""),
                campaign_type,
                product_data["price_original"],
                product_data.get("price_promotional"),
                format_type,
                "subtitle"
            ),
            "cta": self.generate_cta(
                campaign_type,
                product_data.get("cta")
            ),
            "price": self._format_price_text(
                product_data["price_original"],
                product_data.get("price_promotional")
            ),
            "discount": self._format_discount_badge(
                product_data["price_original"],
                product_data.get("price_promotional")
            )
        }

        return texts

    def _format_price_text(
        self,
        price_original: float,
        price_promotional: Optional[float]
    ) -> str:
        """
        Formata texto do preço.

        Args:
            price_original: Preço original
            price_promotional: Preço promocional (opcional)

        Returns:
            Texto formatado do preço
        """
        if price_promotional and price_promotional < price_original:
            return format_price(price_promotional)
        return format_price(price_original)

    def _format_discount_badge(
        self,
        price_original: float,
        price_promotional: Optional[float]
    ) -> Optional[str]:
        """
        Formata badge de desconto.

        Args:
            price_original: Preço original
            price_promotional: Preço promocional (opcional)

        Returns:
            Texto do badge ou None
        """
        if price_promotional and price_promotional < price_original:
            discount_pct = calculate_discount_percentage(price_original, price_promotional)
            return f"-{discount_pct}%"
        return None
