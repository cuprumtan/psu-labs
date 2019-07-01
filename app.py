# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


def get_subjects():
    list = {"1":"Трехфазные цепи",
            "2":"Фильтры. Генераторы. Амплитудно – частотная характеристика. Фаза - частотная характеристика.",
            "3":"Элементы электрической цепи",
            "4":"Цепи при гармоническом воздействии"}
    return list


@app.route('/')
def root():
    return redirect(url_for('test_begin'))


@app.route('/begin', methods=['GET', 'POST'])
def test_begin():
    list = get_subjects()
    return render_template('start.html', subjects=list)


@app.route('/testing', methods=['POST'])
def testing():
    if request.method == 'POST':
        print(str(request.form['fio']))
        print(str(request.form['group']))
        print(str(request.form['course']))
        print(str(request.form['count']))
    return render_template('testing.html')


@app.route('/result', methods=['POST'])
def test_result():
    return render_template('result.html')


@app.route('/manage', methods=['GET', 'POST'])
def manage_server():
    return render_template('server.html')


if __name__ == '__main__':
    app.run()
