# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session
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

# подключение к базе данных
engine = create_engine('sqlite:///circuit-engineering.db', encoding='utf-8')
connection = engine.connect()
Session = sessionmaker(bind=engine)
db_session = Session()


# функция сбора IP-адреса сервера
def get_ipv4():
    all_ip = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]
    ip_v4 = []
    for ip in all_ip:
        if len(ip) < 16 and ip not in ip_v4:
            ip_v4.append(ip)
    return ip_v4


ip_v4 = get_ipv4()


def validatable_ip_v4():
    validatable_ip_v4 = []
    validatable_ip_v4.append('127.0.0.1')
    validatable_ip_v4.append('localhost')
    return validatable_ip_v4


# обработка главной страницы, редирект на начальную страницу тестирования
@app.route('/')
def root():
    return redirect(url_for('test_begin'))


# обработка начальной страницы
@app.route('/info', methods=['GET', 'POST'])
def test_begin():
    if request.method == 'GET':
        session.clear()
    # определение порядкового номера сессии (сессия в данном случае = уникальный запуск или подключение)
    session_number = db_session.query(func.coalesce(func.max(CeSessions.session_number), 0)).all()
    db_session.commit()
    session['number'] = tuple(session_number[0])[0] + 1
    # получение списка всех существующих в бд тем
    subjects_dict = {}
    subjects_data = db_session.query(CeSubjects.id, CeSubjects.subject_name).all()
    db_session.commit()
    id = 0
    for x in range(len(subjects_data)):
        subjects_dict[id] = subjects_data[x]
        id = id+1
    return render_template('start.html', subjects=subjects_dict)


# обработка введенных пользователем данных в форму начальной страницы
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


# обработка страницы с тестом
@app.route('/testing', methods=['POST'])
def testing():
    # сбор персональных данных пользователя с формы начальной страницы
    fio = request.form['fio']
    group = request.form['group']
    course = request.form['course']
    limit = request.form['limit']
    subjects = request.form.getlist('subject')
    # передача персональных данных в параметры сессии
    session['fio'] = fio
    session['group'] = group
    session['course'] = course
    session['limit'] = limit
    session['subjects'] = subjects
    # проверка
    validation_result, has_errors = validate_user_info(fio, group, course, limit, subjects)
    if has_errors:
        session['has_errors'] = True
        session['val_res'] = validation_result
        return test_begin()
    else:
        session['has_errors'] = False
    # сбор случайных вопросов в нужном количестве по выбранным темам
    questions_dict = {}
    questions_data = db_session.query(CeQuestions.id, CeQuestions.question_text).filter(
        CeQuestions.subject_id.in_(subjects)).order_by(func.random()).limit(limit).all()
    db_session.commit()
    id = 0
    for x in range(len(questions_data)):
        questions_dict[id] = questions_data[x]
        id = id+1
    # сбор ответов на полученные выше вопросы
    answers_dict = {}
    answers_data = db_session.query(CeAnswers.id, CeAnswers.answer_text, CeAnswers.question_id, CeAnswers.is_right).filter(
        CeAnswers.question_id.in_([tuple(questions_dict[x])[0] for x in range(len(questions_dict))]))\
        .order_by(func.random()).all()
    db_session.commit()
    # подсчет количества всех верных ответов
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


# обработка страницы с результатом
@app.route('/result', methods=['POST'])
def test_result():
    if request.method == 'POST':
        # получение пользовательских данных из сессии
        questions_data = session.get('questions_data')
        answers_data = session.get('answers_data')
        session_date = datetime.datetime.now().strftime("%Y-%m-%d")# дата
        session_number = session.get('number')
        fio = session.get('fio')# фио студента
        group = session.get('group')# группа
        course = session.get('course')# курс
        # подсчет ответов пользователя
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
                    # заполнение логов БД
                    to_insert = CeSessions(
                        session_number=session_number,
                        session_date=session_date,
                        student_name=fio,
                        student_group=group,
                        student_grade=course,
                        answer_id=a_object[0],
                        is_right=checked
                    )
                    db_session.add(to_insert)
                    db_session.flush()
                    db_session.commit()
            if right_count == right_answered:
                score = score + 1
        # подсчет итогового результата
        questions_count = len(questions_data)
        right_answers_percent = round(float(score)/float(questions_count)*100)
        # вставка результата пользователя в логи БД
        db_session.query(CeSessions).filter(CeSessions.session_number == session.get('number')).\
            update({CeSessions.result_percent: right_answers_percent}, synchronize_session=False)
        db_session.commit()
        session.clear()
    return render_template('result.html', user_answers=score, rigth_answers=questions_count, percent=right_answers_percent)


