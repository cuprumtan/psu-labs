-- темы
create table cesubjects
(
	id integer primary key autoincrement not null,
	subject_name varchar(255) not null
);

-- вопросы
create table cequestions
(
	id integer primary key autoincrement not null,
	subject_id integer not null,
	question_text text not null,
	foreign key (subject_id) references cesubjects(id)
);

-- ответы
create table ceanswers
(
	id integer primary key autoincrement not null,
	question_id integer not null,
	answer_text text not null,
	is_right boolean not null,
	foreign key (question_id) references cequestions(id)
);

-- сессии
create table cesessions
(
	id integer primary key autoincrement not null,
	session_number integer not null,
	session_date text not null,
	student_name varchar(255) not null,
	student_group varchar(10),
	student_grade integer,
	answer_id integer not null,
	is_right boolean not null,
	foreign key (answer_id) references ceanswers(id)
);

