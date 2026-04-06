import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.express as px
import pandas as pd
import ast

# =========================================================
# 1. CARREGAMENTO E TRATAMENTO DE DADOS
# =========================================================
df = pd.read_csv('Movie_Data_File.csv')
cores_brand = ['#FF8000', '#00E054', '#40BCF4']

# Filtro Dinâmico (Quantile 75%) para relevância de visualizações
minimo_views_dinamico = df['Watches'].quantile(0.75)

# --- TRATAMENTO: ESTÚDIOS ---
df_studios = df.assign(Studios=df['Studios'].str.split(r',\s*')).explode('Studios')
studio_stats = df_studios.groupby('Studios').agg(Total_Watches=('Watches', 'sum'), Movie_Count=('Film_title', 'count')).reset_index()
top_10_studios = studio_stats.sort_values(by='Total_Watches', ascending=False).head(10)

# --- TRATAMENTO: DIRETORES GERAL (+5 FILMES) ---
director_stats = df.groupby('Director').agg(Avg_Rating=('Average_rating', 'mean'), Movie_Count=('Film_title', 'count')).reset_index()
top_10_directors = director_stats[director_stats['Movie_Count'] > 5].sort_values(by='Avg_Rating', ascending=False).head(10)

# --- TRATAMENTO: GÊNEROS (EXPLODE PARA INTERAÇÕES) ---
df['Genres_List'] = df['Genres'].fillna('[]').apply(ast.literal_eval)
df_genres_exp = df.explode('Genres_List')
df_genres_exp['Genres_List'] = df_genres_exp['Genres_List'].str.strip()
df_genres_exp = df_genres_exp[df_genres_exp['Genres_List'] != ""]

top_genres_list = df_genres_exp['Genres_List'].value_counts().head(15).index.tolist()
df_genres_filtered = df_genres_exp[df_genres_exp['Genres_List'].isin(top_genres_list)]
ordem_generos = df_genres_filtered.groupby("Genres_List")["Average_rating"].median().sort_values(ascending=True).index.tolist()

# --- FUNÇÃO AUXILIAR PARA LIMPAR TABELAS ---
def limpar_para_tabela(dataframe):
    dff = dataframe.copy()
    cols_to_drop = [c for c in dff.columns if dff[c].apply(lambda x: isinstance(x, list)).any()]
    return dff.drop(columns=cols_to_drop, errors='ignore')

# Rankings Estáticos (Seções 6 e 7)
df_popular = df[df['Watches'] >= minimo_views_dinamico]
top_10_media = df_popular.sort_values(by=['Average_rating', 'Watches'], ascending=[False, False]).head(10).copy()
top_10_media['Ranking'] = [f"{i+1}º" for i in range(len(top_10_media))]
top_10_media_limpo = limpar_para_tabela(top_10_media)

top_10_comunidade = df.sort_values(by=['Fans', 'Average_rating'], ascending=[False, False]).head(10).copy()
top_10_comunidade['Ranking'] = [f"{i+1}º" for i in range(len(top_10_comunidade))]
top_10_comunidade_limpo = limpar_para_tabela(top_10_comunidade)

# =========================================================
# 2. CONFIGURAÇÃO DE GRÁFICOS
# =========================================================
def formatar_grafico(fig):
    fig.update_layout(
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#99AABB', margin=dict(l=20, r=80, t=20, b=20),
        xaxis=dict(showgrid=True, gridcolor='#2C3440', title=''), yaxis=dict(title='')
    )
    return fig

fig_studios = formatar_grafico(px.bar(top_10_studios, x='Total_Watches', y='Studios', orientation='h', color='Studios', color_discrete_sequence=cores_brand, text_auto='.2s', template='plotly_dark'))
fig_directors = formatar_grafico(px.bar(top_10_directors, x='Avg_Rating', y='Director', orientation='h', color='Director', color_discrete_sequence=cores_brand, text_auto='.2f', template='plotly_dark'))
fig_genres = formatar_grafico(px.box(df_genres_filtered, x='Average_rating', y='Genres_List', color='Genres_List', color_discrete_sequence=cores_brand, template='plotly_dark', points=False, category_orders={"Genres_List": ordem_generos}))