# обработка страницы с панелью управления
@app.route('/manage', methods=['GET', 'POST'])
def manage_server():
    # валидация
    if request.remote_addr not in validatable_ip_v4():
        return redirect('page_not_found')
    if request.method == 'GET':
        # заполнение параметров для фильтра дефолтными значениями
        date_from = datetime.datetime.now().strftime("%Y-%m-%d")
        date_to = datetime.datetime.now().strftime("%Y-%m-%d")
        course = None
        course = None
        group = None
    if request.method == 'POST':
        # получение параметров для фильтра
        date_from = request.form['date_from']
        date_to = request.form['date_to']
        course = request.form['course']
        group = request.form['group']
        # применение фильтра
        if request.form['btn_action'] != 'clear':
            session['date_from'] = date_from
            session['date_to'] = date_to
            session['course'] = course
            session['group'] = group
        else:
            # очистка фильтра
            session.clear()
            date_from = datetime.datetime.now().strftime("%Y-%m-%d")
            date_to = datetime.datetime.now().strftime("%Y-%m-%d")
    # поиск номеров уникальных сессий
    query = db_session.query(CeSessions.session_number,
                             CeSessions.session_date,
                             CeSessions.student_name,
                             CeSessions.student_group,
                             CeSessions.student_grade,
                             CeSessions.result_percent) \
        .distinct(CeSessions.session_number)
    db_session.commit()
    # применение фильтра
    conditions = []
    if date_from != None and date_from !='':
        conditions.append(CeSessions.session_date >= date_from)
    if date_to != None and date_to !='':
        conditions.append(CeSessions.session_date <= date_to)
    if course != None and course !='':
        conditions.append(CeSessions.student_grade == course)
    if group != None and group !='':
        conditions.append(CeSessions.student_group == group)
    query = query.filter(*conditions)
    sessions_data = query.order_by(CeSessions.session_number).all()
    db_session.commit()
    return render_template('server.html', ip_list=ip_v4, sessions=sessions_data)


# объявление классов для вопроса и овтета
#################################
class Question():
    def __init__(self):
        self.id = 0
        self.question_text = ""
        self.answers = []


#################################
class UserAnswer():
    def __init__(self):
        self.id = 0
        self.question_id = 0
        self.answer_text = ""
        self.checked = False
        self.is_right = False


# обработка страницы с просмотром полного результата
@app.route('/advanced_result', methods=['GET'])
def advanced_result():
    # валидация
    if request.remote_addr not in validatable_ip_v4():
        return redirect('page_not_found')
    # получение номера сессии, к которой относится просматриваемый тест
    session_number = request.args.get('session_number')
    # получение данных по тесту
    session_data = db_session.query(CeSessions.id,
                                    CeSessions.session_number,
                                    CeSessions.session_date,
                                    CeSessions.student_name,
                                    CeSessions.student_group,
                                    CeSessions.student_grade,
                                    CeSessions.answer_id,
                                    CeSessions.is_right,
                                    CeSessions.result_percent)\
        .filter(CeSessions.session_number == session_number).all()
    db_session.commit()
    # заполнение персональных данных для шапки
    fio = session_data[0].student_name
    group = session_data[0].student_group
    course = session_data[0].student_grade
    date = session_data[0].session_date
    percent = session_data[0].result_percent
    # получение инфорамции о правильных ответах
    answers_data = db_session.query(CeAnswers.id,
                                    CeAnswers.answer_text,
                                    CeAnswers.question_id,
                                    CeAnswers.is_right)\
        .filter(CeAnswers.id.in_([data.answer_id for data in session_data])).all()
    db_session.commit()
    # получение всех вопросов теста
    questions_data = db_session.query(CeQuestions.id,
                                      CeQuestions.question_text) \
        .filter(CeQuestions.id.in_([answer.question_id for answer in answers_data])).all()
    db_session.commit()
    # сравнение ответов
    user_answers = []
    for answer in answers_data:
        for sess_answer in session_data:
            if answer.id == sess_answer.answer_id:
                user_answer = UserAnswer()
                user_answer.id = answer.id
                user_answer.question_id = answer.question_id
                user_answer.answer_text = answer.answer_text
                user_answer.checked = sess_answer.is_right
                if sess_answer.is_right == answer.is_right:
                    user_answer.is_right = True
                else:
                    user_answer.is_right = False
                user_answers.append(user_answer)
    questions_array = []
    for question_data in questions_data:
        answers = []
        question = Question()
        question.id = question_data.id
        question.question_text = question_data.question_text
        for user_answer in user_answers:
            if user_answer.question_id == question_data.id:
                answers.append(user_answer)
        question.answers = answers
        questions_array.append(question)
    return render_template('advanced_results.html', fio=fio, group=group, course=course, date=date, percent=percent, data=questions_array)


