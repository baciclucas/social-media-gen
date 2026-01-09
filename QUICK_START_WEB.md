# Guia Rápido - Interface Web

## Iniciar a Interface

### Opção 1: Script Automático (Linux/Mac)
```bash
./run_web.sh
```

### Opção 2: Comando Direto
```bash
streamlit run app.py
```

### Opção 3: Python
```bash
python -m streamlit run app.py
```

## Acessar de Dispositivos Móveis

### Na Mesma Rede WiFi

1. No terminal, após iniciar o servidor, você verá:
   ```
   Network URL: http://192.168.x.x:8501
   ```

2. No seu celular/tablet, abra o navegador e acesse o endereço mostrado

### Usando Túnel (Para Acesso Remoto)

Se quiser acessar de qualquer lugar (útil para demonstrações):

```bash
# Instale o localtunnel
npm install -g localtunnel

# Em outro terminal, após iniciar o Streamlit
lt --port 8501
```

Você receberá uma URL pública tipo: `https://your-url.loca.lt`

## Como Usar a Interface

### Passo a Passo

1. **Upload de Arquivos**
   - Faça upload do logo da loja (PNG, JPG)
   - Faça upload da foto do produto (PNG, JPG)

2. **Cores da Marca**
   - Escolha 2-3 cores usando os color pickers
   - As cores serão usadas em todos os criativos

3. **Informações da Loja**
   - Digite o nome da loja

4. **Informações do Produto**
   - Nome do produto
   - Descrição curta (até 100 caracteres)
   - Preço original
   - Marque "Produto em promoção?" se houver desconto
   - Se em promoção, informe o preço promocional
   - Escolha o CTA (Call-to-Action)

5. **Configurações Avançadas (Opcional)**
   - Se tiver uma API key da Anthropic, cole aqui
   - Caso contrário, deixe em branco (usará textos padrão)

6. **Gerar**
   - Clique em "🚀 Gerar Criativos"
   - Aguarde alguns segundos
   - Visualize os 8 criativos gerados
   - Baixe individualmente ou todos em ZIP

## Recursos da Interface

### 📱 Mobile-First
- Interface otimizada para celular
- Funciona perfeitamente em tablets e desktops
- Design responsivo que se adapta ao tamanho da tela

### 🎨 Visualização em Tabs
- Instagram Feed
- Instagram Story
- Facebook Ads
- Web Banner

### ⬇️ Download Fácil
- Baixar cada criativo individualmente
- Baixar todos de uma vez em ZIP

### ✨ Interatividade
- Preview instantâneo do logo e produto
- Seletores de cor visuais
- Validação em tempo real
- Feedback visual claro

## Dicas de Uso

### Para Melhores Resultados

**Logo:**
- Use PNG com fundo transparente
- Resolução mínima: 400x400px
- Formato quadrado ou horizontal

**Foto do Produto:**
- Use imagens de alta qualidade
- Fundo limpo (branco de preferência)
- Produto bem iluminado
- Resolução mínima: 800x800px

**Cores:**
- Escolha cores que contrastem bem
- Use cores da identidade visual da marca
- Teste diferentes combinações

**Descrição:**
- Seja conciso e direto
- Destaque o principal benefício
- Use palavras que vendem

## Problemas Comuns

### Página não carrega
```bash
# Verifique se o Streamlit está instalado
pip install streamlit

# Verifique se o servidor está rodando
# Deve aparecer "You can now view your Streamlit app in your browser."
```

### Erro ao fazer upload
- Verifique o formato da imagem (PNG, JPG, JPEG)
- Verifique o tamanho do arquivo (máx. 200MB)
- Tente converter a imagem para PNG

### Criativos não geram
- Verifique se todos os campos obrigatórios estão preenchidos
- Verifique o console para mensagens de erro
- Tente recarregar a página (F5)

### API Key não funciona
- Verifique se a chave está correta
- O sistema funciona sem API key (com textos padrão)
- Erro de API? Deixe em branco e use fallback

## Atalhos de Teclado (Desktop)

- `R` - Recarregar aplicação
- `Ctrl/Cmd + K` - Abrir menu de comandos
- `Ctrl/Cmd + Shift + R` - Limpar cache e recarregar

## Parar o Servidor

Pressione `Ctrl + C` no terminal onde o Streamlit está rodando.

## Recursos Adicionais

### Documentação Completa
Veja `README.md` para documentação técnica completa.

### Exemplos
Teste com os casos de exemplo em `assets/examples/`:
- test_case_1_moda.json
- test_case_2_beleza.json
- test_case_3_tech.json

### Suporte
Para dúvidas ou problemas, consulte o README.md ou entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido por Komea - Rede de Agentes de IA da Loja Integrada**
