# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session
# from flask.ext.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model import CeSubjects
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
    for x in range(len(subjects_data)):
        subjects_dict[subjects_data[x].id] = subjects_data[x].subject_name
    return render_template('start.html', subjects=subjects_dict)


def validate_user_info(fio, group, course, count):
    validation_result = {"fio":"valid",
                         "group":"valid",
                         "course":"valid",
                         "count":"valid"}
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
    return validation_result, has_errors


@app.route('/testing', methods=['POST'])
def testing():
    fio = request.form['fio']
    group = request.form['group']
    course = request.form['course']
    count = request.form['count']
    validation_result, has_errors = validate_user_info(fio, group, course, count)

    if has_errors:
        session['has_errors'] = True
        session['val_res'] = validation_result
        return test_begin()
    else:
        session['has_errors'] = False

    session['fio'] = fio
    session['group'] = group
    session['course'] = course
    session['count'] = count
    return render_template('testing.html')


@app.route('/result', methods=['POST'])
def test_result():
    repr(session)
    return render_template('result.html', data=session.get('fio'))


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
