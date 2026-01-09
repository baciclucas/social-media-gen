#!/bin/bash
# Script para iniciar a interface web do gerador de criativos

echo "🎨 Iniciando Gerador de Criativos - Interface Web"
echo "================================================="
echo ""
echo "A interface será aberta automaticamente no seu navegador."
echo "Para acessar de dispositivos móveis na mesma rede, use:"
echo "http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "Pressione Ctrl+C para parar o servidor."
echo ""

streamlit run app.py --server.port=8501 --server.address=0.0.0.0
