# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session
# from flask.ext.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from Model import CeSubjects, CeQuestions, CeAnswers
import re

SECRET_KEY = 'idi_v_svoi_dvor'

app = Flask(__name__)
app.config.from_object(__name__)

engine = create_engine('sqlite:///circuit-engineering.db', encoding='utf-8')
connection = engine.connect()
Session = sessionmaker(bind=engine)
db_session = Session()


@app.route('/')
def root():
    return redirect(url_for('test_begin'))


@app.route('/info', methods=['GET', 'POST'])
def test_begin():
    if request.method == 'GET':
        session.clear()
    subjects_dict = {}
    subjects_data = db_session.query(CeSubjects.id, CeSubjects.subject_name).all()
    db_session.commit()
    id = 0
    for x in range(len(subjects_data)):
        subjects_dict[id] = subjects_data[x]
        id = id+1
    return render_template('start.html', subjects=subjects_dict)


def validate_user_info(fio, group, course, count, subjects):
    validation_result = {"fio": "valid",
                         "group": "valid",
                         "course": "valid",
                         "count": "valid",
                         "subjects": "valid"}
    has_errors = False
    if not re.match(re.compile(unicode(r'^[А-Яа-я ]+$', 'utf8')), fio):
        validation_result["fio"] = "invalid"
        has_errors = True
    if not re.match(re.compile(unicode('^[А-Яа-я0-9_-]+$', 'utf8')), group):
        validation_result["group"] = "invalid"
        has_errors = True
    if not re.match(r'^[1-6]$', course):
        validation_result["course"] = "invalid"
        has_errors = True
    if not re.match(r'^[1-9]+[0-9]*$', count):
        validation_result["count"] = "invalid"
        has_errors = True
    if len(subjects) == 0:
        validation_result["subjects"] = "invalid"
        has_errors = True
    return validation_result, has_errors


@app.route('/testing', methods=['POST'])
def testing():
    fio = request.form['fio']
    group = request.form['group']
    course = request.form['course']
    count = request.form['count']
    subjects = request.form.getlist('subject')

    session['fio'] = fio
    session['group'] = group
    session['course'] = course
    session['count'] = count
    session['subjects'] = subjects

    validation_result, has_errors = validate_user_info(fio, group, course, count, subjects)

    if has_errors:
        session['has_errors'] = True
        session['val_res'] = validation_result
        return test_begin()
    else:
        session['has_errors'] = False
    questions_dict = {}
    questions_data = db_session.query(CeQuestions.id, CeQuestions.question_text).filter(
        CeQuestions.subject_id.in_(subjects)).order_by(func.random()).limit(count).all()
    db_session.commit()
    id = 0
    for x in range(len(questions_data)):
        questions_dict[id] = questions_data[x]
        id = id+1
    answers_dict = {}
    answers_data = db_session.query(CeAnswers.id, CeAnswers.answer_text, CeAnswers.question_id).filter(
        CeAnswers.question_id.in_([tuple(questions_dict[x])[0] for x in range(len(questions_dict))]))\
        .order_by(func.random()).all()
    db_session.commit()
    id = 0
    for x in range(len(answers_data)):
        answers_dict[id] = answers_data[x]
        id = id + 1
    return render_template('testing.html', questions=questions_dict, answers=answers_dict)


@app.route('/result', methods=['POST'])
def test_result():
    session.clear()
    return render_template('result.html', data=session.get('fio'))


@app.route('/manage', methods=['GET', 'POST'])
def manage_server():
    if request.method == 'POST':
        date_from = request.form['date_from']
        date_to = request.form['date_to']
        course = request.form['course']
        group = request.form['group']

        if request.form['btn_action'] != 'clear':
            session['date_from'] = date_from
            session['date_to'] = date_to
            session['course'] = course
            session['group'] = group
        else:
            session.clear()
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
