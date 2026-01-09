# Gerador Automático de Criativos de Mídia para E-commerce

POC (Proof of Concept) de um sistema gerador automático de criativos profissionais para redes sociais e mídia paga, desenvolvido para a Komea (rede de agentes de IA da Loja Integrada).

## Contexto

Este sistema ajuda micro e pequenos varejistas a criar conteúdo visual profissional e consistente com sua marca para divulgar produtos em:
- Instagram Feed (1080x1080)
- Instagram Story (1080x1920)
- Facebook Ads (1200x628)
- Banner Web (1200x400)

**Problema resolvido**: Lojistas iniciantes não sabem criar criativos de qualidade, o que dificulta a divulgação e atrasa a primeira venda.

## Funcionalidades

- Geração automática de 8 criativos (2 variações por formato)
- Processamento inteligente de logos e produtos
- Harmonização automática de cores
- Geração de textos persuasivos com Claude AI
- Templates minimalistas e vibrantes
- Validação de contraste para legibilidade
- Exportação em alta qualidade (PNG 95%)
- **Interface web mobile-first** para fácil uso em qualquer dispositivo

## 🌐 Interface Web

### Acesso Rápido

O sistema possui uma **interface web moderna e mobile-first** desenvolvida com Streamlit, perfeita para usar em celulares, tablets e desktops.

```bash
# Iniciar interface web
streamlit run app.py

# Ou use o script de inicialização
./run_web.sh
```

Acesse no navegador: `http://localhost:8501`

### Recursos da Interface

- 📱 **Mobile-First**: Design otimizado para celular
- 🎨 **Visual Intuitivo**: Upload de imagens por drag-and-drop
- 🎯 **Seletores de Cor**: Escolha cores da marca visualmente
- 👁️ **Preview em Tempo Real**: Veja logo e produto antes de gerar
- 📊 **Organização em Tabs**: Criativos separados por formato
- ⬇️ **Download Fácil**: Baixe individualmente ou todos em ZIP
- ✨ **Feedback Visual**: Mensagens claras e animações

### Como Acessar de Dispositivos Móveis

Na mesma rede WiFi, use o endereço exibido no terminal:
```
Network URL: http://192.168.x.x:8501
```

Para mais detalhes, veja: [QUICK_START_WEB.md](QUICK_START_WEB.md)

## Requisitos

- Python 3.10+
- Pillow (PIL)
- Anthropic API (para geração de textos)

## Instalação

### 1. Clone ou baixe o projeto

```bash
cd social-media-gen
```

### 2. (Recomendado) Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a API Key da Anthropic

Crie um arquivo `.env` na raiz do projeto:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da API:

```
ANTHROPIC_API_KEY=sua_chave_aqui
```

**Nota**: O sistema funciona sem a API key, mas os textos serão gerados de forma simplificada (fallback).

## Como Usar

### Uso Rápido - Casos de Teste

Execute um dos casos de teste incluídos:

```bash
# Caso 1: Promoção de Moda (Camiseta com 33% desconto)
python -m src.main assets/examples/test_case_1_moda.json

# Caso 2: Produto de Beleza (Creme facial sem desconto)
python -m src.main assets/examples/test_case_2_beleza.json

# Caso 3: Eletrônico em Promoção (Fone com 40% desconto)
python -m src.main assets/examples/test_case_3_tech.json
```

### Uso Programático

```python
from src.main import CreativeGenerator

# Crie o gerador
generator = CreativeGenerator(api_key="sua_chave_aqui")  # api_key é opcional

# Dados de entrada
data = {
    "brand": {
        "name": "Minha Loja",
        "logo_path": "caminho/para/logo.png",
        "primary_colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"]
    },
    "product": {
        "name": "Produto Incrível",
        "image_path": "caminho/para/produto.jpg",
        "price_original": 99.90,
        "price_promotional": 69.90,  # Opcional
        "description": "Descrição do produto",
        "cta": "Compre Agora!"  # Opcional
    },
    "campaign_type": "promotional"  # ou "standard"
}

# Gera os criativos
result = generator.generate_creatives(data)

print(f"✓ {len(result['files'])} criativos gerados em {result['output_dir']}")
print(f"✓ Tempo de processamento: {result['processing_time']:.2f}s")
```

## Estrutura do Projeto

```
social-media-gen/
├── src/
│   ├── main.py                 # Orquestração principal
│   ├── config.py              # Configurações e constantes
│   ├── processors/
│   │   ├── image_processor.py # Manipulação de imagens
│   │   ├── color_processor.py # Processamento de cores
│   │   └── text_generator.py  # Geração de textos com Claude
│   ├── templates/
│   │   ├── base_template.py   # Classe base abstrata
│   │   ├── instagram_feed.py  # Templates Instagram Feed
│   │   ├── instagram_story.py # Templates Instagram Story
│   │   ├── facebook_ad.py     # Templates Facebook Ads
│   │   └── web_banner.py      # Templates Web Banner
│   └── utils/
│       └── helpers.py         # Funções auxiliares
├── assets/
│   └── examples/              # Casos de teste
├── output/                    # Criativos gerados
├── tests/                     # Testes unitários
├── requirements.txt
├── README.md
└── .env.example
```

## Formato de Entrada (JSON)

```json
{
  "brand": {
    "name": "Nome da Loja",
    "logo_path": "path/to/logo.png",
    "primary_colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
    "font_name": "Arial"
  },
  "product": {
    "name": "Nome do Produto",
    "image_path": "path/to/product.jpg",
    "price_original": 89.90,
    "price_promotional": 59.90,
    "description": "Descrição curta do produto",
    "cta": "Compre Agora"
  },
  "campaign_type": "promotional"
}
```

