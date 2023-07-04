from flask import Flask, jsonify, render_template
import pandas as pd
import json

app = Flask(__name__)

if __name__ == "__main__":
    app.run()

@app.route("/")
def index():
    return render_template("linguist.html")

@app.route("/individual.html")
def individual():
    return render_template("individual.html")

@app.route('/linguistData', methods=['GET'])
def get_linguistData():
    df = pd.read_pickle('database/fashion/fashion_linguists.pkl') 
    df = df[['name', 'locale']] 
    df.columns = ['Name', 'Locale']
    data = df.to_dict(orient='records')  # convert the dataframe to a list of dictionaries
    columns = list(df.columns)
    return jsonify({'data': data, 'columns': columns})  # return the data in JSON format

@app.route('/taskData', methods=['GET'])
def get_taskData():
    df = pd.read_pickle('database/fashion/fashion_tasks.pkl') 
    df = df[['name', 'locale', 'task_type', 'deadline', 'required_hours', 'status']]
    df.columns = ['Name', 'Locale', 'Task Type', 'Deadline', 'Required Hours', 'Status']
    data = df.to_dict(orient='records')  # convert the dataframe to a list of dictionaries
    columns = list(df.columns)
    return jsonify({'data': data, 'columns': columns})  # return the data in JSON format