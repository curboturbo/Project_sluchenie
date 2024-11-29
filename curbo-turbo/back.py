from flask import Flask, render_template, send_from_directory
from flask import *
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("mainpage.html")


@app.route('/finance')
def finance():
    folder_path = 'templates/finances'  
    link_to_page = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):  
            link_to_page.append(filename)
    print(len(link_to_page))
    return render_template("finance.html", articles=link_to_page)


@app.route('/finances/<filename>')
def get_finance_file(filename):
    folder_path = 'templates/finances'  
    try:
        return send_from_directory(folder_path, filename)
    except FileNotFoundError:
        return "Файл не найден", 404
   

@app.route('/cook')
def cook():
    folder_path = 'templates/cooks'  
    links = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):  
            links.append(filename)

    return render_template("cook.html", a=links)


@app.route('/cooks/<filename>')
def get_cook_file(filename):
    folder_path = 'templates/cooks'  
    try:
        return send_from_directory(folder_path, filename)
    except FileNotFoundError:
        return "Файл не найден", 404


@app.route('/hel')
def health():
    folder_path = 'templates/health'  
    links = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):  
            links.append(filename)

    return render_template("hel.html", a=links)


@app.route('/health/<filename>')
def get_health_file(filename):
    folder_path = 'templates/health'  
    try:
        return send_from_directory(folder_path, filename)
    except FileNotFoundError:
        return "Файл не найден", 404


@app.route('/home')
def house():
    folder_path = 'templates/house'  
    link_to_page = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):  
            link_to_page.append(filename)
    print(len(link_to_page))
    return render_template("home.html", a=link_to_page)


@app.route('/house/<filename>')
def get_house_file(filename):
    folder_path = 'templates/house'  
    try:
        return send_from_directory(folder_path, filename)
    except FileNotFoundError:
        return "Файл не найден", 404


if __name__ == '__main__':
    app.run(debug=True)