# обработка страницы с удалением темы
@app.route('/delete_subject', methods=['GET', 'POST'])
def delete_subject():
    # валидация
    if request.remote_addr not in validatable_ip_v4():
        return redirect('page_not_found')
    # получение всех тем
    subjects_data = db_session.query(CeSubjects.id, CeSubjects.subject_name).all()
    db_session.commit()
    subjects_dict = {}
    for x in range(len(subjects_data)):
        subjects_dict[subjects_data[x].id] = subjects_data[x].subject_name
    if request.method == 'POST':
        if request.form['btn_action'] == 'delete':
            # получение номера темы, которую нужно удалить
            subject_id = str(request.form['subject_id'])
            # удаление темы, вопросов и ответов на них
            questions_data = db_session.query(CeQuestions.id).filter(CeQuestions.subject_id == subject_id).all()
            db_session.commit()
            db_session.query(CeSubjects).filter(CeSubjects.id == subject_id).delete()
            db_session.commit()
            db_session.query(CeQuestions).filter(CeQuestions.subject_id == subject_id).delete()
            db_session.commit()
            for x in range(len(questions_data)):
                db_session.query(CeAnswers).filter(
                    CeAnswers.question_id == questions_data[x].id).delete()
                db_session.commit()
    return render_template('delete_subject.html', subjects=subjects_dict)


# обработка страниы с добавлением темы
@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    # валидация
    if request.remote_addr not in validatable_ip_v4():
        return redirect('page_not_found')
    # получение всех тем
    subjects_data = db_session.query(CeSubjects.id, CeSubjects.subject_name).all()
    db_session.commit()
    subjects_dict = {}
    for x in range(len(subjects_data)):
        subjects_dict[subjects_data[x].id] = subjects_data[x].subject_name
    if request.method == 'POST':
        if request.form['btn_action'] == 'add':
            # добавление темы в Бд
            subject_name = request.form['subject']
            to_insert = CeSubjects(
                subject_name=subject_name
            )
            db_session.add(to_insert)
    return render_template('add_subject.html', subjects=subjects_dict)


# обработка страницы с удалением вопроса
@app.route('/delete_question', methods=['GET', 'POST'])
def delete_question():
    # валидация
    if request.remote_addr not in validatable_ip_v4():
        return redirect('page_not_found')
    # получение всех вопросов
    questions_data = db_session.query(CeQuestions.id, CeQuestions.question_text).all()
    db_session.commit()
    questions_dict = {}
    for x in range(len(questions_data)):
        questions_dict[questions_data[x].id] = questions_data[x].question_text
    if request.method == 'POST':
        if request.form['btn_action'] == 'delete':
            # получение номера вопроса, который нужно удалить
            question_id = str(request.form['question_id'])
            # удаление вопроса и ответов на него
            db_session.query(CeQuestions).filter(CeQuestions.id == question_id).delete()
            db_session.commit()
            db_session.query(CeAnswers).filter(CeAnswers.question_id == question_id).delete()
            db_session.commit()
    return render_template('delete_question.html', questions=questions_dict)


# обработка страницы с добавлением вопроса
@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    # валидация
    if request.remote_addr not in validatable_ip_v4():
        return redirect('page_not_found')
    # получение всех тем
    subjects_data = db_session.query(CeSubjects.id, CeSubjects.subject_name).all()
    db_session.commit()
    subjects_dict = {}
    for x in range(len(subjects_data)):
        subjects_dict[subjects_data[x].id] = subjects_data[x].subject_name
    if request.method == 'POST':
        if request.form['btn_action'] == 'add':
            # сбор информации о вопросе с формы
            question_subject = request.form.getlist('subject')
            question_text = request.form['text']
            answer_1 = request.form['ans1']
            answer_2 = request.form['ans2']
            answer_3 = request.form['ans3']
            answer_4 = request.form['ans4']
            right_answers = request.form.getlist('right-flag')
            # добваление вопроса в БД
            to_insert = CeQuestions(
                subject_id=question_subject[0],
                question_text=question_text
            )
            db_session.add(to_insert)
            db_session.commit()
            # получение ID добавленного вопроса
            question_id = db_session.query(func.max(CeQuestions.id)).all()
            db_session.commit()
            # добавление ответов на вопрос в БД
            to_insert = CeAnswers(
                question_id=tuple(question_id[0])[0],
                answer_text=answer_1,
                is_right=(1 in right_answers)
            )
            db_session.add(to_insert)
            db_session.commit()
            to_insert = CeAnswers(
                question_id=tuple(question_id[0])[0],
                answer_text=answer_2,
                is_right=(2 in right_answers)
            )
            db_session.add(to_insert)
            db_session.commit()
            to_insert = CeAnswers(
                question_id=tuple(question_id[0])[0],
                answer_text=answer_3,
                is_right=(3 in right_answers)
            )
            db_session.add(to_insert)
            db_session.commit()
            to_insert = CeAnswers(
                question_id=tuple(question_id[0])[0],
                answer_text=answer_4,
                is_right=(4 in right_answers)
            )
            db_session.add(to_insert)
            db_session.commit()
    return render_template('add_question.html', subjects=subjects_dict)


# обработа ошибки 405 (== ошибка методов [post, get], поэтому приравниваем к 404)
@app.errorhandler(405)
def page_not_found(e):
    return render_template('404.html'), 405


# обработа ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# старт приложения
if __name__ == '__main__':
    app.run()
