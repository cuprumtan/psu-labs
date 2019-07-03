# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session
# from flask.ext.session import Session
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from Model import CeSubjects, CeQuestions, CeAnswers, CeSessions
import re
import socket
import datetime


SECRET_KEY = 'idi_v_svoi_dvor'

app = Flask(__name__)
app.config.from_object(__name__)

engine = create_engine('sqlite:///circuit-engineering.db', encoding='utf-8')
connection = engine.connect()
Session = sessionmaker(bind=engine)
db_session = Session()


def get_ipv4():
    all_ip = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]
    ip_v4 = []
    for ip in all_ip:
        if len(ip) < 16:
            ip_v4.append(ip)
    return ip_v4


ip_v4 = get_ipv4()


@app.route('/')
def root():
    return redirect(url_for('test_begin'))


@app.route('/info', methods=['GET', 'POST'])
def test_begin():
    if request.method == 'GET':
        session.clear()
    session_number = db_session.query(func.coalesce(func.max(CeSessions.session_number), 0)).all()
    db_session.commit()
    session['number'] = tuple(session_number[0])[0] + 1
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
    limit = request.form['limit']
    subjects = request.form.getlist('subject')

    session['fio'] = fio
    session['group'] = group
    session['course'] = course
    session['limit'] = limit
    session['subjects'] = subjects

    validation_result, has_errors = validate_user_info(fio, group, course, limit, subjects)

    if has_errors:
        session['has_errors'] = True
        session['val_res'] = validation_result
        return test_begin()
    else:
        session['has_errors'] = False
    questions_dict = {}
    questions_data = db_session.query(CeQuestions.id, CeQuestions.question_text).filter(
        CeQuestions.subject_id.in_(subjects)).order_by(func.random()).limit(limit).all()
    db_session.commit()
    id = 0
    for x in range(len(questions_data)):
        questions_dict[id] = questions_data[x]
        id = id+1
    answers_dict = {}
    answers_data = db_session.query(CeAnswers.id, CeAnswers.answer_text, CeAnswers.question_id, CeAnswers.is_right).filter(
        CeAnswers.question_id.in_([tuple(questions_dict[x])[0] for x in range(len(questions_dict))]))\
        .order_by(func.random()).all()
    db_session.commit()
    right_answers_count = db_session.query(CeAnswers.id, CeAnswers.answer_text, CeAnswers.question_id).filter(
        CeAnswers.question_id.in_([tuple(questions_dict[x])[0] for x in range(len(questions_dict))]))\
        .filter(CeAnswers.is_right == True).count()
    db_session.commit()
    id = 0
    for x in range(len(answers_data)):
        answers_dict[id] = answers_data[x]
        id = id + 1
    session['questions_data'] = questions_data
    session['answers_data'] = answers_data
    session['right_answers_count'] = right_answers_count
    return render_template('testing.html', questions=questions_dict, answers=answers_dict)


@app.route('/result', methods=['POST'])
def test_result():
    if request.method == 'POST':
        questions_data = session.get('questions_data')
        answers_data = session.get('answers_data')
        session_date = datetime.datetime.now().strftime("%Y-%m-%d")# дата
        session_number = session.get('number')
        fio = session.get('fio')# фио студента
        group = session.get('group')# группа
        course = session.get('course')# курс
        # right_answers_count = session.get('right_answers_count')
        score = 0
        for q_object in questions_data:
            answered = request.form.getlist(str(q_object[0]))
            right_count = 0
            right_answered = 0
            for a_object in answers_data:
                if q_object[0] == a_object[2]:
                    if a_object[3] == True:
                        right_count = right_count + 1
                    if str(a_object[0]) in answered:
                        checked = True
                        if a_object[3] == True:
                            right_answered = right_answered + 1
                    else:
                        checked = False
                    to_insert = CeSessions(
                        session_number=session_number,
                        session_date=session_date,
                        student_name=fio,
                        student_group=group,
                        student_grade=course,
                        answer_id=a_object[0],
                        is_right=a_object[3]
                    )
                    db_session.add(to_insert)
                    db_session.flush()
                    db_session.commit()
                    # тут сохраняем
            if right_count == right_answered:
                score = score + 1
        questions_count = len(questions_data)
        right_answers_percent = round(float(score)/float(questions_count)*100)
        db_session.query(CeSessions).filter(CeSessions.session_number == session.get('number')).\
            update({CeSessions.result_percent: right_answers_percent}, synchronize_session=False)
        db_session.commit()
        session.clear()
    return render_template('result.html', user_answers=score, rigth_answers=questions_count, percent=right_answers_percent)


@app.route('/manage', methods=['GET', 'POST'])
def manage_server():
    # p = subprocess.Popen("bash get_my_ip.sh", stdout=subprocess.PIPE, shell=True)
    # (output, err) = p.communicate()
    if request.method == 'GET':
        date_from = datetime.datetime.now().strftime("%Y-%m-%d")
        date_to = datetime.datetime.now().strftime("%Y-%m-%d")
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
            date_from = datetime.datetime.now().strftime("%Y-%m-%d")
            date_to = datetime.datetime.now().strftime("%Y-%m-%d")
    sessions_data = db_session.query(CeSessions.session_number,
                                     CeSessions.session_date,
                                     CeSessions.student_name,
                                     CeSessions.student_group,
                                     CeSessions.student_grade,
                                     CeSessions.result_percent) \
        .distinct(CeSessions.session_number) \
        .filter(CeSessions.session_date >= date_from) \
        .filter(CeSessions.session_date <= date_to) \
        .order_by(CeSessions.session_number).all()
    db_session.commit()
    return render_template('server.html', ip_list=ip_v4, sessions=sessions_data)

class UserAnswer():
    id = 0
    question_id = 0
    answer_text = 0
    is_right = 0

@app.route('/advanced_result', methods=['GET'])
def advanced_result():
    session_number = request.args.get('session_number')
    session_data = db_session.query(CeSessions.id,
                                    CeSessions.session_number,
                                    CeSessions.session_date,
                                    CeSessions.student_name,
                                    CeSessions.student_group,
                                    CeSessions.student_grade,
                                    CeSessions.answer_id,
                                    CeSessions.is_right)\
        .filter(CeSessions.session_number == session_number).all()
    db_session.commit()
    fio = session_data[0].student_name
    group = session_data[0].student_group
    course = session_data[0].student_grade
    date = session_data[0].session_date
    answers_data = db_session.query(CeAnswers.id,
                                    CeAnswers.answer_text,
                                    CeAnswers.question_id,
                                    CeAnswers.is_right)\
        .filter(CeAnswers.id.in_([data.answer_id for data in session_data])).all()
    db_session.commit()
    questions_data = db_session.query(CeQuestions.id,
                                      CeQuestions.question_text) \
        .filter(CeQuestions.id.in_([answer.question_id for answer in answers_data])).all()
    db_session.commit()
    id = 0
    questions_dict = {}
    user_answers = []
    for answer in answers_data:
        for sess_answer in session_data:
            if answer.id == sess_answer.answer_id:
                answer = UserAnswer()
    # for session in session_data:
    #     CeAnswers
    #     questions_dict[id] =
    # questions_dict =
    return render_template('advanced_results.html', fio=fio, group=group, course=course, date=date, data=questions_dict)


@app.errorhandler(405)
def page_not_found(e):
    return render_template('404.html'), 405


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
