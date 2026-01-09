"""
Interface Web Mobile-First para o Gerador de Criativos.
Desenvolvido com Streamlit para fácil uso em dispositivos móveis.
"""
import streamlit as st
import os
import json
import tempfile
import zipfile
from datetime import datetime
from PIL import Image
import io

from src.main import CreativeGenerator

# Configuração da página
st.set_page_config(
    page_title="Gerador de Criativos - Komea",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para mobile-first
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .main {
        padding: 1rem;
    }

    .stButton>button {
        width: 100%;
        background-color: #FF6B6B;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
    }

    .stButton>button:hover {
        background-color: #FF5252;
    }

    /* Header */
    .header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    .header h1 {
        margin: 0;
        font-size: 1.8rem;
    }

    .header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }

    /* Cards */
    .card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }

    /* Color picker container */
    .color-picker {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    /* Success message */
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    /* Image grid */
    .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .header h1 {
            font-size: 1.5rem;
        }

        .image-grid {
            grid-template-columns: 1fr;
        }
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Inicialização do session state
if 'generated_files' not in st.session_state:
    st.session_state.generated_files = None
if 'output_dir' not in st.session_state:
    st.session_state.output_dir = None

def create_header():
    """Cria o header da aplicação."""
    st.markdown("""
    <div class="header">
        <h1>🎨 Gerador de Criativos</h1>
        <p>Crie anúncios profissionais para suas redes sociais</p>
    </div>
    """, unsafe_allow_html=True)

def save_uploaded_file(uploaded_file):
    """Salva arquivo enviado temporariamente."""
    if uploaded_file is not None:
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

def create_zip_download(output_dir):
    """Cria arquivo ZIP com todos os criativos."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename in os.listdir(output_dir):
            if filename.endswith('.png'):
                file_path = os.path.join(output_dir, filename)
                zip_file.write(file_path, filename)
    zip_buffer.seek(0)
    return zip_buffer

def main():
    """Função principal da aplicação."""
    create_header()

    # Instruções
    with st.expander("ℹ️ Como usar", expanded=False):
        st.markdown("""
        **Passo a passo:**
        1. Faça upload do logo da sua loja
        2. Faça upload da foto do produto
        3. Escolha 2-3 cores da sua marca
        4. Preencha as informações do produto
        5. Clique em "Gerar Criativos"

        **O sistema vai gerar:**
        - 2 criativos para Instagram Feed (1080x1080)
        - 2 criativos para Instagram Story (1080x1920)
        - 2 criativos para Facebook Ads (1200x628)
        - 2 criativos para Banner Web (1200x400)

        Total: **8 criativos profissionais!**
        """)

    # Seção 1: Upload de Arquivos
    st.markdown("### 📁 1. Arquivos")

    col1, col2 = st.columns(2)

    with col1:
        logo_file = st.file_uploader(
            "Logo da Loja",
            type=['png', 'jpg', 'jpeg'],
            help="Sua logo em alta resolução",
            key="logo"
        )
        if logo_file:
            st.image(logo_file, caption="Logo carregado", use_container_width=True)

    with col2:
        product_file = st.file_uploader(
            "Foto do Produto",
            type=['png', 'jpg', 'jpeg'],
            help="Foto do produto em boa qualidade",
            key="product"
        )
        if product_file:
            st.image(product_file, caption="Produto carregado", use_container_width=True)

    # Seção 2: Cores da Marca
    st.markdown("### 🎨 2. Cores da Marca")
    st.caption("Escolha de 2 a 3 cores que representam sua marca")

    col1, col2, col3 = st.columns(3)

    with col1:
        color1 = st.color_picker("Cor Primária", "#FF6B6B", key="color1")
    with col2:
        color2 = st.color_picker("Cor Secundária", "#4ECDC4", key="color2")
    with col3:
        color3 = st.color_picker("Cor Terciária", "#45B7D1", key="color3")

    # Seção 3: Informações da Marca
    st.markdown("### 🏪 3. Informações da Loja")

    brand_name = st.text_input(
        "Nome da Loja",
        placeholder="Ex: Minha Loja",
        help="Nome que aparecerá nos criativos"
    )

    # Seção 4: Informações do Produto
    st.markdown("### 📦 4. Informações do Produto")

    product_name = st.text_input(
        "Nome do Produto",
        placeholder="Ex: Camiseta Premium",
        help="Nome atrativo do produto"
    )

    product_description = st.text_area(
        "Descrição Curta",
        placeholder="Ex: 100% algodão, confortável e durável",
        help="Descreva os principais benefícios (máx. 60 caracteres)",
        max_chars=100
    )

    col1, col2 = st.columns(2)

    with col1:
        price_original = st.number_input(
            "Preço Original (R$)",
            min_value=0.0,
            value=99.90,
            step=0.10,
            format="%.2f"
        )

    with col2:
        has_discount = st.checkbox("Produto em promoção?")

        if has_discount:
            price_promotional = st.number_input(
                "Preço Promocional (R$)",
                min_value=0.0,
                value=69.90,
                step=0.10,
                format="%.2f"
            )
        else:
            price_promotional = None

    # Tipo de campanha
    campaign_type = "promotional" if has_discount else "standard"

    # CTA customizado
    cta_options = {
        "promotional": ["Compre Agora!", "Aproveite!", "Garanta o Seu!", "Oferta Limitada!"],
        "standard": ["Compre Agora", "Saiba Mais", "Confira", "Ver Produto"]
    }

    cta = st.selectbox(
        "Call-to-Action (CTA)",
        options=cta_options[campaign_type],
        help="Frase de chamada para ação"
    )

    # Configurações da API (opcional)
    with st.expander("⚙️ Configurações Avançadas (Opcional)"):
        api_key = st.text_input(
            "Chave da API Anthropic",
            type="password",
            help="Deixe em branco para usar textos padrão",
            placeholder="sk-ant-..."
        )
        st.caption("💡 Com a API, os textos serão gerados por IA. Sem ela, usaremos textos padrão.")

    # Botão de gerar
    st.markdown("---")

    # Validação
    can_generate = all([
        logo_file is not None,
        product_file is not None,
        brand_name.strip() != "",
        product_name.strip() != ""
    ])

    if not can_generate:
        st.warning("⚠️ Preencha todos os campos obrigatórios antes de gerar os criativos.")

    if st.button("🚀 Gerar Criativos", disabled=not can_generate, type="primary"):
        with st.spinner("✨ Gerando seus criativos profissionais..."):
            try:
                # Salva arquivos temporariamente
                logo_path = save_uploaded_file(logo_file)
                product_path = save_uploaded_file(product_file)

                # Prepara dados
                data = {
                    "brand": {
                        "name": brand_name,
                        "logo_path": logo_path,
                        "primary_colors": [color1, color2, color3],
                        "font_name": "Arial"
                    },
                    "product": {
                        "name": product_name,
                        "image_path": product_path,
                        "price_original": price_original,
                        "price_promotional": price_promotional,
                        "description": product_description,
                        "cta": cta
                    },
                    "campaign_type": campaign_type
                }

                # Gera criativos
                generator = CreativeGenerator(api_key if api_key else None)
                result = generator.generate_creatives(data)

                # Armazena no session state
                st.session_state.generated_files = result['files']
                st.session_state.output_dir = result['output_dir']
                st.session_state.processing_time = result['processing_time']

                st.success(f"✅ Sucesso! {len(result['files'])} criativos gerados em {result['processing_time']:.2f}s")
                st.balloons()

            except Exception as e:
                st.error(f"❌ Erro ao gerar criativos: {str(e)}")
                st.exception(e)

    # Exibição dos resultados
    if st.session_state.generated_files:
        st.markdown("---")
        st.markdown("### 🎉 Seus Criativos Estão Prontos!")

        # Estatísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Criativos Gerados", len(st.session_state.generated_files))
        with col2:
            st.metric("Tempo de Processo", f"{st.session_state.processing_time:.2f}s")
        with col3:
            st.metric("Formatos", "4")

        # Download ZIP
        zip_buffer = create_zip_download(st.session_state.output_dir)
        st.download_button(
            label="📥 Baixar Todos (ZIP)",
            data=zip_buffer,
            file_name=f"criativos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip",
            use_container_width=True
        )

        # Tabs para cada formato
        tabs = st.tabs(["📱 Instagram Feed", "📲 Instagram Story", "👍 Facebook Ads", "🌐 Web Banner"])

        # Organiza arquivos por formato
        formats = {
            "instagram_feed": [],
            "instagram_story": [],
            "facebook_ad": [],
            "web_banner": []
        }

        for file_path in st.session_state.generated_files:
            filename = os.path.basename(file_path)
            for format_name in formats.keys():
                if filename.startswith(format_name):
                    formats[format_name].append(file_path)

        # Instagram Feed
        with tabs[0]:
            st.markdown("**Dimensões: 1080x1080px** - Perfeito para o feed do Instagram")
            cols = st.columns(2)
            for i, file_path in enumerate(formats["instagram_feed"]):
                with cols[i]:
                    img = Image.open(file_path)
                    st.image(img, caption=f"Variação {i+1}", use_container_width=True)
                    with open(file_path, "rb") as f:
                        st.download_button(
                            f"⬇️ Download V{i+1}",
                            f,
                            file_name=os.path.basename(file_path),
                            mime="image/png",
                            use_container_width=True,
                            key=f"download_feed_{i}"
                        )

        # Instagram Story
        with tabs[1]:
            st.markdown("**Dimensões: 1080x1920px** - Ideal para stories do Instagram")
            cols = st.columns(2)
            for i, file_path in enumerate(formats["instagram_story"]):
                with cols[i]:
                    img = Image.open(file_path)
                    st.image(img, caption=f"Variação {i+1}", use_container_width=True)
                    with open(file_path, "rb") as f:
                        st.download_button(
                            f"⬇️ Download V{i+1}",
                            f,
                            file_name=os.path.basename(file_path),
                            mime="image/png",
                            use_container_width=True,
                            key=f"download_story_{i}"
                        )

        # Facebook Ads
        with tabs[2]:
            st.markdown("**Dimensões: 1200x628px** - Otimizado para anúncios no Facebook")
            cols = st.columns(2)
            for i, file_path in enumerate(formats["facebook_ad"]):
                with cols[i]:
                    img = Image.open(file_path)
                    st.image(img, caption=f"Variação {i+1}", use_container_width=True)
                    with open(file_path, "rb") as f:
                        st.download_button(
                            f"⬇️ Download V{i+1}",
                            f,
                            file_name=os.path.basename(file_path),
                            mime="image/png",
                            use_container_width=True,
                            key=f"download_fb_{i}"
                        )

        # Web Banner
        with tabs[3]:
            st.markdown("**Dimensões: 1200x400px** - Perfeito para banners em sites")
            cols = st.columns(2)
            for i, file_path in enumerate(formats["web_banner"]):
                with cols[i]:
                    img = Image.open(file_path)
                    st.image(img, caption=f"Variação {i+1}", use_container_width=True)
                    with open(file_path, "rb") as f:
                        st.download_button(
                            f"⬇️ Download V{i+1}",
                            f,
                            file_name=os.path.basename(file_path),
                            mime="image/png",
                            use_container_width=True,
                            key=f"download_banner_{i}"
                        )

        # Botão para gerar novos criativos
        if st.button("🔄 Gerar Novos Criativos", use_container_width=True):
            st.session_state.generated_files = None
            st.session_state.output_dir = None
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>💡 Desenvolvido por <strong>Komea</strong> - Rede de Agentes de IA da Loja Integrada</p>
        <p style="font-size: 0.9rem;">v1.0.0 | POC Gerador de Criativos</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
