"""
Testes unitários básicos para o sistema gerador de criativos.
"""
import pytest
import os
from src.utils.helpers import (
    hex_to_rgb,
    rgb_to_hex,
    calculate_luminance,
    get_text_color,
    format_price,
    calculate_discount_percentage,
    truncate_text
)
from src.processors.color_processor import ColorProcessor


class TestHelpers:
    """Testes para funções auxiliares."""

    def test_hex_to_rgb(self):
        """Testa conversão hex para RGB."""
        assert hex_to_rgb("#FF6B6B") == (255, 107, 107)
        assert hex_to_rgb("FF6B6B") == (255, 107, 107)
        assert hex_to_rgb("#000000") == (0, 0, 0)
        assert hex_to_rgb("#FFFFFF") == (255, 255, 255)

    def test_hex_to_rgb_invalid(self):
        """Testa conversão com valor inválido."""
        with pytest.raises(ValueError):
            hex_to_rgb("INVALID")

    def test_rgb_to_hex(self):
        """Testa conversão RGB para hex."""
        assert rgb_to_hex((255, 107, 107)) == "#ff6b6b"
        assert rgb_to_hex((0, 0, 0)) == "#000000"
        assert rgb_to_hex((255, 255, 255)) == "#ffffff"

    def test_calculate_luminance(self):
        """Testa cálculo de luminância."""
        # Branco deve ter luminância próxima de 1
        assert calculate_luminance((255, 255, 255)) > 0.9
        # Preto deve ter luminância próxima de 0
        assert calculate_luminance((0, 0, 0)) < 0.1

    def test_get_text_color(self):
        """Testa escolha de cor de texto."""
        # Background claro deve retornar texto escuro
        assert get_text_color((255, 255, 255)) == (45, 55, 72)
        # Background escuro deve retornar texto claro
        assert get_text_color((0, 0, 0)) == (255, 255, 255)

    def test_format_price(self):
        """Testa formatação de preço."""
        assert format_price(99.90) == "R$ 99,90"
        assert format_price(1234.56) == "R$ 1.234,56"
        assert format_price(99.90, show_currency=False) == "99,90"

    def test_calculate_discount_percentage(self):
        """Testa cálculo de desconto."""
        assert calculate_discount_percentage(100, 70) == 30
        assert calculate_discount_percentage(89.90, 59.90) == 33
        assert calculate_discount_percentage(100, 100) == 0

    def test_truncate_text(self):
        """Testa truncamento de texto."""
        text = "Este é um texto muito longo que precisa ser truncado"
        assert len(truncate_text(text, 20)) <= 20
        assert truncate_text(text, 20).endswith("...")
        assert truncate_text("Curto", 20) == "Curto"


class TestColorProcessor:
    """Testes para processador de cores."""

    def test_initialization(self):
        """Testa inicialização do processador."""
        colors = ["#FF6B6B", "#4ECDC4"]
        processor = ColorProcessor(colors)
        assert len(processor.primary_colors_rgb) == 2
        assert processor.get_primary_color(0) == (255, 107, 107)

    def test_get_complementary_color(self):
        """Testa geração de cor complementar."""
        processor = ColorProcessor(["#FF0000"])
        red = (255, 0, 0)
        comp = processor.get_complementary_color(red)
        assert comp == (0, 255, 255)  # Ciano

    def test_get_lighter_shade(self):
        """Testa geração de tom mais claro."""
        processor = ColorProcessor(["#000000"])
        black = (0, 0, 0)
        lighter = processor.get_lighter_shade(black, 0.5)
        # Tom mais claro deve ter valores maiores
        assert all(c > 0 for c in lighter)

    def test_get_darker_shade(self):
        """Testa geração de tom mais escuro."""
        processor = ColorProcessor(["#FFFFFF"])
        white = (255, 255, 255)
        darker = processor.get_darker_shade(white, 0.5)
        # Tom mais escuro deve ter valores menores
        assert all(c < 255 for c in darker)


class TestIntegration:
    """Testes de integração básicos."""

    def test_assets_exist(self):
        """Verifica se assets de teste existem."""
        assert os.path.exists("assets/examples/logo_moda.png")
        assert os.path.exists("assets/examples/produto_camiseta.png")
        assert os.path.exists("assets/examples/test_case_1_moda.json")

    def test_output_directory_structure(self):
        """Verifica se diretórios de output existem."""
        assert os.path.exists("output")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