# =========================================================
# 3. LAYOUT DO DASHBOARD
# =========================================================
app = dash.Dash(__name__, title="Dashboard Letterboxd")

cores = {'fundo_tela': '#14181C', 'fundo_card': '#2C3440', 'texto_principal': '#FFFFFF', 'texto_secundario': '#99AABB', 'destaque_verde': '#00E054'}
estilo_card = {'backgroundColor': cores['fundo_card'], 'padding': '25px', 'borderRadius': '10px', 'marginBottom': '30px'}

app.layout = html.Div(
    style={'backgroundColor': cores['fundo_tela'], 'color': cores['texto_principal'], 'fontFamily': 'sans-serif', 'padding': '40px 20px'},
    children=[
        html.Div(style={'maxWidth': '900px', 'margin': '0 auto'}, children=[
            
            # --- CABEÇALHO ---
            html.Div(style={'textAlign': 'center', 'marginBottom': '40px'}, children=[
                html.Img(src=app.get_asset_url('logo.png'), style={'height': '50px', 'width': 'auto', 'marginBottom': '20px'}),
                html.H1("Dashboard Letterboxd", style={'fontSize': '3em', 'margin': '0'}),
                html.Div(style={'marginTop': '20px', 'color': cores['texto_secundario'], 'lineHeight': '1.6'}, children=[
                    html.P("O Letterboxd é uma plataforma para análises e reviews de filmes, avaliações com estrelas e resenhas."),
                    html.P("Uma ferramenta essencial para cinefília, revelando tendências em rankings e gêneros.")
                ])
            ]),

            html.Hr(style={'borderColor': cores['fundo_card'], 'marginBottom': '50px'}),

            # Seções 1, 2, 3 (Gráficos)
            html.Div(style=estilo_card, children=[html.H2("1. O Poder dos Estúdios"), html.P("Análise Gráfica dos estúdios com maiores produções.", style={'color': cores['texto_secundario']}), dcc.Graph(figure=fig_studios, config={'displayModeBar': False})]),
            
            html.Div(style=estilo_card, children=[html.H2("2. Análise de Direção Autoral"), html.P("Diretores com as maiores médias de notas (+5 filmes).", style={'color': cores['texto_secundario']}), dcc.Graph(figure=fig_directors, config={'displayModeBar': False})]),
            
            # --- NOVA SEÇÃO 3: DIRETORES POR GÊNERO ---
            html.Div(style=estilo_card, children=[
                html.H2("3. Melhores Diretores por Gênero"),
                html.P("Selecione um gênero para ver os diretores com melhor avaliação média (mínimo de 5 filmes no gênero).", style={'color': cores['texto_secundario']}),
                dcc.Dropdown(id='dropdown-diretor-genero', options=[{'label': g, 'value': g} for g in sorted(top_genres_list)], value='Drama', style={'color': '#000', 'marginBottom': '20px'}),
                dash_table.DataTable(
                    id='tabela-diretor-genero', 
                    columns=[{"name": "Ranking", "id": "Ranking"}, {"name": "Diretor", "id": "Director"}, {"name": "Média", "id": "Avg_Rating"}, {"name": "Qtd. Filmes", "id": "Movie_Count"}],
                    style_header={'backgroundColor': '#1F232B', 'color': cores['destaque_verde'], 'fontWeight': 'bold'},
                    style_cell={'backgroundColor': cores['fundo_card'], 'color': cores['texto_secundario'], 'padding': '10px'},
                )
            ]),

            html.Div(style=estilo_card, children=[html.H2("4. Distribuição por Gênero"), html.P("Análise de consistência de notas via Boxplot.", style={'color': cores['texto_secundario']}), dcc.Graph(figure=fig_genres, config={'displayModeBar': False})]),

            # Seção 5: Filmes por Gênero
            html.Div(style=estilo_card, children=[
                html.H2("5. Top 10 Filmes por Gênero"),
                dcc.Dropdown(id='genero-selector', options=[{'label': g, 'value': g} for g in sorted(top_genres_list)], value='Drama', style={'color': '#000', 'marginBottom': '20px'}),
                dash_table.DataTable(
                    id='tabela-filmes', 
                    columns=[{"name": "Pos.", "id": "Ranking"}, {"name": "Título", "id": "Film_title"}, {"name": "Nota", "id": "Average_rating"}],
                    style_header={'backgroundColor': '#1F232B', 'color': cores['destaque_verde'], 'fontWeight': 'bold'},
                    style_cell={'backgroundColor': cores['fundo_card'], 'color': cores['texto_secundario'], 'padding': '10px'},
                    style_data_conditional=[{'if': {'row_index': 0}, 'color': '#FF8000', 'fontWeight': 'bold'}]
                )
            ]),

            # Rankings Globais (Finais)
            html.Div(style=estilo_card, children=[
                html.H2("6. Top 10 Filmes Favoritos por média de estrelas"),
                html.P(f"Filtro: Top 25% em visualizações (+{int(minimo_views_dinamico)} views).", style={'fontSize': '0.85em', 'color': cores['destaque_verde']}),
                dash_table.DataTable(id='tabela-olimpo', columns=[{"name": "Pos.", "id": "Ranking"}, {"name": "Filme", "id": "Film_title"}, {"name": "Nota", "id": "Average_rating"}], data=top_10_media_limpo.to_dict('records'), style_header={'backgroundColor': '#1F232B', 'color': cores['destaque_verde']}, style_cell={'backgroundColor': cores['fundo_card'], 'color': cores['texto_secundario'], 'padding': '10px'})
            ]),

            html.Div(style=estilo_card, children=[
                html.H2("7. Top 10 Filmes favoritados pela comunidade"),
                dash_table.DataTable(id='tabela-fans', columns=[{"name": "Pos.", "id": "Ranking"}, {"name": "Filme", "id": "Film_title"}, {"name": "Fãs", "id": "Fans"}], data=top_10_comunidade_limpo.to_dict('records'), style_header={'backgroundColor': '#1F232B', 'color': cores['destaque_verde']}, style_cell={'backgroundColor': cores['fundo_card'], 'color': cores['texto_secundario'], 'padding': '10px'})
            ])
        ])
    ]
)

