from funcs import read_file, read_file_pl
from json import dumps
from plotly.utils import PlotlyJSONEncoder
from plotly.express import bar, box, histogram, imshow
from plotly.subplots import make_subplots
from pandas import DataFrame
import polars as pl
import plotly.graph_objects as go

'''def get_graphs_data():

    df_clean = read_file('static/dataset/df_churn_cleaned.csv') 
    
    # first fig
    #fig = go.Figure(data=[go.Bar(x=value_counts.index, y=value_counts.values)])
    value_counts = round(df_clean['churn_user'].value_counts(normalize=True), 2)
    colors = ['#36739B', '#F0472C']
    fig1 = bar(df_clean, x=value_counts.index, y=value_counts.values)
    # Personalizar el diseño del gráfico
    fig1 = fig1.update_traces(marker_color=colors)
    fig1 = fig1.update_layout(
        title='Balance de clases',
        xaxis=dict(title='Clase'),
        yaxis=dict(title='Porcentaje'),
        title_x=0.5
    )
    # second 
    # divido el dataset en cada clase para comparar comportamiento
    is_churn = df_clean['churn_user'] == 1
    churn_df = df_clean[is_churn] #df where users are churn
    not_churn_df = df_clean[~is_churn] #df where users are NOT churn.
    #grupos para grafico
    churn_leveltype = round(churn_df.groupby('userId', as_index=False).agg({'level': 'first'})['level'].value_counts(normalize=True), 2)
    nochurn_leveltype = round(not_churn_df.groupby('userId', as_index=False).agg({'level': 'first'})['level'].value_counts(normalize=True), 2)
    df = DataFrame({"Churn Users":churn_leveltype,"No Churn Users":nochurn_leveltype})
    fig = bar(df, barmode = 'group')
    fig = fig.update_layout(
        title='Nivel de Usuarios',
        xaxis=dict(title='Nivel de usuario (Gratuito o Pago)'),
        yaxis=dict(title='Porcentaje'),
        title_x=0.5
    )
    # third 
    interesting_events = ['Thumbs Up', 'Thumbs Down', 'Add to Playlist', 'Roll Advert', 'Add Friend', 'Error']
    #Para usuarios que hicieron churn:
    churn_events = churn_df[churn_df.page.isin(interesting_events)]
    churn_events = round(churn_events.groupby('userId', as_index=False).agg({'page': 'first'})['page'].value_counts(normalize=True), 2)
    #Para usuarios No churn:
    not_churn_events = not_churn_df[not_churn_df.page.isin(interesting_events)]
    not_churn_events = round(not_churn_events.groupby('userId', as_index=False).agg({'page': 'first'})['page'].value_counts(normalize=True), 2)
    df_events = DataFrame({"Churn Users":churn_events,"No Churn Users":not_churn_events})
    df_events = df_events.sort_values(by=["Churn Users", "No Churn Users"], ascending=False)
    
    fig_events = bar(df_events, barmode = 'group')
    fig_events = fig_events.update_layout(
            title='Tipos de eventos',
            xaxis=dict(title='Evento'),
            yaxis=dict(title='Porcentaje'),
            title_x=0.5
        )
    # fourth 
    churn_add = churn_df[(churn_df['page'] == 'Roll Advert') & (churn_df['userId'] != '')].groupby('userId')['page'].count().reset_index().page;
    not_churn_add = not_churn_df[(not_churn_df['page'] == 'Roll Advert') & (not_churn_df['userId'] != '')].groupby('userId')['page'].count().reset_index().page;
    df_add = DataFrame({"Churn Users":churn_add,"No Churn Users":not_churn_add})
    fig_add = box(df_add, height=700)
    
    fig_add = fig_add.update_layout(
            title='Cantidad de anuncios vistos',
            xaxis=dict(title='Clase'),
            yaxis=dict(title='Cantidad'),
            title_x=0.5
        )

    # Convertir los gráficos a formato JSON
    graph1_json = dumps(fig1, cls=PlotlyJSONEncoder)
    graph_json = dumps(fig, cls=PlotlyJSONEncoder)
    graph3_json = dumps(fig_events, cls=PlotlyJSONEncoder)
    graph4_json = dumps(fig_add, cls=PlotlyJSONEncoder)
    return graph1_json, graph_json, graph3_json, graph4_json'''