### Campos Obrigatórios

**Brand:**
- `name`: Nome da loja
- `primary_colors`: Array com 1-3 cores em hexadecimal
- `logo_path`: Caminho para o logo (PNG, JPG, WEBP)

**Product:**
- `name`: Nome do produto
- `image_path`: Caminho para foto do produto
- `price_original`: Preço original

### Campos Opcionais

**Brand:**
- `font_name`: Nome da fonte (padrão: Arial)

**Product:**
- `price_promotional`: Preço promocional (ativa modo promoção)
- `description`: Descrição do produto (usado para gerar copy)
- `cta`: Call-to-action customizado (padrão: "Compre Agora")

**Raiz:**
- `campaign_type`: "promotional" ou "standard" (padrão: "standard")

## Saída

Para cada execução, o sistema gera:

### 8 Imagens PNG (qualidade 95%)
- `instagram_feed_v1.png` - Feed minimalista
- `instagram_feed_v2.png` - Feed vibrante
- `instagram_story_v1.png` - Story minimalista
- `instagram_story_v2.png` - Story vibrante
- `facebook_ad_v1.png` - Ad minimalista
- `facebook_ad_v2.png` - Ad vibrante
- `web_banner_v1.png` - Banner minimalista
- `web_banner_v2.png` - Banner vibrante

### Arquivo metadata.json
Contém informações sobre:
- Cores utilizadas
- Textos gerados para cada formato
- Tempo de processamento
- Lista de arquivos gerados

## Templates

### Minimalist (v1)
- Background claro/neutro
- Produto centralizado
- Muito espaço em branco
- Tipografia limpa
- Foco no produto

### Vibrant (v2)
- Background com cores da marca
- Layout dinâmico
- Gradientes e overlays
- Mais elementos visuais
- Impacto visual forte

## Personalização

### Adicionar Novos Formatos

1. Defina dimensões em `src/config.py`:

```python
FORMATS["novo_formato"] = (largura, altura)
```

2. Crie template herdando de `BaseTemplate`:

```python
from src.templates.base_template import BaseTemplate

class NovoFormatoMinimalist(BaseTemplate):
    def __init__(self, color_processor):
        super().__init__("novo_formato", "minimalist", color_processor)

    def generate(self, brand_data, product_data, texts, logo_image, product_image):
        # Implemente sua lógica aqui
        pass
```

3. Registre em `src/main.py`:

```python
templates_map["novo_formato"] = [
    ("v1", NovoFormatoMinimalist),
    ("v2", NovoFormatoVibrant)
]
```

### Ajustar Tamanhos de Fonte

Edite `FONT_SIZES` em `src/config.py`:

```python
FONT_SIZES["instagram_feed"]["title"] = 80  # Aumenta título
```

### Customizar Cores Padrão

Modifique `COLOR_DEFAULTS` em `src/config.py`.

## Performance

- **Objetivo**: < 60 segundos para gerar 8 criativos
- **Alcançado**: ~15-30 segundos (sem remoção de background)
- **Com rembg**: ~40-50 segundos

### Otimizações Implementadas
- Cache de fontes
- Processamento eficiente de imagens
- Reutilização de processadores

## Limitações Conhecidas

1. **Remoção de Background**: Implementada de forma básica. Para melhor resultado, instale `rembg`:
   ```bash
   pip install rembg
   ```

2. **Fontes**: O sistema tenta usar fontes do sistema. Se não encontradas, usa fonte padrão.

3. **Textos Longos**: Textos são truncados para caber nos limites. Ajuste `TEXT_LIMITS` em `config.py` se necessário.

4. **API Rate Limits**: Claude API tem limites de requisições. O sistema usa fallback se houver erro.

5. **Formatos de Imagem**: Suporta PNG, JPG, JPEG, WEBP. Outros formatos podem não funcionar.

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'PIL'"
```bash
pip install Pillow
```

### Erro: "ANTHROPIC_API_KEY não configurada"
- Configure a variável de ambiente ou use fallback (textos simples)

### Fontes não encontradas
- O sistema usa fonte padrão automaticamente
- Para melhores resultados, instale fontes TrueType no sistema

### Imagens não aparecem nos criativos
- Verifique se os caminhos estão corretos (absolutos ou relativos ao diretório de execução)
- Verifique se os formatos das imagens são suportados

## Desenvolvimento

### Executar Testes

```bash
python -m pytest tests/
```

### Adicionar Testes

Crie arquivos em `tests/` seguindo o padrão:

```python
def test_nova_funcionalidade():
    # Seu teste aqui
    pass
```

## Próximos Passos / Melhorias Futuras

- [ ] Interface web com Streamlit ou Flask
- [ ] Remoção automática de background com rembg
- [ ] Análise de contraste automática (WCAG)
- [ ] Geração de versões A/B com mais variações
- [ ] Sugestão automática de cores complementares
- [ ] Export para dimensões customizadas
- [ ] Suporte a vídeos curtos (GIF/MP4)
- [ ] Integração com bibliotecas de stock photos
- [ ] API REST para integração com outros sistemas

## Contribuindo

Este é um projeto POC. Sugestões e melhorias são bem-vindas!

## Licença

Este projeto é uma POC desenvolvida para demonstração. Consulte os proprietários para uso comercial.

## Autoria

Desenvolvido como POC para a Komea - Rede de Agentes de IA da Loja Integrada.

## Contato

Para dúvidas ou sugestões sobre este projeto, entre em contato com a equipe de desenvolvimento.

---

**Status**: POC Funcional ✓
**Versão**: 1.0.0
**Data**: 2026-01
**Python**: 3.10+