# --- CALLBACKS ---

# Callback 1: Diretores por Gênero
@app.callback(Output('tabela-diretor-genero', 'data'), Input('dropdown-diretor-genero', 'value'))
def update_director_table(selected_genre):
    filtered_gen = df_genres_exp[df_genres_exp['Genres_List'] == selected_genre]
    d_stats = filtered_gen.groupby('Director').agg(Avg_Rating=('Average_rating', 'mean'), Movie_Count=('Film_title', 'count')).reset_index()
    # Filtro: Apenas diretores que fizeram mais de 5 filmes NESTE gênero específico
    d_top = d_stats[d_stats['Movie_Count'] >= 5].sort_values(by='Avg_Rating', ascending=False).head(10)
    d_top['Avg_Rating'] = d_top['Avg_Rating'].round(2)
    d_top['Ranking'] = [f"{i+1}º" for i in range(len(d_top))]
    return d_top.to_dict('records')

# Callback 2: Filmes por Gênero
@app.callback(Output('tabela-filmes', 'data'), Input('genero-selector', 'value'))
def update_movie_table(selected_genre):
    filtered = df_genres_exp[(df_genres_exp['Genres_List'] == selected_genre) & (df_genres_exp['Watches'] >= minimo_views_dinamico)].copy()
    ordered = filtered.sort_values(by=['Average_rating', 'Watches'], ascending=[False, False]).head(10)
    ordered['Ranking'] = [f"{i+1}º" for i in range(len(ordered))]
    return ordered.drop(columns=['Genres_List'], errors='ignore').to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)