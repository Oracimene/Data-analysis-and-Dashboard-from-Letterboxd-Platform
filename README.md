EADME — Análise de Dados e Dashboard (Letterboxd)
📌 Sobre o Projeto

Este projeto tem como objetivo realizar uma análise exploratória de dados e desenvolver um dashboard interativo utilizando dados da plataforma Letterboxd (filmes). A proposta segue os conceitos de Data Science, aplicando tratamento de dados e visualização interativa para gerar insights relevantes.

🎯 Objetivo
Explorar um conjunto de dados de filmes
Realizar análise com Pandas
Tratar inconsistências e estruturar os dados
Criar um dashboard interativo para visualização
Gerar insights sobre filmes, diretores, estúdios e gêneros
🗂️ Estrutura do Projeto
📁 Data-analysis-and-Dashboard-from-Letterboxd
 ┣ 📄 Movie_Data_File.csv   # Base de dados
 ┣ 📄 app.py                # Aplicação do dashboard (Dash)
 ┣ 📄 dados.ipynb           # Análise exploratória
 ┣ 📁 assets/               # Recursos visuais (logo)
 ┗ 📄 README.md             # Documentação
🛠️ Tecnologias Utilizadas
Python
Pandas
Plotly
Dash
Jupyter Notebook
🔍 Etapas do Projeto
1. Coleta de Dados
Dataset contendo informações de filmes:
Título
Diretor
Avaliação média
Número de visualizações
Gêneros
Estúdios
2. Análise Exploratória
Estatísticas descritivas
Identificação de padrões
Análise de popularidade e avaliações
3. Tratamento de Dados
Separação de listas (gêneros e estúdios)
Remoção de valores inconsistentes
Explosão de colunas para análise detalhada
Filtro dinâmico baseado em relevância (quantil 75%)
4. Construção do Dashboard

O dashboard apresenta:

🎬 Top estúdios por número de visualizações
🎥 Diretores com melhor avaliação média (mín. 5 filmes)
📊 Distribuição de gêneros
⭐ Relação entre avaliações e popularidade

Recursos:

Interatividade
Filtros dinâmicos
Visualizações intuitivas
▶️ Como Executar
Instale as dependências:
pip install pandas dash plotly
Execute o projeto:
python app.py
Acesse no navegador:
http://127.0.0.1:8050/
📈 Principais Insights
Estúdios mais populares concentram maior número de visualizações
Diretores com mais filmes tendem a ter avaliações mais consistentes
Alguns gêneros possuem avaliações médias mais altas que outros
Popularidade nem sempre significa melhor avaliação
👥 Autoria

Projeto desenvolvido como atividade acadêmica para a disciplina de Interface de Software / Data Science.

✅ Conclusão

O projeto demonstra como transformar dados brutos em informações úteis através de:

Análise de dados
Tratamento eficiente
Visualização interativa

Mostrando na prática a importância da ciência de dados na tomada de decisões.