def get_graphs_data_eda():
    '''
    Graficos de exploracion de variables 
    '''
    df_clean = read_file()

    fig2 = histogram(df_clean, x="date")
    fig2 = fig2.update_layout(
        title='Registros por Fecha',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Recuento')
    )

    graph2_json = dumps(fig2, cls=PlotlyJSONEncoder)
    return graph2_json


def get_graphs_experiments():
    data = {
    'Modelos': ['DM', 'LR', 'SGD', 'SVM', 'DT', 'RF', 'GB'],
    'Validation Accuracy': [0.50, 0.57, 0.53, 0.57, 0.99, 0.99, 0.91],
    'Validation Precision': [0.50, 0.56, 0.52, 0.56, 0.99, 0.98, 0.87],
    'Validation Recall': [0.50, 0.64, 0.73, 0.63, 0.99, 0.99, 0.97],
    'Validation F1': [0.50, 0.59, 0.61, 0.59, 0.99, 0.99, 0.92]
    }

    df = DataFrame(data)
    fig = make_subplots(rows=1, cols=4, subplot_titles=('Accuracy', 'Precision', 'Recall', 'F1-Score'))

    
    fig_accuracy = bar(df, x='Modelos', y='Validation Accuracy', color='Modelos')
    fig_precision = bar(df, x='Modelos', y='Validation Precision', color='Modelos')
    fig_recall = bar(df, x='Modelos', y='Validation Recall', color='Modelos')
    fig_f1 = bar(df, x='Modelos', y='Validation F1', color='Modelos')

    
    for fig_bar, subplot_num in zip([fig_accuracy, fig_precision, fig_recall, fig_f1], range(1, 5)):
        for trace in fig_bar.data:
            fig.add_trace(trace, row=1, col=subplot_num)

    
    fig.update_layout(showlegend=False, 
                        height=450, 
                        width=1100,
                        title_text="Evaluación de los modelos",
                        title_font=dict(size=24, color="rgb(12, 26, 71)"),
                        plot_bgcolor='rgba(0,0,0,0)',  
                        title_x=0.5
                    )
    fig.update_xaxes(tickangle=45)
    graphJSON_allplots = dumps(fig, cls=PlotlyJSONEncoder)
    
    return graphJSON_allplots

def get_map_experiments():
    df_churn_clean = read_file('static/dataset/df_modelos.csv') 
    corr_matrix = df_churn_clean.corr()

    fig = imshow(corr_matrix,
                    labels=dict(color='Correlation'),
                    x=corr_matrix.columns,
                    y=corr_matrix.columns)
    fig = fig.update_layout(
        title='Gráfico de Correlaciones',
        title_x=0.5,
        width=900,  
        height=600  
    )
    
    graph_map = dumps(fig, cls=PlotlyJSONEncoder)
    return graph_map


def get_c():
    '''
    returns dfs
    '''
    df = read_file_pl()
    is_churn = df['churn_user'] == 1
    churn_df_pl = df.filter(is_churn)
    not_churn_df_pl = df.filter(pl.col("churn_user") != 1)
    return churn_df_pl, not_churn_df_pl

def cb_plot():
    '''
    char plot Classes Balance 
    '''
    df = read_file_pl()
    grouped_df = df.group_by('churn_user').agg(pl.count('churn_user').alias('count'))
    grouped_dict = grouped_df.to_dict()
    labels = grouped_dict['churn_user']
    values = grouped_dict['count']
    
    plot_1 = go.Figure(data=[go.Pie(labels=labels, values=values)])
    plot_1 = plot_1.update_layout(
             title='Balance de clases',
             title_x=0.5,
             template="ggplot2"
            )
    plot_1_json = dumps(plot_1, cls=PlotlyJSONEncoder)
    return plot_1_json
    
