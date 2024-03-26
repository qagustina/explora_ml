from funcs import read_file
from json import dumps
from plotly.utils import PlotlyJSONEncoder
from plotly.express import bar, box, histogram, imshow
from plotly.subplots import make_subplots
from pandas import DataFrame

def get_graphs_data():
    ''' 
    Graficos de exploracion entre churn y no churn
    '''
    df_clean = read_file('static/dataset/df_churn_cleaned.csv') 
    
    # Crear una figura de Plotly
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
    #divido el dataset en cada clase para comparar comportamiento
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

    interesting_events = ['Thumbs Up', 'Thumbs Down', 'Add to Playlist', 'Roll Advert', 'Add Friend', 'Error']
    #Para usuarios que hicieron churn:
    churn_events = churn_df[churn_df.page.isin(interesting_events)]
    churn_events = round(churn_events.groupby('userId', as_index=False).agg({'page': 'first'})['page'].value_counts(normalize=True), 2)
    #Para usuarios No churn:
    not_churn_events = not_churn_df[not_churn_df.page.isin(interesting_events)]
    not_churn_events = round(not_churn_events.groupby('userId', as_index=False).agg({'page': 'first'})['page'].value_counts(normalize=True), 2)
    df_events = DataFrame({"Churn Users":churn_events,"No Churn Users":not_churn_events})
    df_events = df_events.sort_values(by=["Churn Users", "No Churn Users"], ascending=False)
    #grafico
    fig_events = bar(df_events, barmode = 'group')
    fig_events = fig_events.update_layout(
            title='Tipos de eventos',
            xaxis=dict(title='Evento'),
            yaxis=dict(title='Porcentaje'),
            title_x=0.5
        )

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
    return graph1_json, graph_json, graph3_json, graph4_json


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
    # Convertir los gráficos a formato JSON
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

    # Crear DataFrame con los datos
    df = DataFrame(data)

    fig = make_subplots(rows=1, cols=4, subplot_titles=('Accuracy', 'Precision', 'Recall', 'F1-Score'))

    # Gráficos de barra para cada métrica
    fig_accuracy = bar(df, x='Modelos', y='Validation Accuracy', color='Modelos')
    fig_precision = bar(df, x='Modelos', y='Validation Precision', color='Modelos')
    fig_recall = bar(df, x='Modelos', y='Validation Recall', color='Modelos')
    fig_f1 = bar(df, x='Modelos', y='Validation F1', color='Modelos')

    # Agregar gráficos a los subplots
    for fig_bar, subplot_num in zip([fig_accuracy, fig_precision, fig_recall, fig_f1], range(1, 5)):
        for trace in fig_bar.data:
            fig.add_trace(trace, row=1, col=subplot_num)

    # Configurar el layout del subplot
    fig.update_layout(showlegend=False, 
                        height=450, 
                        width=1100,
                        title_text="Evaluación de los modelos",
                        title_font=dict(size=24, color="rgb(12, 26, 71)"),
                        plot_bgcolor='rgba(0,0,0,0)',  # Color de fondo del gráfico
                        #paper_bgcolor='rgb(255,255,255)',  # Color de fondo del papel
                        title_x=0.5
                    )
    fig.update_xaxes(tickangle=45)
    # Convertir el subplot a formato JSON
    graphJSON_allplots = dumps(fig, cls=PlotlyJSONEncoder)
    
    return graphJSON_allplots

def get_map_experiments():
    df_churn_clean = read_file('static/dataset/df_modelos.csv') 

    corr_matrix = df_churn_clean.corr()

    # Crear el mapa de correlación con Plotly Express
    fig = imshow(corr_matrix,
                    labels=dict(color='Correlation'),
                    x=corr_matrix.columns,
                    y=corr_matrix.columns)
    fig = fig.update_layout(
        title='Gráfico de Correlaciones',
        title_x=0.5,
        #xaxis=dict(title='Date'),
        #yaxis=dict(title='Recuento'),
        width=900,  # Ancho del gráfico
        height=600  # Alto del gráfico
    )
    # Convertir los gráficos a formato JSON
    graph_map = dumps(fig, cls=PlotlyJSONEncoder)
    return graph_map
    