from funcs import metricas, cargar_dataset
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
#from sklearn.metrics import confusion_matrix
import plotly.express as px
from json import dumps
from plotly.utils import PlotlyJSONEncoder

# vble global
RANDOM_STATE = 123

def predict_linealmodels():
    '''
    Prediccion con modelos lineales con parametros por defecto,
    crea dataframe para comparar metricas de cada modelo
    '''
    X_train, X_val, X_test, y_train, y_val, y_test, selected_vars = cargar_dataset()

    classifiers = [
        ('Regresión Logística', LogisticRegression(random_state=RANDOM_STATE)),
        ('Descenso del gradiente estocástico', SGDClassifier(random_state=RANDOM_STATE))
    ]
    
    results = []

    for clf_name, clf in classifiers:
        clf.fit(X_train, y_train)
        y_val_pred = clf.predict(X_val)
        accuracy, recall, f1, precision = metricas(y_val, y_val_pred)
        
        results.append({
            'Model': clf_name,
            'Accuracy': accuracy,
            'Recall': recall,
            'F1-score': f1,
            'Precision': precision
        })

    confusion_matrices = 0
    dframe = pd.DataFrame(results)
    fig = px.bar(dframe, x='Model', y=['Accuracy', 'Recall', 'F1-score', 'Precision'], barmode='group')
    fig = fig.update_layout(
            title='Métricas por Modelo',
            xaxis=dict(title='Modelo'),
            yaxis=dict(title='Porcentaje'),
            title_x=0.5
        )
    
    graphJSON_m = dumps(fig, cls=PlotlyJSONEncoder)
    
    classes = 'table table-bordered-ml table-hover table-sm'
    dframe = dframe.to_html(classes=classes)
    
    #cm = confusion_matrix(y_val, y_val_pred_lr)
    return dframe, selected_vars, confusion_matrices, graphJSON_m


def predict_tree():
    X_train, X_val, X_test, y_train, y_val, y_test, selected_vars = cargar_dataset()

    clf = DecisionTreeClassifier(random_state=RANDOM_STATE)
    clf.fit(X_train, y_train)
    y_val_pred = clf.predict(X_val)
    accuracy, recall, f1, precision = metricas(y_val, y_val_pred)

    results = {
        #'Métricas': 'Decision Tree',
        'Accuracy': accuracy,
        'Recall': recall,
        'F1-score': f1,
        'Presicion': precision,
    }

   
    dframe_a = pd.DataFrame(results, index=['Metrics'])
    colors = ['blue', 'green', 'red', 'orange']
    
    fig = px.bar(
        dframe_a.transpose(),
        x=dframe_a.columns,  
        y='Metrics',
        color_discrete_sequence=colors, 
        labels={'index': 'Variables', 'Metrics': 'Valor'}  #
    )
    
    fig = fig.update_layout(
        title='Métricas del Modelo',
        xaxis=dict(title='Métricas'),
        yaxis=dict(title='Porcentaje'),
        title_x=0.5
    )

    
    graphJSON_dt = dumps(fig, cls=PlotlyJSONEncoder)
    classes = 'table table-bordered-arboles table-hover table-sm'
    dframe_a = dframe_a.to_html(classes=classes)

    return dframe_a, selected_vars, graphJSON_dt


def predict_rf():
    X_train, X_val, X_test, y_train, y_val, y_test, selected_vars = cargar_dataset()

    clf = RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1) # reduces time
    clf.fit(X_train, y_train)
    y_val_pred = clf.predict(X_val)
    accuracy, recall, f1, precision = metricas(y_val, y_val_pred)

    results = {
        #'Métricas': 'Decision Tree',
        'Accuracy': accuracy,
        'Recall': recall,
        'F1-score': f1,
        'Presicion': precision,
    }
   
    dframe_rf = pd.DataFrame(results, index=['Metrics'])
    colors = ['blue', 'green', 'red', 'orange']
  
    fig = px.bar(
        dframe_rf.transpose(), 
        x=dframe_rf.columns,  
        y='Metrics',
        color_discrete_sequence=colors,  
        labels={'index': 'Variables', 'Metrics': 'Valor'}  #
    )
    
    fig = fig.update_layout(
        title='Métricas del Modelo',
        xaxis=dict(title='Métricas'),
        yaxis=dict(title='Porcentaje'),
        title_x=0.5
    )

    # Convertir a formato JSON
    graphJSON_dt = dumps(fig, cls=PlotlyJSONEncoder)
    classes = 'table table-bordered-arboles table-hover table-sm'
    dframe_rf = dframe_rf.to_html(classes=classes)

    return dframe_rf, selected_vars, graphJSON_dt