def events_plot():
    '''
    bar plot Events Types
    '''
    churn_df_pl, not_churn_df_pl = get_c()
    interesting_events = ['Thumbs Up', 'Thumbs Down', 'Add to Playlist', 'Roll Advert', 'Add Friend', 'Error']
    # churn df
    churn_events_pl = churn_df_pl.filter(pl.col("page").is_in(interesting_events))
    churn_events_pl = churn_events_pl.group_by('userId').agg(pl.col('page').first().alias('first_page')).select(pl.col('first_page'))
    churn_events_pl = churn_events_pl['first_page'].value_counts(sort=True)
    relative_col = churn_events_pl['count'] / churn_events_pl['count'].sum()
    churn_events_pl = churn_events_pl.with_columns(c=relative_col)
    # not churn df
    not_churn_events_pl = not_churn_df_pl.filter(pl.col("page").is_in(interesting_events))
    not_churn_events_pl = not_churn_events_pl.group_by('userId').agg(pl.col('page').first().alias('first_page')).select(pl.col('first_page'))
    not_churn_events_pl = not_churn_events_pl['first_page'].value_counts(sort=True)
    relative_col_nc = not_churn_events_pl['count'] / not_churn_events_pl['count'].sum()
    not_churn_events_pl = not_churn_events_pl.with_columns(c=relative_col_nc)
    # join
    events_df = churn_events_pl.join(not_churn_events_pl, on='first_page', suffix='_churn_events_pl', how='inner')
    # plot 
    fig_e = go.Figure()
    fig_e.add_trace(go.Bar(x=events_df['first_page'], y=events_df['c'], name='Churn'))
    fig_e.add_trace(go.Bar(x=events_df['first_page'], y=events_df['c_churn_events_pl'], name='Not churn'))

    fig_e = fig_e.update_layout(
                barmode='group', 
                title='Tipos de eventos',
                xaxis=dict(title='eventos'),
                yaxis=dict(title='Conteo'),
                title_x=0.5,
                template="ggplot2"
                )
    fig_e = dumps(fig_e, cls=PlotlyJSONEncoder)
    return fig_e

def level_plot():
    '''
    bar plot level types 
    '''
    churn_df_pl, not_churn_df_pl = get_c()
    churn_percentage = churn_df_pl.group_by('level').agg(pl.count('churn_user') / churn_df_pl['level'].count())
    nc_p = not_churn_df_pl.group_by('level').agg(pl.count('churn_user') / not_churn_df_pl['level'].count())
    nc_p = nc_p.rename({"churn_user": "nochurn_user"})
    level_df = churn_percentage.join(nc_p, on='level', suffix='_churn_percentage', how='inner')

    fig_level = go.Figure()
    fig_level.add_trace(go.Bar(x=level_df['level'], y=level_df['churn_user'], name='Churn'))
    fig_level.add_trace(go.Bar(x=level_df['level'], y=level_df['nochurn_user'], name='Not churn'))

    fig_level.update_layout(
        barmode='group',  
        title='Nivel de Usuarios (Gratuito o Pago)',
        xaxis=dict(title='level'),
        yaxis=dict(title='percentage'),
        title_x=0.5,
        template="ggplot2"
    )
    fig_level = dumps(fig_level, cls=PlotlyJSONEncoder)
    return fig_level

def page_plot():
    '''
    box plot roll advert
    '''
    churn_df_pl, not_churn_df_pl = get_c()
    churn_filtered = churn_df_pl.filter((pl.col('page') == 'Roll Advert') & (pl.col('userId').is_not_null()))
    churn_grouped = churn_filtered.group_by('userId').agg(pl.count('page').alias('page_count'))
    churn_page_count = churn_grouped.select(['userId', 'page_count'])
    nc_filtered = not_churn_df_pl.filter((pl.col('page') == 'Roll Advert') & (pl.col('userId').is_not_null()))
    nc_grouped = nc_filtered.group_by('userId').agg(pl.count('page').alias('page_count_nc'))
    nc_page_count = nc_grouped.select(['userId', 'page_count_nc'])
    p_df = churn_page_count.join(nc_page_count, on='userId', suffix='_churn_page_count', how='outer')
    p_df = p_df.select(['page_count', 'page_count_nc'])

    fig_page = go.Figure()
    fig_page.add_trace(go.Box(y=p_df['page_count'], name='C'))
    fig_page.add_trace(go.Box(y=p_df['page_count_nc'], name='NC'))

    fig_page = fig_page.update_layout(
                title='Cantidad de anuncios vistos',
                xaxis=dict(title='Clase'),
                yaxis=dict(title='Cantidad'),
                height=700,
                title_x=0.5, 
                template="ggplot2"
    )

    fig_page = dumps(fig_page, cls=PlotlyJSONEncoder)
    return fig_page