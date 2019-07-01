# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model import CeSubjects


app = Flask(__name__)

engine = create_engine('sqlite:///circuit-engineering.db', encoding='utf-8')
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
def root():
    return redirect(url_for('test_begin'))


@app.route('/info', methods=['GET', 'POST'])
def test_begin():
    subjects_dict = {}
    subjects_data = session.query(CeSubjects.id, CeSubjects.subject_name).all()
    session.commit()
    for x in range(len(subjects_data)):
        subjects_dict[subjects_data[x].id] = subjects_data[x].subject_name
    return render_template('start.html', subjects=subjects_dict)


@app.route('/testing', methods=['POST'])
def testing():
    arr_data = []
    if request.method == 'POST':
        arr_data.append(request.form['fio'])
        arr_data.append(request.form['group'])
        arr_data.append(request.form['course'])
        arr_data.append(request.form['count'])
    return render_template('testing.html')


@app.route('/result', methods=['POST'])
def test_result():
    return render_template('result.html')


@app.route('/manage', methods=['GET', 'POST'])
def manage_server():
    return render_template('server.html')


@app.route('/advanced_result')
def advanced_result():
    return render_template('advanced_results.html')


@app.errorhandler(405)
def page_not_found(e):
    return render_template('404.html'), 405


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
