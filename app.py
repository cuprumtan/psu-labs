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
    # test_data = session.query(CeSubjects.subject_name).all()
    # session.commit()
    # test_arr = []
    # for x in range(len(test_data)):
    #     test_arr.append(test_data[x].subject_name)
    # return test_arr[5]
    # return repr(test_arr).decode("unicode-escape")
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
