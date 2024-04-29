#from application import app
from app import app
from flask import render_template, request
from graphs import get_graphs_experiments, get_map_experiments, cb_plot, events_plot, level_plot, page_plot
from preds import predict_linealmodels, predict_tree, predict_rf
from funcs import get_year
from flask_login import login_required

'''@app.route('/index')
def index():
    return render_template('index.html')'''

@app.route("/eda_churn_nochurn")
@login_required
def eda_churn_nochurn():
    #graph1_json, graph_json, graph3_json, graph4_json = get_graphs_data()
    plot_1_json = cb_plot()
    fig_e = events_plot()
    fig_level = level_plot()
    fig_page = page_plot()
    year = get_year()
    return render_template('eda_churn_nochurn.html', 
                           plot_1_json=plot_1_json, 
                           fig_e=fig_e, 
                           fig_level=fig_level,
                           fig_page=fig_page,
                           current_year=year)


@app.route("/modelos")
@login_required
def modelos():
    graphJSON_allplots = get_graphs_experiments()
    graph_map = get_map_experiments()
    year = get_year()
    return render_template("modelos.html", 
                           graphJSON_allplots=graphJSON_allplots, 
                           graph_map=graph_map, 
                           current_year=year)


@app.route("/predicciones_modeloslineales")
@login_required
def predicciones_modeloslineales():
    year = get_year()
    return render_template("predicciones_modeloslineales.html", current_year=year) 


# al hacer la prediccion
@app.route('/predict', methods=['POST'])
@login_required
def predict():
    dframe, selected_vars, confusion_matrices, graphJSON_m  = predict_linealmodels()
    return render_template('predicciones_modeloslineales.html',  
                           dframe=dframe,
                           selected_vars=selected_vars, 
                           confusion_matrices=confusion_matrices, 
                           graphJSON_m=graphJSON_m)  


@app.route("/predicciones")
@login_required
def predicciones():
    year = get_year()
    return render_template("predicciones.html", current_year=year)


@app.route("/predicciones_modelosarboles")
@login_required
def predicciones_modelosarboles():
    year = get_year()
    return render_template("predicciones_modelosarboles.html", current_year=year)


@app.route('/predict_a', methods=['POST'])
@login_required
def predict_a():
    year = get_year()
    selected_model = request.form['model_selection']
    if selected_model == 'tree':
        dframe_a, selected_vars, graphJSON_dt = predict_tree()
    elif selected_model == 'rf':
        dframe_a, selected_vars, graphJSON_dt = predict_rf()
    else:
        return "Unknown model selection"
    
    return render_template('predicciones_modelosarboles.html', 
                           dframe_a=dframe_a, 
                           selected_vars=selected_vars, 
                           graphJSON_dt=graphJSON_dt,
                           current_year=year)

