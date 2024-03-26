from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from flask import request
import os
from pandas import read_csv
import datetime

def read_file(path):
    csv_path = os.path.abspath(path)
    df = read_csv(csv_path)
    return df


def cargar_dataset():
    '''
    Obtiene las variables seleccionadas del formulario,
    divide en tres conjuntos para el entrenamiento
    '''
    selected_vars = request.form.getlist('selected_vars')

    dataset = read_file('static/dataset/df_modelos.csv')
    X = dataset[selected_vars]
    y = dataset.churn_user

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42, stratify=y_train)
    return X_train, X_val, X_test, y_train, y_val, y_test, selected_vars


def metricas(y_true, y_pred):
    ''' Funcion para calcular metricas de modelos'''
    accuracy = round(accuracy_score(y_true, y_pred), 2)
    recall = round(recall_score(y_true, y_pred), 2)
    f1 = round(f1_score(y_true, y_pred), 2)
    precision = round(precision_score(y_true, y_pred), 2)
    return accuracy, recall, f1, precision

def get_year():
    return datetime.datetime.now().year
