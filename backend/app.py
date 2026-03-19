import os
from flask import Flask, jsonify, request, render_template, redirect, url_for, session, Response
from datetime import datetime
import oracledb
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import io
from io import TextIOWrapper, StringIO
import sys
import csv



# --- Инициализация Oracle client (thick mode) ---
oracledb.init_oracle_client(lib_dir="/opt/oracle/instantclient")

app = Flask(__name__)
app.secret_key = 'asutp-super-secret-key-2026-bmstu'  # Сложный ключ

# --- Параметры подключения к БД из переменных окружения ---
DB_USER = os.environ.get("ORACLE_USER", "system")
DB_PASSWORD = os.environ.get("ORACLE_PASSWORD", "oracle")
DB_DSN = os.environ.get("ORACLE_DSN", "oracle-db:1521/XE")

# Декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('seminar1_task3_login'))
        return f(*args, **kwargs)
    return decorated_function

# Функция подключения к БД
def get_db_connection():
    """Получение соединения с БД и переключение на схему ASUTP"""
    conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
    
    # Пытаемся переключиться на схему ASUTP
    try:
        cur = conn.cursor()
        cur.execute("ALTER SESSION SET CURRENT_SCHEMA = ASUTP")
        cur.close()
    except:
        # Если не получается, работаем в текущей схеме
        pass
    
    return conn

def check_system_user(username, password):
    """Проверка пользователя SYSTEM через Oracle"""
    try:
        # Пробуем подключиться к Oracle с переданными учетными данными
        test_conn = oracledb.connect(
            user=username,
            password=password,
            dsn=DB_DSN
        )
        test_conn.close()
        return True
    except:
        return False
    
@app.route("/seminar1/task3_login", methods=["GET", "POST"])
def seminar1_task3_login():
    error = None
    
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Проверяем через Oracle
        if check_system_user(username, password):
            session['logged_in'] = True
            session['username'] = username
            # Хешируем пароль для дополнительной безопасности (но не храним)
            session['password_hash'] = generate_password_hash(password)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('seminar1_task3_advanced'))
        else:
            error = 'Неверный логин или пароль Oracle'
    
    return render_template("seminar1/task3_login.html", error=error)

@app.route("/seminar1/task3_add_15_records")
@login_required
def seminar1_task3_add_15_records():
    """Добавляет по 15 записей в каждую таблицу"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("ALTER SESSION SET CURRENT_SCHEMA = ASUTP")
        
        results = []
        
        # 15 КЛИЕНТОВ
        clients_data = [
            ('ООО "ТехноСервис"', 'Алексей Петров', '+7(495)111-11-11', 'info@technoservice.ru', 2),
            ('АО "ИТ-Интегратор"', 'Мария Иванова', '+7(495)222-22-22', 'contact@itintegrator.ru', 1),
            ('ООО "СофтМастер"', 'Дмитрий Соколов', '+7(495)333-33-33', 'softmaster@mail.ru', 3),
            ('ЗАО "ТестЛаб"', 'Елена Новикова', '+7(495)444-44-44', 'testlab@yandex.ru', 1),
            ('ООО "ВебСтудия Плюс"', 'Павел Морозов', '+7(495)555-55-55', 'webstudio@mail.ru', 2),
            ('АО "Системы Безопасности"', 'Игорь Волков', '+7(495)666-66-66', 'security@safety.ru', 1),
            ('ООО "ФинансТех"', 'Ольга Смирнова', '+7(495)777-77-77', 'fintech@bank.ru', 1),
            ('ЗАО "МедТех"', 'Андрей Козлов', '+7(495)888-88-88', 'medtech@health.ru', 3),
            ('ООО "ЛогистикПРО"', 'Татьяна Орлова', '+7(495)999-99-99', 'logistic@pro.ru', 2),
            ('АО "ЭнергоСофт"', 'Николай Васильев', '+7(495)000-00-00', 'energo@soft.ru', 2),
            ('ООО "КиберЗащита"', 'Сергей Павлов', '+7(495)123-12-12', 'cyber@security.ru', 1),
            ('ЗАО "РоботТех"', 'Анна Михайлова', '+7(495)234-23-23', 'robot@tech.ru', 1),
            ('ООО "Искусственный Интеллект"', 'Максим Федоров', '+7(495)345-34-34', 'ai@intellect.ru', 1),
            ('АО "Блокчейн Солюшнс"', 'Екатерина Степанова', '+7(495)456-45-45', 'blockchain@solution.ru', 2),
            ('ООО "Облачные Технологии"', 'Денис Григорьев', '+7(495)567-56-56', 'cloud@tech.ru', 2),
        ]
        
        for name, contact, phone, email, priority in clients_data:
            cur.execute("""
                INSERT INTO ASU_CLIENTS (client_id, client_name, contact_person, phone, email, priority)
                VALUES (SEQ_CLIENT_ID.NEXTVAL, :1, :2, :3, :4, :5)
            """, [name, contact, phone, email, priority])
        results.append(f"✅ Добавлено 15 клиентов")
        
        # 15 СОТРУДНИКОВ
        employees_data = [
            ('Артем', 'Сидоров', 'Тестировщик', 'TESTING', 'a.sidorov@testlab.ru', '+7(903)111-11-11', 2),
            ('Виктория', 'Кузнецова', 'Тестировщик', 'TESTING', 'v.kuznecova@testlab.ru', '+7(903)222-22-22', 2),
            ('Глеб', 'Никитин', 'Тестировщик', 'TESTING', 'g.nikitin@testlab.ru', '+7(903)333-33-33', 2),
            ('Дарья', 'Морозова', 'Аналитик', 'ANALYSIS', 'd.morozova@testlab.ru', '+7(903)444-44-44', 4),
            ('Евгений', 'Воробьев', 'Аналитик', 'ANALYSIS', 'e.vorobiev@testlab.ru', '+7(903)555-55-55', 4),
            ('Жанна', 'Павлова', 'Аналитик', 'ANALYSIS', 'j.pavlova@testlab.ru', '+7(903)666-66-66', 4),
            ('Захар', 'Громов', 'Руководитель', 'MANAGEMENT', 'z.gromov@testlab.ru', '+7(903)777-77-77', 1),
            ('Ирина', 'Соловьева', 'Руководитель', 'MANAGEMENT', 'i.solovieva@testlab.ru', '+7(903)888-88-88', 1),
            ('Кирилл', 'Белов', 'Тестировщик', 'TESTING', 'k.belov@testlab.ru', '+7(903)999-99-99', 2),
            ('Лариса', 'Комарова', 'Тестировщик', 'TESTING', 'l.komarova@testlab.ru', '+7(903)000-00-00', 2),
            ('Михаил', 'Жуков', 'Тестировщик', 'TESTING', 'm.zhukov@testlab.ru', '+7(903)121-21-21', 2),
            ('Надежда', 'Сорокина', 'Аналитик', 'ANALYSIS', 'n.sorokina@testlab.ru', '+7(903)232-32-32', 4),
            ('Олег', 'Крылов', 'Аналитик', 'ANALYSIS', 'o.krylov@testlab.ru', '+7(903)343-43-43', 4),
            ('Полина', 'Фролова', 'Руководитель', 'MANAGEMENT', 'p.frolova@testlab.ru', '+7(903)454-54-54', 1),
            ('Роман', 'Щербаков', 'Руководитель', 'MANAGEMENT', 'r.scherbakov@testlab.ru', '+7(903)565-65-65', 1),
        ]
        
        for first, last, pos, dept, email, phone, manager in employees_data:
            cur.execute("""
                INSERT INTO ASU_EMPLOYEES (employee_id, first_name, last_name, position, department, email, phone, manager_id)
                VALUES (SEQ_EMPLOYEE_ID.NEXTVAL, :1, :2, :3, :4, :5, :6, :7)
            """, [first, last, pos, dept, email, phone, manager])
        results.append(f"✅ Добавлено 15 сотрудников")
        
        # 15 ПРОЕКТОВ
        projects_data = [
            ('Разработка ERP системы', 1, 'Внедрение ERP', '2024-06-01', 1, 3),
            ('Мобильное приложение для доставки', 3, 'Приложение доставки еды', '2024-06-15', 2, 7),
            ('Обновление CRM', 2, 'Миграция на новую версию', '2024-07-01', 2, 3),
            ('Сайт для интернет-магазина', 4, 'Разработка нового сайта', '2024-07-15', 3, 8),
            ('Система документооборота', 5, 'Электронный документооборот', '2024-08-01', 1, 7),
            ('Чат-бот для поддержки', 6, 'ИИ помощник', '2024-08-15', 1, 14),
            ('BI аналитика', 7, 'Система отчетности', '2024-09-01', 2, 14),
            ('Интеграция с 1С', 8, 'Обмен данными', '2024-09-15', 2, 3),
            ('Личный кабинет клиента', 9, 'ЛК для клиентов', '2024-10-01', 3, 8),
            ('API шлюз', 10, 'Микросервисная архитектура', '2024-10-15', 1, 7),
            ('Система мониторинга', 11, 'Мониторинг серверов', '2024-11-01', 2, 14),
            ('Портал для партнеров', 12, 'B2B портал', '2024-11-15', 2, 8),
            ('Мобильное приложение банка', 13, 'Интернет-банкинг', '2024-12-01', 1, 3),
            ('Система лояльности', 14, 'Программа лояльности', '2024-12-15', 3, 7),
            ('HR портал', 15, 'Портал для сотрудников', '2025-01-01', 2, 14),
        ]
        
        for name, client, desc, date, priority, manager in projects_data:
            cur.execute("""
                INSERT INTO ASU_PROJECTS (project_id, project_name, client_id, description, start_date, priority, project_manager_id)
                VALUES (SEQ_PROJECT_ID.NEXTVAL, :1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6)
            """, [name, client, desc, date, priority, manager])
        results.append(f"✅ Добавлено 15 проектов")
        
        # 15 ТЕСТ-КЕЙСОВ
        for i in range(1, 16):
            cur.execute("""
                INSERT INTO ASU_TEST_CASES (testcase_id, testcase_name, project_id, steps, expected_result, priority, author_id, status)
                VALUES (SEQ_TESTCASE_ID.NEXTVAL, :1, :2, :3, :4, :5, :6, 'ACTIVE')
            """, [
                f'Тест-кейс #{i} для проекта {i%5+1}',
                i%5+1,
                f'1. Действие 1\n2. Действие 2\n3. Действие 3',
                'Ожидаемый результат',
                i%3+1,
                i%10+3
            ])
        results.append(f"✅ Добавлено 15 тест-кейсов")
        
        # 15 ДЕФЕКТОВ
        for i in range(1, 16):
            cur.execute("""
                INSERT INTO ASU_DEFECTS (defect_id, defect_title, project_id, description, steps_to_reproduce, severity, priority, assigned_to, reported_by)
                VALUES (SEQ_DEFECT_ID.NEXTVAL, :1, :2, :3, :4, :5, :6, :7, :8)
            """, [
                f'Дефект #{i} в проекте {i%5+1}',
                i%5+1,
                f'Описание дефекта {i}',
                f'1. Шаг 1\n2. Шаг 2\n3. Шаг 3',
                ['MINOR', 'MAJOR', 'CRITICAL', 'BLOCKER'][i%4],
                i%3+1,
                i%10+3,
                2
            ])
        results.append(f"✅ Добавлено 15 дефектов")
        
        conn.commit()
        cur.close()
        conn.close()
        
        return render_template("seminar1/task3_success.html", results=results)
        
    except Exception as e:
        return f"Ошибка: {str(e)}"

@app.route("/seminar1/task3_setup", methods=["GET", "POST"])
@login_required
def seminar1_task3_setup():
    """Страница для настройки базы данных АСУ"""
    result = None
    error = None
    
    if request.method == "POST":
        action = request.form.get("action")
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            result = []
            
            if action == "create_user":
                # Создаем пользователя ASUTP
                try:
                    cur.execute("""
                        BEGIN
                            EXECUTE IMMEDIATE 'CREATE USER ASUTP IDENTIFIED BY asutp123 DEFAULT TABLESPACE USERS QUOTA UNLIMITED ON USERS';
                            EXECUTE IMMEDIATE 'GRANT CONNECT, RESOURCE TO ASUTP';
                            EXECUTE IMMEDIATE 'GRANT CREATE SESSION TO ASUTP';
                            EXECUTE IMMEDIATE 'GRANT CREATE TABLE TO ASUTP';
                            EXECUTE IMMEDIATE 'GRANT CREATE VIEW TO ASUTP';
                            EXECUTE IMMEDIATE 'GRANT CREATE SEQUENCE TO ASUTP';
                            EXECUTE IMMEDIATE 'GRANT CREATE PROCEDURE TO ASUTP';
                            EXECUTE IMMEDIATE 'GRANT CREATE TRIGGER TO ASUTP';
                            EXECUTE IMMEDIATE 'GRANT SELECT ON HR.EMPLOYEES TO ASUTP';
                            EXECUTE IMMEDIATE 'GRANT SELECT ON HR.DEPARTMENTS TO ASUTP';
                            EXECUTE IMMEDIATE 'GRANT SELECT ON HR.JOBS TO ASUTP';
                        END;
                    """)
                    conn.commit()
                    result.append("✅ Пользователь ASUTP успешно создан")
                except Exception as e:
                    if "ORA-01920" in str(e):
                        result.append("ℹ️ Пользователь ASUTP уже существует")
                    else:
                        raise e
                        
            elif action == "create_tables":
                # Переключаемся на пользователя ASUTP
                cur.execute("ALTER SESSION SET CURRENT_SCHEMA = ASUTP")
                
                cur.execute("SELECT SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') FROM dual")
                current_schema = cur.fetchone()[0]
                result.append(f"📋 Текущая схема: {current_schema}")
                
                # Создаем таблицы
                tables_sql = [
                    """
                    CREATE TABLE ASU_CLIENTS (
                        client_id NUMBER PRIMARY KEY,
                        client_name VARCHAR2(200) NOT NULL,
                        contact_person VARCHAR2(100),
                        phone VARCHAR2(20),
                        email VARCHAR2(100),
                        status VARCHAR2(20) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE')),
                        priority NUMBER(1) DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
                        responsible_emp_id NUMBER,
                        created_date DATE DEFAULT SYSDATE,
                        modified_date DATE
                    )
                    """,
                    """
                    CREATE TABLE ASU_EMPLOYEES (
                        employee_id NUMBER PRIMARY KEY,
                        first_name VARCHAR2(50) NOT NULL,
                        last_name VARCHAR2(50) NOT NULL,
                        position VARCHAR2(100),
                        department VARCHAR2(50) CHECK (department IN ('TESTING', 'ANALYSIS', 'MANAGEMENT')),
                        email VARCHAR2(100) UNIQUE,
                        phone VARCHAR2(20),
                        status VARCHAR2(20) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE')),
                        manager_id NUMBER,
                        hire_date DATE DEFAULT SYSDATE
                    )
                    """,
                    """
                    CREATE TABLE ASU_PROJECTS (
                        project_id NUMBER PRIMARY KEY,
                        project_name VARCHAR2(200) NOT NULL,
                        client_id NUMBER REFERENCES ASU_CLIENTS(client_id),
                        description CLOB,
                        start_date DATE,
                        end_date DATE,
                        status VARCHAR2(20) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'ON_HOLD', 'COMPLETED', 'CANCELLED')),
                        priority NUMBER(1) DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
                        project_manager_id NUMBER REFERENCES ASU_EMPLOYEES(employee_id),
                        created_date DATE DEFAULT SYSDATE
                    )
                    """,
                    """
                    CREATE TABLE ASU_TEST_PLANS (
                        plan_id NUMBER PRIMARY KEY,
                        project_id NUMBER REFERENCES ASU_PROJECTS(project_id),
                        plan_name VARCHAR2(200) NOT NULL,
                        version VARCHAR2(20),
                        release_date DATE,
                        status VARCHAR2(20) DEFAULT 'PLANNED' CHECK (status IN ('PLANNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
                        description CLOB,
                        created_by NUMBER REFERENCES ASU_EMPLOYEES(employee_id),
                        created_date DATE DEFAULT SYSDATE
                    )
                    """,
                    """
                    CREATE TABLE ASU_TEST_CASES (
                        testcase_id NUMBER PRIMARY KEY,
                        testcase_name VARCHAR2(500) NOT NULL,
                        project_id NUMBER REFERENCES ASU_PROJECTS(project_id),
                        plan_id NUMBER REFERENCES ASU_TEST_PLANS(plan_id),
                        description CLOB,
                        steps CLOB,
                        expected_result CLOB,
                        priority NUMBER(1) DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
                        status VARCHAR2(20) DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'ACTIVE', 'DEPRECATED')),
                        author_id NUMBER REFERENCES ASU_EMPLOYEES(employee_id),
                        created_date DATE DEFAULT SYSDATE,
                        modified_date DATE
                    )
                    """,
                    """
                    CREATE TABLE ASU_DEFECTS (
                        defect_id NUMBER PRIMARY KEY,
                        defect_title VARCHAR2(500) NOT NULL,
                        project_id NUMBER REFERENCES ASU_PROJECTS(project_id),
                        testcase_id NUMBER REFERENCES ASU_TEST_CASES(testcase_id),
                        description CLOB,
                        steps_to_reproduce CLOB,
                        severity VARCHAR2(20) CHECK (severity IN ('BLOCKER', 'CRITICAL', 'MAJOR', 'MINOR', 'TRIVIAL')),
                        priority NUMBER(1) DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
                        status VARCHAR2(20) DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'IN_PROGRESS', 'FIXED', 'VERIFIED', 'CLOSED', 'REOPENED')),
                        assigned_to NUMBER REFERENCES ASU_EMPLOYEES(employee_id),
                        reported_by NUMBER REFERENCES ASU_EMPLOYEES(employee_id),
                        created_date DATE DEFAULT SYSDATE,
                        resolved_date DATE,
                        closed_date DATE
                    )
                    """,
                    """
                    CREATE TABLE ASU_REPORTS (
                        report_id NUMBER PRIMARY KEY,
                        report_name VARCHAR2(200) NOT NULL,
                        project_id NUMBER REFERENCES ASU_PROJECTS(project_id),
                        plan_id NUMBER REFERENCES ASU_TEST_PLANS(plan_id),
                        report_type VARCHAR2(50) CHECK (report_type IN ('PROGRESS', 'DEFECTS', 'COVERAGE', 'SUMMARY')),
                        report_data CLOB,
                        created_by NUMBER REFERENCES ASU_EMPLOYEES(employee_id),
                        created_date DATE DEFAULT SYSDATE,
                        report_date DATE
                    )
                    """
                ]
                
                for i, sql in enumerate(tables_sql):
                    try:
                        cur.execute(sql)
                        result.append(f"✅ Таблица {i+1} создана в схеме {current_schema}")
                    except Exception as e:
                        if "ORA-00955" in str(e):
                            result.append(f"ℹ️ Таблица {i+1} уже существует")
                        else:
                            raise e
                
                conn.commit()
                
            elif action == "create_sequences":
                cur.execute("ALTER SESSION SET CURRENT_SCHEMA = ASUTP")
                
                sequences_sql = [
                    "CREATE SEQUENCE SEQ_CLIENT_ID START WITH 1 INCREMENT BY 1",
                    "CREATE SEQUENCE SEQ_EMPLOYEE_ID START WITH 1 INCREMENT BY 1",
                    "CREATE SEQUENCE SEQ_PROJECT_ID START WITH 1 INCREMENT BY 1",
                    "CREATE SEQUENCE SEQ_PLAN_ID START WITH 1 INCREMENT BY 1",
                    "CREATE SEQUENCE SEQ_TESTCASE_ID START WITH 1 INCREMENT BY 1",
                    "CREATE SEQUENCE SEQ_DEFECT_ID START WITH 1 INCREMENT BY 1",
                    "CREATE SEQUENCE SEQ_REPORT_ID START WITH 1 INCREMENT BY 1"
                ]
                
                for sql in sequences_sql:
                    try:
                        cur.execute(sql)
                        result.append(f"✅ Последовательность создана")
                    except Exception as e:
                        if "ORA-00955" in str(e):
                            result.append(f"ℹ️ Последовательность уже существует")
                        else:
                            raise e
                
                conn.commit()
                
            elif action == "create_indexes":
                cur.execute("ALTER SESSION SET CURRENT_SCHEMA = ASUTP")
                
                indexes_sql = [
                    "CREATE INDEX IDX_CLIENTS_NAME ON ASU_CLIENTS(client_name)",
                    "CREATE INDEX IDX_CLIENTS_STATUS ON ASU_CLIENTS(status)",
                    "CREATE INDEX IDX_EMPLOYEES_NAME ON ASU_EMPLOYEES(last_name, first_name)",
                    "CREATE INDEX IDX_EMPLOYEES_STATUS ON ASU_EMPLOYEES(status)",
                    "CREATE INDEX IDX_PROJECTS_NAME ON ASU_PROJECTS(project_name)",
                    "CREATE INDEX IDX_PROJECTS_STATUS ON ASU_PROJECTS(status)",
                    "CREATE INDEX IDX_TESTCASES_NAME ON ASU_TEST_CASES(testcase_name)",
                    "CREATE INDEX IDX_TESTCASES_STATUS ON ASU_TEST_CASES(status)",
                    "CREATE INDEX IDX_DEFECTS_STATUS ON ASU_DEFECTS(status)",
                    "CREATE INDEX IDX_DEFECTS_SEVERITY ON ASU_DEFECTS(severity)"
                ]
                
                for sql in indexes_sql:
                    try:
                        cur.execute(sql)
                        result.append(f"✅ Индекс создан")
                    except Exception as e:
                        if "ORA-00955" in str(e):
                            result.append(f"ℹ️ Индекс уже существует")
                        else:
                            raise e
                
                conn.commit()
                
            elif action == "insert_test_data":
                cur.execute("ALTER SESSION SET CURRENT_SCHEMA = ASUTP")
                
                # Очищаем таблицы
                cur.execute("DELETE FROM ASU_DEFECTS")
                cur.execute("DELETE FROM ASU_TEST_CASES")
                cur.execute("DELETE FROM ASU_TEST_PLANS")
                cur.execute("DELETE FROM ASU_PROJECTS")
                cur.execute("DELETE FROM ASU_EMPLOYEES")
                cur.execute("DELETE FROM ASU_CLIENTS")
                
                # Сбрасываем последовательности
                cur.execute("DROP SEQUENCE SEQ_CLIENT_ID")
                cur.execute("DROP SEQUENCE SEQ_EMPLOYEE_ID")
                cur.execute("DROP SEQUENCE SEQ_PROJECT_ID")
                cur.execute("DROP SEQUENCE SEQ_PLAN_ID")
                cur.execute("DROP SEQUENCE SEQ_TESTCASE_ID")
                cur.execute("DROP SEQUENCE SEQ_DEFECT_ID")
                
                cur.execute("CREATE SEQUENCE SEQ_CLIENT_ID START WITH 1 INCREMENT BY 1")
                cur.execute("CREATE SEQUENCE SEQ_EMPLOYEE_ID START WITH 1 INCREMENT BY 1")
                cur.execute("CREATE SEQUENCE SEQ_PROJECT_ID START WITH 1 INCREMENT BY 1")
                cur.execute("CREATE SEQUENCE SEQ_PLAN_ID START WITH 1 INCREMENT BY 1")
                cur.execute("CREATE SEQUENCE SEQ_TESTCASE_ID START WITH 1 INCREMENT BY 1")
                cur.execute("CREATE SEQUENCE SEQ_DEFECT_ID START WITH 1 INCREMENT BY 1")
                
                # Клиенты
                cur.execute("""
                    INSERT INTO ASU_CLIENTS (client_id, client_name, contact_person, phone, email, priority)
                    VALUES (SEQ_CLIENT_ID.NEXTVAL, 'ООО "ТехноИнновации"', 'Иванов Петр', '+7(495)123-45-67', 'info@techno.ru', 1)
                """)
                cur.execute("""
                    INSERT INTO ASU_CLIENTS (client_id, client_name, contact_person, phone, email, priority)
                    VALUES (SEQ_CLIENT_ID.NEXTVAL, 'АО "Банк Финанс"', 'Сидорова Анна', '+7(495)234-56-78', 'contact@bankfinance.ru', 2)
                """)
                cur.execute("""
                    INSERT INTO ASU_CLIENTS (client_id, client_name, contact_person, phone, email, priority)
                    VALUES (SEQ_CLIENT_ID.NEXTVAL, 'ООО "Ритейл Плюс"', 'Петров Иван', '+7(495)345-67-89', 'info@retailplus.ru', 3)
                """)
                
                # Сотрудники
                cur.execute("""
                    INSERT INTO ASU_EMPLOYEES (employee_id, first_name, last_name, position, department, email, phone)
                    VALUES (SEQ_EMPLOYEE_ID.NEXTVAL, 'Алексей', 'Смирнов', 'Руководитель отдела', 'MANAGEMENT', 'a.smirnov@testlab.ru', '+7(903)111-22-33')
                """)
                cur.execute("""
                    INSERT INTO ASU_EMPLOYEES (employee_id, first_name, last_name, position, department, email, phone, manager_id)
                    VALUES (SEQ_EMPLOYEE_ID.NEXTVAL, 'Елена', 'Петрова', 'Ведущий тестировщик', 'TESTING', 'e.petrova@testlab.ru', '+7(903)222-33-44', 1)
                """)
                cur.execute("""
                    INSERT INTO ASU_EMPLOYEES (employee_id, first_name, last_name, position, department, email, phone, manager_id)
                    VALUES (SEQ_EMPLOYEE_ID.NEXTVAL, 'Дмитрий', 'Иванов', 'Тестировщик', 'TESTING', 'd.ivanov@testlab.ru', '+7(903)333-44-55', 2)
                """)
                cur.execute("""
                    INSERT INTO ASU_EMPLOYEES (employee_id, first_name, last_name, position, department, email, phone, manager_id)
                    VALUES (SEQ_EMPLOYEE_ID.NEXTVAL, 'Ольга', 'Соколова', 'Аналитик', 'ANALYSIS', 'o.sokolova@testlab.ru', '+7(903)444-55-66', 1)
                """)
                
                # Проекты
                cur.execute("""
                    INSERT INTO ASU_PROJECTS (project_id, project_name, client_id, description, start_date, priority, project_manager_id)
                    VALUES (SEQ_PROJECT_ID.NEXTVAL, 'Мобильное приложение "Банк-Клиент"', 2, 'Разработка и тестирование мобильного приложения для банка', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 1, 2)
                """)
                cur.execute("""
                    INSERT INTO ASU_PROJECTS (project_id, project_name, client_id, description, start_date, priority, project_manager_id)
                    VALUES (SEQ_PROJECT_ID.NEXTVAL, 'Интернет-магазин "Ритейл Плюс"', 3, 'Тестирование интернет-магазина', TO_DATE('2024-02-01', 'YYYY-MM-DD'), 2, 2)
                """)
                cur.execute("""
                    INSERT INTO ASU_PROJECTS (project_id, project_name, client_id, description, start_date, priority, project_manager_id)
                    VALUES (SEQ_PROJECT_ID.NEXTVAL, 'CRM для ТехноИнновации', 1, 'Внутренняя CRM система', TO_DATE('2023-10-10', 'YYYY-MM-DD'), 3, 1)
                """)
                
                # Планы тестирования
                cur.execute("""
                    INSERT INTO ASU_TEST_PLANS (plan_id, project_id, plan_name, version, release_date, status, created_by)
                    VALUES (SEQ_PLAN_ID.NEXTVAL, 1, 'Релиз 1.0 - Мобильное приложение', '1.0', TO_DATE('2024-03-15', 'YYYY-MM-DD'), 'IN_PROGRESS', 2)
                """)
                cur.execute("""
                    INSERT INTO ASU_TEST_PLANS (plan_id, project_id, plan_name, version, release_date, status, created_by)
                    VALUES (SEQ_PLAN_ID.NEXTVAL, 1, 'Релиз 1.1 - Мобильное приложение', '1.1', TO_DATE('2024-04-15', 'YYYY-MM-DD'), 'PLANNED', 2)
                """)
                cur.execute("""
                    INSERT INTO ASU_TEST_PLANS (plan_id, project_id, plan_name, version, release_date, status, created_by)
                    VALUES (SEQ_PLAN_ID.NEXTVAL, 2, 'Релиз 1.0 - Интернет-магазин', '1.0', TO_DATE('2024-03-01', 'YYYY-MM-DD'), 'COMPLETED', 3)
                """)
                
                # Тест-кейсы
                cur.execute("""
                    INSERT INTO ASU_TEST_CASES (testcase_id, testcase_name, project_id, plan_id, description, steps, expected_result, priority, author_id)
                    VALUES (SEQ_TESTCASE_ID.NEXTVAL, 'Проверка авторизации в мобильном приложении', 1, 1, 
                    'Тест проверяет возможность входа в приложение', 
                    '1. Открыть приложение\n2. Ввести логин\n3. Ввести пароль\n4. Нажать кнопку "Войти"', 
                    'Пользователь успешно входит в приложение', 1, 3)
                """)
                cur.execute("""
                    INSERT INTO ASU_TEST_CASES (testcase_id, testcase_name, project_id, plan_id, description, steps, expected_result, priority, author_id)
                    VALUES (SEQ_TESTCASE_ID.NEXTVAL, 'Проверка добавления товара в корзину', 2, 3, 
                    'Тест проверяет добавление товара в корзину', 
                    '1. Открыть сайт\n2. Найти товар\n3. Нажать "Добавить в корзину"', 
                    'Товар появляется в корзине', 2, 3)
                """)
                cur.execute("""
                    INSERT INTO ASU_TEST_CASES (testcase_id, testcase_name, project_id, plan_id, description, steps, expected_result, priority, author_id)
                    VALUES (SEQ_TESTCASE_ID.NEXTVAL, 'Проверка оформления заказа', 2, 3, 
                    'Тест проверяет оформление заказа', 
                    '1. Добавить товар в корзину\n2. Перейти к оформлению\n3. Заполнить данные\n4. Подтвердить заказ', 
                    'Заказ успешно оформлен', 1, 2)
                """)
                
                # Дефекты
                cur.execute("""
                    INSERT INTO ASU_DEFECTS (defect_id, defect_title, project_id, testcase_id, description, steps_to_reproduce, severity, priority, assigned_to, reported_by)
                    VALUES (SEQ_DEFECT_ID.NEXTVAL, 'Приложение вылетает при входе', 1, 1, 
                    'Краш приложения после ввода логина и пароля', 
                    '1. Открыть приложение\n2. Ввести логин\n3. Ввести пароль\n4. Нажать "Войти"', 
                    'CRITICAL', 1, 3, 2)
                """)
                cur.execute("""
                    INSERT INTO ASU_DEFECTS (defect_id, defect_title, project_id, testcase_id, description, steps_to_reproduce, severity, priority, assigned_to, reported_by)
                    VALUES (SEQ_DEFECT_ID.NEXTVAL, 'Неверный расчет суммы заказа', 2, 3, 
                    'Итоговая сумма заказа не совпадает с суммой товаров', 
                    '1. Добавить несколько товаров\n2. Перейти к оформлению\n3. Сравнить суммы', 
                    'MAJOR', 2, 3, 4)
                """)
                cur.execute("""
                    INSERT INTO ASU_DEFECTS (defect_id, defect_title, project_id, description, severity, priority, assigned_to, reported_by)
                    VALUES (SEQ_DEFECT_ID.NEXTVAL, 'Опечатка в интерфейсе', 2, 
                    'В кнопке "Оформить заказ" опечатка', 
                    'MINOR', 4, 3, 4)
                """)
                cur.execute("""
                    INSERT INTO ASU_DEFECTS (defect_id, defect_title, project_id, severity, priority, status, assigned_to, reported_by)
                    VALUES (SEQ_DEFECT_ID.NEXTVAL, 'Медленная загрузка страницы', 1, 'MAJOR', 3, 'OPEN', 3, 2)
                """)
                
                conn.commit()
                result.append("✅ Тестовые данные успешно добавлены")
                
            elif action == "check_status":
                cur.execute("ALTER SESSION SET CURRENT_SCHEMA = ASUTP")
                
                # Проверяем существование таблиц
                cur.execute("SELECT table_name FROM user_tables WHERE table_name LIKE 'ASU_%'")
                tables = cur.fetchall()
                result.append(f"📊 Найдено таблиц: {len(tables)}")
                for table in tables:
                    cur.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cur.fetchone()[0]
                    result.append(f"   - {table[0]}: {count} записей")
            
            cur.close()
            conn.close()
            
        except Exception as e:
            error = str(e)
            if conn:
                conn.rollback()
    
    return render_template("seminar1/task3_setup.html", result=result, error=error)

@app.route("/seminar1/task3_diagnostic")
@login_required
def seminar1_task3_diagnostic():
    """Диагностика подключения к ASUTP"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Текущий пользователь
        cur.execute("SELECT USER FROM dual")
        current_user = cur.fetchone()[0]
        
        # Текущая схема
        cur.execute("SELECT SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') FROM dual")
        current_schema = cur.fetchone()[0]
        
        # Все пользователи (первые 10)
        cur.execute("SELECT username FROM all_users ORDER BY username FETCH FIRST 10 ROWS ONLY")
        users = [row[0] for row in cur.fetchall()]
        
        # Проверяем существование пользователя ASUTP
        cur.execute("SELECT COUNT(*) FROM all_users WHERE username = 'ASUTP'")
        asutp_exists = cur.fetchone()[0] > 0
        
        # Таблицы в текущей схеме
        cur.execute("""
            SELECT table_name, num_rows 
            FROM user_tables 
            WHERE table_name LIKE 'ASU_%'
            ORDER BY table_name
        """)
        my_tables = cur.fetchall()
        
        # Таблицы ASUTP (если доступны)
        cur.execute("ALTER SESSION SET CURRENT_SCHEMA = ASUTP")
        cur.execute("SELECT SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') FROM dual")
        after_switch = cur.fetchone()[0]
        
        cur.execute("""
            SELECT table_name, num_rows 
            FROM user_tables 
            WHERE table_name LIKE 'ASU_%'
            ORDER BY table_name
        """)
        asutp_tables = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return f"""
        <html>
        <head>
            <title>Диагностика ASUTP</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial; padding: 20px; }}
                .success {{ color: green; }}
                .error {{ color: red; }}
                .warning {{ color: orange; }}
                table {{ border-collapse: collapse; margin: 10px 0; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .box {{ 
                    border: 1px solid #ddd; 
                    padding: 15px; 
                    margin: 20px 0;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }}
            </style>
        </head>
        <body>
            <h1>Диагностика подключения ASUTP</h1>
            
            <div class="box">
                <h2>Информация о подключении</h2>
                <table>
                    <tr><th>Параметр</th><th>Значение</th></tr>
                    <tr><td>Текущий пользователь</td><td><strong>{current_user}</strong></td></tr>
                    <tr><td>Текущая схема</td><td><strong>{current_schema}</strong></td></tr>
                    <tr><td>После переключения на ASUTP</td><td>{after_switch}</td></tr>
                    <tr><td>Пользователь ASUTP существует</td>
                        <td class="{'success' if asutp_exists else 'error'}">
                            {'✅ Да' if asutp_exists else '❌ Нет'}
                        </td>
                    </tr>
                </table>
            </div>
            
            <div class="box">
                <h2>Доступные пользователи</h2>
                <p>{', '.join(users)}</p>
            </div>
            
            <div class="box">
                <h2>Таблицы в текущей схеме ({current_schema})</h2>
                <table>
                    <tr><th>Таблица</th><th>Записей</th></tr>
                    {"".join(f"<tr><td>{t[0]}</td><td>{t[1] or 0}</td></tr>" for t in my_tables) if my_tables else "<tr><td colspan='2'>Нет таблиц ASU_*</td></tr>"}
                </table>
            </div>
            
            <div class="box">
                <h2>Таблицы в схеме ASUTP (после переключения)</h2>
                <table>
                    <tr><th>Таблица</th><th>Записей</th></tr>
                    {"".join(f"<tr><td>{t[0]}</td><td>{t[1] or 0}</td></tr>" for t in asutp_tables) if asutp_tables else "<tr><td colspan='2'>Нет таблиц ASU_* или нет доступа</td></tr>"}
                </table>
            </div>
            
            <div class="box">
                <h2>Рекомендации</h2>
                <ul>
                    <li>Если таблицы видны в схеме ASUTP, значит проблема в параметрах подключения</li>
                    <li>Если таблицы видны в текущей схеме, значит они создались не там</li>
                    <li>Попробуйте выполнить: <code>ALTER SESSION SET CURRENT_SCHEMA = ASUTP</code> перед запросами</li>
                </ul>
            </div>
            
            <p><a href="/seminar1/task3_setup">← Вернуться к настройке</a></p>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
        <body>
            <h1 class="error">Ошибка диагностики</h1>
            <pre>{str(e)}</pre>
        </body>
        </html>
        """

@app.route("/seminar1/task3_final_check")
@login_required
def seminar1_task3_final_check():
    """Финальная проверка - где таблицы?"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Текущий пользователь и схема
        cur.execute("SELECT USER FROM dual")
        current_user = cur.fetchone()[0]
        
        cur.execute("SELECT SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') FROM dual")
        current_schema = cur.fetchone()[0]
        
        # Поиск таблиц во всех схемах
        cur.execute("""
            SELECT owner, table_name 
            FROM all_tables 
            WHERE table_name LIKE 'ASU_%'
            ORDER BY owner, table_name
        """)
        all_tables = cur.fetchall()
        
        # Проверяем права доступа к ASUTP
        try:
            cur.execute("ALTER SESSION SET CURRENT_SCHEMA = ASUTP")
            cur.execute("SELECT SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') FROM dual")
            asutp_schema = cur.fetchone()[0]
            
            cur.execute("SELECT table_name FROM user_tables WHERE table_name LIKE 'ASU_%'")
            asutp_tables = cur.fetchall()
        except Exception as e:
            asutp_schema = f"Ошибка доступа: {str(e)}"
            asutp_tables = []
        
        cur.close()
        conn.close()
        
        return f"""
        <html>
        <head>
            <title>Финальная проверка</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial; padding: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                .success {{ color: green; font-weight: bold; }}
                .error {{ color: red; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>🔍 Финальная проверка таблиц ASU</h1>
            
            <h2>Текущее подключение:</h2>
            <ul>
                <li><strong>Пользователь:</strong> {current_user}</li>
                <li><strong>Текущая схема:</strong> {current_schema}</li>
            </ul>
            
            <h2>Где создались таблицы?</h2>
            <table>
                <tr>
                    <th>Владелец (схема)</th>
                    <th>Таблица</th>
                </tr>
                {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td></tr>" for row in all_tables) if all_tables else "<tr><td colspan='2'>Таблицы ASU_* не найдены ни в одной схеме</td></tr>"}
            </table>
            
            <h2>Доступ к схеме ASUTP:</h2>
            <p><strong>Результат переключения:</strong> {asutp_schema}</p>
            
            <h3>Таблицы в ASUTP:</h3>
            <ul>
                {"".join(f"<li>{t[0]}</li>" for t in asutp_tables) if asutp_tables else "<li>Нет таблиц или нет доступа</li>"}
            </ul>
            
            <h2>Рекомендации:</h2>
            <ul>
                <li>Если таблицы есть в колонке "Владелец" - это их реальное местоположение</li>
                <li>Если таблицы в ASUTP не видны, но есть в другой схеме - нужно создать синонимы</li>
                <li>Если таблиц нет нигде - они не создались</li>
            </ul>
            
            <p><a href="/seminar1/task3_setup">← Вернуться к настройке</a></p>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Ошибка</h1><pre>{str(e)}</pre>"


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/db-test")
def db_test():
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM dual")
                row = cur.fetchone()
        return jsonify({"status": "ok", "result": int(row[0])})
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 500


# ===== Примеры =====

@app.route("/examples")
def example_index():
    return render_template("example/index.html")

@app.route("/examples/example1")
def example_1():
    return render_template("example/example1.html")

@app.route("/examples/example2")
def example_2():
    return render_template("example/example2.html")

@app.route("/examples/example3", methods=["GET", "POST"])
def example_3():
    name = None
    
    if request.method == "POST":
        name = request.form.get("name")
    
    return render_template("example/example3.html", name=name)

@app.route("/examples/example4", methods=["GET"])
def example_4():
    name = request.args.get("name")
    email = request.args.get("email")

    return render_template("example/example4.html", name=name, email=email)

@app.route("/examples/example5", methods=["GET", "POST"])
def example_5():
    result = ""

    if request.method == "POST":
        kurs = request.form.get("kurs")
        times = request.form.getlist("times")  # список выбранных checkbox

        result += f"<p>Мой любимый предмет: <i>{kurs}</i></p>"

        favorite_times = len(times)

        if favorite_times <= 1:
            times_message = "не ботан"
        elif 1 < favorite_times < 4:
            times_message = "ботаю иногда"
        else:
            times_message = "ботан"

        result += f"<p>Я <i>{times_message}</i></p>"

    return render_template("example/example5.html", result=result)

@app.route("/examples/example6", methods=["GET", "POST"])
def example_6():
    result = None
    
    if request.method == "POST":
        try:
            with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1 FROM dual")
                    row = cur.fetchone()
                    
            result = {
                "status": "success",
                "message": "✅ Подключение успешно!"
            }
            
        except Exception as e:
            result = {
                "status": "error", 
                "message": f"❌ Ошибка: {str(e)}"
            }

    return render_template("example/example6.html", result=result)

@app.route("/examples/example7")
def example_7():
    try:
        # Подключение к БД
        con = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        cur = con.cursor()
        # Выполняем запрос
        cur.execute("SELECT object_name, object_type FROM user_objects")
        
        # Получаем все строки
        objects = cur.fetchall()
        
        cur.close()
        con.close()
        
        return render_template("example/example7.html", objects=objects)
        
    except oracledb.DatabaseError as e:
        error, = e.args
        return render_template("example/example7.html", error=str(error.message))
    except Exception as e:
        return render_template("example/example7.html", error=str(e))

@app.route("/examples/example8")
def example_8():
    try:
        con = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        cur = con.cursor()
        
        # Разные вычисления в Oracle
        cur.execute("SELECT SIN(3.14) FROM dual")
        (sin_val,) = cur.fetchone()
        
        cur.execute("SELECT COS(3.14) FROM dual")
        (cos_val,) = cur.fetchone()
        
        cur.execute("SELECT EXP(2) FROM dual")
        (exp_val,) = cur.fetchone()
        
        cur.execute("SELECT POWER(5, 3) FROM dual")
        (power_val,) = cur.fetchone()
        
        cur.execute("SELECT SQRT(16) FROM dual")
        (sqrt_val,) = cur.fetchone()
        
        cur.execute("SELECT MOD(10, 3) FROM dual")
        (mod_val,) = cur.fetchone()
        
        cur.execute("SELECT ROUND(3.14159, 2) FROM dual")
        (round_val,) = cur.fetchone()
        
        cur.execute("SELECT TRUNC(3.14159, 2) FROM dual")
        (trunc_val,) = cur.fetchone()
        
        cur.execute("SELECT ABS(-10) FROM dual")
        (abs_val,) = cur.fetchone()
        
        con.commit()
        cur.close()
        con.close()
        
        calculations = {
            "sin": sin_val,
            "cos": cos_val,
            "exp": exp_val,
            "power": power_val,
            "sqrt": sqrt_val,
            "mod": mod_val,
            "round": round_val,
            "trunc": trunc_val,
            "abs": abs_val
        }
        
        return render_template("example/example8.html", calc=calculations)
        
    except oracledb.DatabaseError as e:
        error, = e.args
        return render_template("example/example8.html", error=str(error.message))
    except Exception as e:
        return render_template("example/example8.html", error=str(e))

@app.route("/examples/example9")
def example_9():
    return render_template("example/example9.html")

# ===== СЕМИНАР 1 =====

@app.route("/seminar1")
def seminar1_index():
    return render_template("seminar1/index.html")

@app.route("/seminar1/task1", methods=["GET", "POST"])
def seminar1_task1():
    """
    Семинар 1 – задание 1:
    Демонстрация обработки полей SELECT и списка интересов (чекбоксы).
    """
    faculty_names = {
        "iu4": "ИУ4 – Радиоэлектроника",
        "iu5": "ИУ5 – Компьютерные системы",
        "iu7": "ИУ7 – Программная инженерия",
        "bmstu": "МГТУ им. Баумана (общее)",
    }

    interest_names = {
        "python": "Python",
        "databases": "Базы данных",
        "networks": "Компьютерные сети",
        "hardware": "Микроконтроллеры и железо",
        "math": "Математика",
        "other": "Другое",
    }

    if request.method == "GET":
        return render_template(
            "seminar1/task1.html",
            faculty_names=faculty_names,
            interest_names=interest_names,
        )

    faculty = request.form.get("faculty")
    interests = request.form.getlist("interests")

    faculty_text = faculty_names.get(faculty, "не выбрано")
    interests_text = [interest_names.get(i, i) for i in interests]

    return render_template(
        "seminar1/task1_result.html",
        faculty_text=faculty_text,
        interests_text=interests_text,
    )

@app.route("/seminar1/task2")
def seminar1_task2():
    try:
        # Подключение к Oracle
        con = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        cur = con.cursor()
        
        # Вычисляем функции с точностью 5 знаков
        cur.execute("""
            SELECT
                ROUND(SIN(3.14), 5),
                ROUND(COS(3.14), 5),
                ROUND(TAN(3.14/4), 5),
                ROUND(SQRT(2), 5),
                ROUND(EXP(1), 5),
                ROUND(POWER(2, 8), 5),
                ROUND(ABS(-12.345678), 5),
                ROUND(LOG(10, 100), 5),
                ROUND(MOD(17, 5), 5),
                ROUND(CEIL(4.2), 5),
                ROUND(FLOOR(4.8), 5)
            FROM dual
        """)

        result = cur.fetchone()
        
        cur.close()
        con.close()
        
        # Распаковываем результаты
        functions = {
            'sin': result[0],
            'cos': result[1],
            'tan': result[2],
            'sqrt': result[3],
            'exp': result[4],
            'power': result[5],
            'abs': result[6],
            'log': result[7],
            'mod': result[8],
            'ceil': result[9],
            'floor': result[10]
        }
        
        return render_template("seminar1/task2.html", functions=functions)
        
    except oracledb.DatabaseError as e:
        error, = e.args
        return render_template("seminar1/task2.html", error=str(error.message))
    except Exception as e:
        return render_template("seminar1/task2.html", error=str(e))

@app.route("/seminar1/task3")
def seminar1_task3():
    """Шаблон интерфейса АСУ отдела тестирования ПО."""
    # execute_sql_script("create_asu_tables.sql")
    return render_template("seminar1/task3.html", title="АСУ отдела тестирования ПО")

@app.route("/seminar1/task4")
def seminar1_task4():
    try:
        con = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        cur = con.cursor()
        
        # 1. Выбор служащих по диапазону окладов (3000-4000)
        cur.execute("""
            SELECT first_name, last_name, salary 
            FROM HR.EMPLOYEES 
            WHERE salary BETWEEN 3000 AND 4000 
            ORDER BY salary DESC
        """)
        task1_result = cur.fetchall()
        task1_count = len(task1_result)
        
        # 2. Выбор подчиненных менеджеров (105, 149, 205)
        cur.execute("""
            SELECT first_name, last_name, manager_id 
            FROM HR.EMPLOYEES 
            WHERE manager_id IN (105, 149, 205)
        """)
        task2_result = cur.fetchall()
        task2_count = len(task2_result)
        
        # 3. Выбор сотрудников по буквам Email (вторая буква 'H')
        cur.execute("""
            SELECT last_name, email, phone_number 
            FROM HR.EMPLOYEES 
            WHERE email LIKE '_H%'
        """)
        task3_result = cur.fetchall()
        task3_count = len(task3_result)
        
        # 4. Выбор сотрудников без комиссионных
        cur.execute("""
            SELECT last_name, salary, commission_pct 
            FROM HR.EMPLOYEES 
            WHERE commission_pct IS NULL 
            ORDER BY salary
        """)
        task4_result = cur.fetchall()
        task4_count = len(task4_result)
        
        # 5. Выбор высокооплачиваемых сотрудников отдела 60
        cur.execute("""
            SELECT first_name, last_name, salary, phone_number 
            FROM HR.EMPLOYEES 
            WHERE department_id = 60 AND salary > 3000 
            ORDER BY salary DESC
        """)
        task5_result = cur.fetchall()
        task5_count = len(task5_result)
        
        # 6. Выбор IT сотрудников или с комиссионными
        cur.execute("""
            SELECT first_name, last_name, salary, commission_pct, job_id 
            FROM HR.EMPLOYEES 
            WHERE job_id LIKE 'IT%' OR commission_pct IS NOT NULL
        """)
        task6_result = cur.fetchall()
        task6_count = len(task6_result)
        
        # 7. Выбор сотрудников не подчиняющихся менеджерам 105,149,205
        cur.execute("""
            SELECT first_name, last_name, manager_id 
            FROM HR.EMPLOYEES 
            WHERE manager_id NOT IN (105, 149, 205) 
            ORDER BY last_name
        """)
        task7_result = cur.fetchall()
        task7_count = len(task7_result)
        
        # 8. Дата поступления на работу
        cur.execute("""
            SELECT first_name, last_name, hire_date 
            FROM HR.EMPLOYEES 
            ORDER BY hire_date
        """)
        task8_result = cur.fetchall()
        task8_count = len(task8_result)
        
        # 9. Телефоны служащих по отделам
        cur.execute("""
            SELECT department_id, last_name, phone_number 
            FROM HR.EMPLOYEES 
            ORDER BY department_id, last_name
        """)
        task9_result = cur.fetchall()
        task9_count = len(task9_result)
        
        # 10. Взаимосвязь подразделений
        cur.execute("""
            SELECT d.department_id dep,
                   e.employee_id manager_id,
                   q.employee_id head_manager_id,
                   q.department_id head_dep
            FROM hr.departments d, hr.employees e, hr.employees q
            WHERE d.manager_id IS NOT NULL
              AND d.manager_id = e.employee_id
              AND e.manager_id = q.employee_id
            ORDER BY dep ASC
        """)
        task10_result = cur.fetchall()
        task10_count = len(task10_result)
        
        cur.close()
        con.close()
        
        tasks = {
            '1': {'result': task1_result, 'count': task1_count, 'expected': 19,
                  'title': 'Выбор служащих по диапазону окладов',
                  'sql': 'SELECT first_name, last_name, salary FROM HR.EMPLOYEES WHERE salary BETWEEN 3000 AND 4000 ORDER BY salary DESC;'},
            '2': {'result': task2_result, 'count': task2_count, 'expected': 7,
                  'title': 'Выбор подчиненных менеджеров',
                  'sql': 'SELECT first_name, last_name, manager_id FROM HR.EMPLOYEES WHERE manager_id IN (105,149,205);'},
            '3': {'result': task3_result, 'count': task3_count, 'expected': 6,
                  'title': 'Выбор сотрудников по буквам Email',
                  'sql': 'SELECT last_name, email, phone_number FROM HR.EMPLOYEES WHERE email LIKE \'_H%\';'},
            '4': {'result': task4_result, 'count': task4_count, 'expected': 72,
                  'title': 'Выбор сотрудников без комиссионных',
                  'sql': 'SELECT last_name, salary, commission_pct FROM HR.EMPLOYEES WHERE commission_pct IS NULL ORDER BY salary;'},
            '5': {'result': task5_result, 'count': task5_count, 'expected': 5,
                  'title': 'Выбор высокооплачиваемых сотрудников отдела 60',
                  'sql': 'SELECT first_name,last_name, salary, phone_number FROM HR.EMPLOYEES WHERE department_id=60 and salary>3000 ORDER BY salary DESC;'},
            '6': {'result': task6_result, 'count': task6_count, 'expected': 40,
                  'title': 'Выбор IT сотрудников или с комиссионными',
                  'sql': 'SELECT first_name, last_name, salary,commission_pct, job_id FROM HR.EMPLOYEES WHERE job_id LIKE \'IT%\' OR commission_pct IS NOT NULL;'},
            '7': {'result': task7_result, 'count': task7_count, 'expected': 99,
                  'title': 'Выбор сотрудников не подчиняющихся менеджерам',
                  'sql': 'SELECT first_name, last_name, manager_id FROM HR.EMPLOYEES WHERE manager_id NOT IN (105,149,205) ORDER BY last_name;'},
            '8': {'result': task8_result, 'count': task8_count, 'expected': 107,
                  'title': 'Дата поступления на работу',
                  'sql': 'SELECT first_name, last_name, hire_date FROM HR.EMPLOYEES ORDER BY hire_date;'},
            '9': {'result': task9_result, 'count': task9_count, 'expected': 107,
                  'title': 'Телефоны служащих по отделам',
                  'sql': 'SELECT department_id, last_name, phone_number FROM HR.EMPLOYEES ORDER BY department_id, last_name;'},
            '10': {'result': task10_result, 'count': task10_count, 'expected': 10,
                   'title': 'Взаимосвязь подразделений',
                   'sql': 'SELECT d.department_id dep, e.employee_id manager_id, q.employee_id head_manager_id, q.department_id head_dep FROM hr.departments d, hr.employees e, hr.employees q WHERE d.manager_id IS NOT NULL AND d.manager_id = e.employee_id AND e.manager_id = q.employee_id ORDER BY dep ASC;'}
        }
        
        return render_template("seminar1/task4.html", tasks=tasks)
        
    except oracledb.DatabaseError as e:
        error, = e.args
        return render_template("seminar1/task4.html", error=str(error.message))
    except Exception as e:
        return render_template("seminar1/task4.html", error=str(e))

@app.route("/seminar1/task3_advanced")
def seminar1_task3_advanced():
    """Расширенная версия АСУ с реальной БД"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Получаем статистику для карточек (прямым запросом, без представления)
        cur.execute("""
            SELECT 
                (SELECT COUNT(*) FROM asu_clients WHERE status = 'ACTIVE') as active_clients,
                (SELECT COUNT(*) FROM asu_projects WHERE status = 'ACTIVE') as active_projects,
                (SELECT COUNT(*) FROM asu_defects WHERE status IN ('OPEN', 'IN_PROGRESS', 'REOPENED')) as open_defects,
                (SELECT COUNT(*) FROM asu_test_cases WHERE status = 'ACTIVE') as active_testcases,
                (SELECT COUNT(*) FROM asu_test_plans WHERE status IN ('PLANNED', 'IN_PROGRESS')) as active_plans
            FROM dual
        """)
        stats_row = cur.fetchone()
        
        # Получаем список проектов
        cur.execute("""
            SELECT project_id, project_name 
            FROM asu_projects 
            WHERE status = 'ACTIVE' 
            ORDER BY project_name
        """)
        projects = cur.fetchall()
        
        # Получаем список релизов
        cur.execute("""
            SELECT plan_id, plan_name, version 
            FROM asu_test_plans 
            WHERE status IN ('PLANNED', 'IN_PROGRESS')
            ORDER BY release_date DESC
        """)
        releases = cur.fetchall()
        
        cur.close()
        conn.close()
        
        stats = {
            'active_clients': stats_row[0] if stats_row else 0,
            'active_projects': stats_row[1] if stats_row else 0,
            'open_defects': stats_row[2] if stats_row else 0,
            'active_testcases': stats_row[3] if stats_row else 0,
            'active_plans': stats_row[4] if stats_row else 0
        }
        
        return render_template(
            "seminar1/task3_advanced.html", 
            stats=stats,
            projects=projects,
            releases=releases,
            error=None
        )
        
    except oracledb.DatabaseError as e:
        error, = e.args
        # Возвращаем шаблон с пустыми данными, чтобы избежать UndefinedError
        return render_template(
            "seminar1/task3_advanced.html", 
            stats={'active_clients':0, 'active_projects':0, 'open_defects':0, 'active_testcases':0, 'active_plans':0},
            projects=[],
            releases=[],
            error=str(error.message)
        )
    except Exception as e:
        return render_template(
            "seminar1/task3_advanced.html", 
            stats={'active_clients':0, 'active_projects':0, 'open_defects':0, 'active_testcases':0, 'active_plans':0},
            projects=[],
            releases=[],
            error=str(e)
        )

@app.route("/seminar1/task3_advanced/data")
def seminar1_task3_advanced_data():
    """API для получения данных с фильтрацией"""
    entity = request.args.get('entity', 'clients')
    search = request.args.get('q', '')
    only_active = request.args.get('only_active') == 'true'
    has_open_bugs = request.args.get('has_open_bugs') == 'true'
    has_test_plan = request.args.get('has_test_plan') == 'true'
    project_filter = request.args.get('project', '')
    release_filter = request.args.get('release', '')
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        data = []
        columns = []
        
        if entity == 'clients':
            query = """
                SELECT c.client_id, c.client_name, c.status, c.priority, 
                       e.last_name || ' ' || e.first_name as responsible,
                       (SELECT COUNT(*) FROM asu_projects p WHERE p.client_id = c.client_id) as projects_count
                FROM asu_clients c
                LEFT JOIN asu_employees e ON c.responsible_emp_id = e.employee_id
                WHERE 1=1
            """
            params = []
            
            if search:
                query += " AND LOWER(c.client_name) LIKE LOWER(:1)"
                params.append(f'%{search}%')
            
            if only_active:
                query += " AND c.status = 'ACTIVE'"
            
            if has_open_bugs:
                query += """
                    AND EXISTS (
                        SELECT 1 FROM asu_projects p 
                        JOIN asu_defects d ON p.project_id = d.project_id
                        WHERE p.client_id = c.client_id 
                        AND d.status IN ('OPEN', 'IN_PROGRESS', 'REOPENED')
                    )
                """
            
            cur.execute(query, params)
            rows = cur.fetchall()
            
            for row in rows:
                data.append({
                    'id': row[0],
                    'name': row[1],
                    'status': row[2],
                    'priority': row[3],
                    'responsible': row[4] or 'Не назначен',
                    'projects_count': row[5]
                })
            
            columns = ['ID', 'Название компании', 'Статус', 'Приоритет', 'Ответственный']
            
        elif entity == 'employees':
            query = """
                SELECT employee_id, first_name, last_name, position, department, status,
                       (SELECT COUNT(*) FROM asu_projects WHERE project_manager_id = employee_id) as projects_managed
                FROM asu_employees
                WHERE 1=1
            """
            params = []
            
            if search:
                query += " AND (LOWER(first_name) LIKE LOWER(:1) OR LOWER(last_name) LIKE LOWER(:1))"
                params.append(f'%{search}%')
            
            if only_active:
                query += " AND status = 'ACTIVE'"
            
            cur.execute(query, params)
            rows = cur.fetchall()
            
            for row in rows:
                data.append({
                    'id': row[0],
                    'name': f"{row[1]} {row[2]}",
                    'position': row[3],
                    'department': row[4],
                    'status': row[5],
                    'projects': row[6]
                })
            
            columns = ['ID', 'ФИО', 'Должность', 'Отдел', 'Статус']
            
        elif entity == 'projects':
            query = """
                SELECT p.project_id, p.project_name, c.client_name, p.status, p.priority,
                       e.last_name || ' ' || e.first_name as manager,
                       (SELECT COUNT(*) FROM asu_test_plans tp WHERE tp.project_id = p.project_id) as plans_count,
                       (SELECT COUNT(*) FROM asu_defects d WHERE d.project_id = p.project_id AND d.status IN ('OPEN', 'IN_PROGRESS')) as open_defects
                FROM asu_projects p
                LEFT JOIN asu_clients c ON p.client_id = c.client_id
                LEFT JOIN asu_employees e ON p.project_manager_id = e.employee_id
                WHERE 1=1
            """
            params = []
            
            if search:
                query += " AND LOWER(p.project_name) LIKE LOWER(:1)"
                params.append(f'%{search}%')
            
            if only_active:
                query += " AND p.status = 'ACTIVE'"
            
            if project_filter:
                query += " AND p.project_id = :2"
                params.append(project_filter)
            
            if has_open_bugs:
                query += " AND EXISTS (SELECT 1 FROM asu_defects d WHERE d.project_id = p.project_id AND d.status IN ('OPEN', 'IN_PROGRESS'))"
            
            if has_test_plan:
                query += " AND EXISTS (SELECT 1 FROM asu_test_plans tp WHERE tp.project_id = p.project_id)"
            
            cur.execute(query, params)
            rows = cur.fetchall()
            
            for row in rows:
                data.append({
                    'id': row[0],
                    'name': row[1],
                    'client': row[2] or 'Нет клиента',
                    'status': row[3],
                    'priority': row[4],
                    'manager': row[5] or 'Не назначен',
                    'plans': row[6],
                    'defects': row[7]
                })
            
            columns = ['ID', 'Проект', 'Клиент', 'Статус', 'Приоритет', 'Менеджер']
            
        elif entity == 'testcases':
            query = """
                SELECT tc.testcase_id, tc.testcase_name, p.project_name, tc.priority, tc.status,
                       e.last_name || ' ' || e.first_name as author,
                       (SELECT COUNT(*) FROM asu_defects d WHERE d.testcase_id = tc.testcase_id) as defects_count
                FROM asu_test_cases tc
                LEFT JOIN asu_projects p ON tc.project_id = p.project_id
                LEFT JOIN asu_employees e ON tc.author_id = e.employee_id
                WHERE 1=1
            """
            params = []
            
            if search:
                query += " AND LOWER(tc.testcase_name) LIKE LOWER(:1)"
                params.append(f'%{search}%')
            
            if only_active:
                query += " AND tc.status = 'ACTIVE'"
            
            if project_filter:
                query += " AND tc.project_id = :2"
                params.append(project_filter)
            
            if release_filter:
                query += " AND tc.plan_id = :3"
                params.append(release_filter)
            
            if has_open_bugs:
                query += " AND EXISTS (SELECT 1 FROM asu_defects d WHERE d.testcase_id = tc.testcase_id)"
            
            cur.execute(query, params)
            rows = cur.fetchall()
            
            for row in rows:
                data.append({
                    'id': row[0],
                    'name': row[1],
                    'project': row[2] or 'Нет проекта',
                    'priority': row[3],
                    'status': row[4],
                    'author': row[5] or 'Неизвестен',
                    'defects': row[6]
                })
            
            columns = ['ID', 'Название тест-кейса', 'Проект', 'Приоритет', 'Статус', 'Автор']
            
        elif entity == 'bugs':
            query = """
                SELECT d.defect_id, d.defect_title, p.project_name, d.severity, d.priority, d.status,
                       e.last_name || ' ' || e.first_name as assigned,
                       TO_CHAR(d.created_date, 'DD.MM.YYYY') as created
                FROM asu_defects d
                LEFT JOIN asu_projects p ON d.project_id = p.project_id
                LEFT JOIN asu_employees e ON d.assigned_to = e.employee_id
                WHERE 1=1
            """
            params = []
            
            if search:
                query += " AND LOWER(d.defect_title) LIKE LOWER(:1)"
                params.append(f'%{search}%')
            
            if only_active:
                query += " AND d.status IN ('OPEN', 'IN_PROGRESS', 'REOPENED')"
            
            if project_filter:
                query += " AND d.project_id = :2"
                params.append(project_filter)
            
            if has_test_plan:
                query += " AND EXISTS (SELECT 1 FROM asu_test_plans tp WHERE tp.project_id = d.project_id)"
            
            cur.execute(query, params)
            rows = cur.fetchall()
            
            for row in rows:
                data.append({
                    'id': row[0],
                    'title': row[1],
                    'project': row[2] or 'Нет проекта',
                    'severity': row[3],
                    'priority': row[4],
                    'status': row[5],
                    'assigned': row[6] or 'Не назначен',
                    'created': row[7]
                })
            
            columns = ['ID', 'Название', 'Проект', 'Серьезность', 'Приоритет', 'Статус', 'Назначен']
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': data,
            'columns': columns,
            'count': len(data)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route("/seminar1/task3_advanced/add/<entity>", methods=["GET", "POST"])
@login_required
def seminar1_task3_advanced_add(entity):
    """Добавление новой записи"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if request.method == "POST":
            if entity == "clients":
                cur.execute("""
                    INSERT INTO asu_clients (client_id, client_name, contact_person, phone, email, priority, responsible_emp_id)
                    VALUES (seq_client_id.NEXTVAL, :1, :2, :3, :4, :5, :6)
                """, (
                    request.form['client_name'],
                    request.form.get('contact_person', ''),
                    request.form.get('phone', ''),
                    request.form.get('email', ''),
                    int(request.form['priority']),
                    int(request.form['responsible']) if request.form.get('responsible') else None
                ))
                
            elif entity == "employees":
                cur.execute("""
                    INSERT INTO asu_employees (employee_id, first_name, last_name, position, department, email, phone, manager_id)
                    VALUES (seq_employee_id.NEXTVAL, :1, :2, :3, :4, :5, :6, :7)
                """, (
                    request.form['first_name'],
                    request.form['last_name'],
                    request.form['position'],
                    request.form['department'],
                    request.form['email'],
                    request.form.get('phone', ''),
                    int(request.form['manager_id']) if request.form.get('manager_id') else None
                ))
                
            elif entity == "projects":
                cur.execute("""
                    INSERT INTO asu_projects (project_id, project_name, client_id, description, start_date, priority, project_manager_id)
                    VALUES (seq_project_id.NEXTVAL, :1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6)
                """, (
                    request.form['project_name'],
                    int(request.form['client_id']) if request.form.get('client_id') else None,
                    request.form.get('description', ''),
                    request.form['start_date'],
                    int(request.form['priority']),
                    int(request.form['manager_id']) if request.form.get('manager_id') else None
                ))
                
            elif entity == "testcases":
                cur.execute("""
                    INSERT INTO asu_test_cases (testcase_id, testcase_name, project_id, plan_id, description, steps, expected_result, priority, author_id)
                    VALUES (seq_testcase_id.NEXTVAL, :1, :2, :3, :4, :5, :6, :7, :8)
                """, (
                    request.form['testcase_name'],
                    int(request.form['project_id']) if request.form.get('project_id') else None,
                    int(request.form['plan_id']) if request.form.get('plan_id') else None,
                    request.form.get('description', ''),
                    request.form.get('steps', ''),
                    request.form.get('expected_result', ''),
                    int(request.form['priority']),
                    int(request.form['author_id']) if request.form.get('author_id') else None
                ))
                
            elif entity == "bugs":
                cur.execute("""
                    INSERT INTO asu_defects (defect_id, defect_title, project_id, testcase_id, description, steps_to_reproduce, severity, priority, reported_by)
                    VALUES (seq_defect_id.NEXTVAL, :1, :2, :3, :4, :5, :6, :7, :8)
                """, (
                    request.form['defect_title'],
                    int(request.form['project_id']) if request.form.get('project_id') else None,
                    int(request.form['testcase_id']) if request.form.get('testcase_id') else None,
                    request.form.get('description', ''),
                    request.form.get('steps_to_reproduce', ''),
                    request.form['severity'],
                    int(request.form['priority']),
                    int(request.form['reported_by']) if request.form.get('reported_by') else None
                ))
            
            conn.commit()
            cur.close()
            conn.close()
            
            return redirect(url_for('seminar1_task3_advanced'))
        
        # GET запрос - получаем справочные данные для формы
        employees = []
        clients = []
        projects = []
        plans = []
        testcases = []
        
        if entity in ["clients", "projects"]:
            cur.execute("SELECT employee_id, first_name, last_name FROM asu_employees WHERE status = 'ACTIVE'")
            employees = cur.fetchall()
        
        if entity in ["projects", "testcases", "bugs"]:
            cur.execute("SELECT client_id, client_name FROM asu_clients WHERE status = 'ACTIVE'")
            clients = cur.fetchall()
            
            cur.execute("SELECT project_id, project_name FROM asu_projects WHERE status = 'ACTIVE'")
            projects = cur.fetchall()
        
        if entity == "testcases":
            cur.execute("SELECT plan_id, plan_name FROM asu_test_plans WHERE status IN ('PLANNED', 'IN_PROGRESS')")
            plans = cur.fetchall()
            
            cur.execute("SELECT employee_id, first_name, last_name FROM asu_employees WHERE status = 'ACTIVE' AND department = 'TESTING'")
            employees = cur.fetchall()
        
        if entity == "bugs":
            cur.execute("SELECT testcase_id, testcase_name FROM asu_test_cases WHERE status = 'ACTIVE'")
            testcases = cur.fetchall()
            
            cur.execute("SELECT employee_id, first_name, last_name FROM asu_employees WHERE status = 'ACTIVE'")
            employees = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return render_template(
            f"seminar1/add_{entity}.html",
            employees=employees,
            clients=clients,
            projects=projects,
            plans=plans,
            testcases=testcases
        )
        
    except Exception as e:
        return render_template(f"seminar1/add_{entity}.html", error=str(e))

@app.route("/seminar1/task3_advanced/get_plans")
def get_plans():
    """Получение планов тестирования для проекта"""
    project_id = request.args.get('project_id')
    
    if not project_id:
        return jsonify({'plans': []})
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT plan_id, plan_name 
            FROM asu_test_plans 
            WHERE project_id = :1 AND status IN ('PLANNED', 'IN_PROGRESS')
            ORDER BY release_date DESC
        """, [project_id])
        
        plans = [{'id': row[0], 'name': row[1]} for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return jsonify({'plans': plans})
        
    except Exception as e:
        return jsonify({'plans': [], 'error': str(e)})

@app.route("/seminar1/task3_advanced/get_testcases")
def get_testcases():
    """Получение тест-кейсов для проекта"""
    project_id = request.args.get('project_id')
    
    if not project_id:
        return jsonify({'testcases': []})
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT testcase_id, testcase_name 
            FROM asu_test_cases 
            WHERE project_id = :1 AND status = 'ACTIVE'
            ORDER BY testcase_name
        """, [project_id])
        
        testcases = [{'id': row[0], 'name': row[1]} for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return jsonify({'testcases': testcases})
        
    except Exception as e:
        return jsonify({'testcases': [], 'error': str(e)})

@app.route("/seminar1/task3_advanced/edit/<entity>/<int:record_id>", methods=["GET", "POST"])
@login_required
def seminar1_task3_advanced_edit(entity, record_id):
    """Редактирование записи"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if request.method == "POST":
            # Обновление записи
            if entity == "clients":
                cur.execute("""
                    UPDATE asu_clients 
                    SET client_name = :1, contact_person = :2, phone = :3, email = :4, 
                        priority = :5, responsible_emp_id = :6, modified_date = SYSDATE
                    WHERE client_id = :7
                """, (
                    request.form['client_name'],
                    request.form.get('contact_person', ''),
                    request.form.get('phone', ''),
                    request.form.get('email', ''),
                    int(request.form['priority']),
                    int(request.form['responsible']) if request.form.get('responsible') else None,
                    record_id
                ))
                
            elif entity == "employees":
                cur.execute("""
                    UPDATE asu_employees 
                    SET first_name = :1, last_name = :2, position = :3, department = :4,
                        email = :5, phone = :6, status = :7, manager_id = :8
                    WHERE employee_id = :9
                """, (
                    request.form['first_name'],
                    request.form['last_name'],
                    request.form['position'],
                    request.form['department'],
                    request.form['email'],
                    request.form.get('phone', ''),
                    request.form['status'],
                    int(request.form['manager_id']) if request.form.get('manager_id') else None,
                    record_id
                ))
                
            elif entity == "projects":
                cur.execute("""
                    UPDATE asu_projects 
                    SET project_name = :1, client_id = :2, description = :3,
                        status = :4, priority = :5, project_manager_id = :6
                    WHERE project_id = :7
                """, (
                    request.form['project_name'],
                    int(request.form['client_id']) if request.form.get('client_id') else None,
                    request.form.get('description', ''),
                    request.form['status'],
                    int(request.form['priority']),
                    int(request.form['manager_id']) if request.form.get('manager_id') else None,
                    record_id
                ))
                
            elif entity == "testcases":
                cur.execute("""
                    UPDATE asu_test_cases 
                    SET testcase_name = :1, project_id = :2, plan_id = :3,
                        description = :4, steps = :5, expected_result = :6,
                        priority = :7, status = :8, modified_date = SYSDATE
                    WHERE testcase_id = :9
                """, (
                    request.form['testcase_name'],
                    int(request.form['project_id']) if request.form.get('project_id') else None,
                    int(request.form['plan_id']) if request.form.get('plan_id') else None,
                    request.form.get('description', ''),
                    request.form.get('steps', ''),
                    request.form.get('expected_result', ''),
                    int(request.form['priority']),
                    request.form['status'],
                    record_id
                ))
                
            elif entity == "bugs":
                cur.execute("""
                    UPDATE asu_defects 
                    SET defect_title = :1, project_id = :2, testcase_id = :3,
                        description = :4, steps_to_reproduce = :5, severity = :6,
                        priority = :7, status = :8, assigned_to = :9,
                        resolved_date = CASE WHEN :8 IN ('FIXED', 'VERIFIED', 'CLOSED') THEN SYSDATE ELSE resolved_date END
                    WHERE defect_id = :10
                """, (
                    request.form['defect_title'],
                    int(request.form['project_id']) if request.form.get('project_id') else None,
                    int(request.form['testcase_id']) if request.form.get('testcase_id') else None,
                    request.form.get('description', ''),
                    request.form.get('steps_to_reproduce', ''),
                    request.form['severity'],
                    int(request.form['priority']),
                    request.form['status'],
                    int(request.form['assigned_to']) if request.form.get('assigned_to') else None,
                    record_id
                ))
            
            conn.commit()
            cur.close()
            conn.close()
            
            return redirect(url_for('seminar1_task3_advanced'))
        
        # GET запрос - получаем данные для формы
        record = None
        employees = []
        clients = []
        projects = []
        plans = []
        testcases = []
        
        if entity == "clients":
            cur.execute("""
                SELECT client_id, client_name, contact_person, phone, email, priority, responsible_emp_id
                FROM asu_clients WHERE client_id = :1
            """, [record_id])
            record = cur.fetchone()
            
            cur.execute("SELECT employee_id, first_name, last_name FROM asu_employees WHERE status = 'ACTIVE'")
            employees = cur.fetchall()
            
        elif entity == "employees":
            cur.execute("""
                SELECT employee_id, first_name, last_name, position, department, email, phone, status, manager_id
                FROM asu_employees WHERE employee_id = :1
            """, [record_id])
            record = cur.fetchone()
            
            cur.execute("""
                SELECT employee_id, first_name, last_name 
                FROM asu_employees 
                WHERE status = 'ACTIVE' AND employee_id != :1
            """, [record_id])
            employees = cur.fetchall()
            
        elif entity == "projects":
            cur.execute("""
                SELECT project_id, project_name, client_id, description, status, priority, project_manager_id
                FROM asu_projects WHERE project_id = :1
            """, [record_id])
            record = cur.fetchone()
            
            cur.execute("SELECT client_id, client_name FROM asu_clients WHERE status = 'ACTIVE'")
            clients = cur.fetchall()
            
            cur.execute("SELECT employee_id, first_name, last_name FROM asu_employees WHERE status = 'ACTIVE'")
            employees = cur.fetchall()
            
        elif entity == "testcases":
            cur.execute("""
                SELECT testcase_id, testcase_name, project_id, plan_id, description, steps, expected_result, priority, status, author_id
                FROM asu_test_cases WHERE testcase_id = :1
            """, [record_id])
            record = cur.fetchone()
            
            cur.execute("SELECT project_id, project_name FROM asu_projects WHERE status = 'ACTIVE'")
            projects = cur.fetchall()
            
            cur.execute("SELECT plan_id, plan_name FROM asu_test_plans WHERE status IN ('PLANNED', 'IN_PROGRESS')")
            plans = cur.fetchall()
            
            cur.execute("SELECT employee_id, first_name, last_name FROM asu_employees WHERE status = 'ACTIVE'")
            employees = cur.fetchall()
            
        elif entity == "bugs":
            cur.execute("""
                SELECT defect_id, defect_title, project_id, testcase_id, description, steps_to_reproduce, 
                       severity, priority, status, assigned_to, reported_by
                FROM asu_defects WHERE defect_id = :1
            """, [record_id])
            record = cur.fetchone()
            
            cur.execute("SELECT project_id, project_name FROM asu_projects WHERE status = 'ACTIVE'")
            projects = cur.fetchall()
            
            cur.execute("SELECT testcase_id, testcase_name FROM asu_test_cases WHERE status = 'ACTIVE'")
            testcases = cur.fetchall()
            
            cur.execute("SELECT employee_id, first_name, last_name FROM asu_employees WHERE status = 'ACTIVE'")
            employees = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return render_template(
            f"seminar1/edit_{entity}.html",
            record=record,
            employees=employees,
            clients=clients,
            projects=projects,
            plans=plans,
            testcases=testcases
        )
        
    except Exception as e:
        return render_template(f"seminar1/edit_{entity}.html", error=str(e))

@app.route("/seminar1/task3_advanced/view/<entity>/<int:record_id>")
def seminar1_task3_advanced_view(entity, record_id):
    """Просмотр детальной информации о записи"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if entity == "clients":
            cur.execute("""
                SELECT c.client_id, c.client_name, c.contact_person, c.phone, c.email, 
                       c.status, c.priority, TO_CHAR(c.created_date, 'DD.MM.YYYY') as created,
                       e.last_name || ' ' || e.first_name as responsible,
                       (SELECT COUNT(*) FROM asu_projects p WHERE p.client_id = c.client_id) as projects_count,
                       (SELECT COUNT(*) FROM asu_projects p WHERE p.client_id = c.client_id AND p.status = 'ACTIVE') as active_projects
                FROM asu_clients c
                LEFT JOIN asu_employees e ON c.responsible_emp_id = e.employee_id
                WHERE c.client_id = :1
            """, [record_id])
            record = cur.fetchone()
            
            # Получаем проекты клиента
            cur.execute("""
                SELECT project_id, project_name, status, priority, 
                       TO_CHAR(start_date, 'DD.MM.YYYY') as start_date
                FROM asu_projects
                WHERE client_id = :1
                ORDER BY start_date DESC
            """, [record_id])
            projects = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return render_template("seminar1/view_client.html", record=record, projects=projects)
            
        elif entity == "employees":
            cur.execute("""
                SELECT e.employee_id, e.first_name, e.last_name, e.position, e.department,
                       e.email, e.phone, e.status, TO_CHAR(e.hire_date, 'DD.MM.YYYY') as hire_date,
                       m.last_name || ' ' || m.first_name as manager,
                       (SELECT COUNT(*) FROM asu_projects WHERE project_manager_id = e.employee_id) as projects_managed,
                       (SELECT COUNT(*) FROM asu_defects WHERE assigned_to = e.employee_id AND status IN ('OPEN', 'IN_PROGRESS')) as assigned_defects
                FROM asu_employees e
                LEFT JOIN asu_employees m ON e.manager_id = m.employee_id
                WHERE e.employee_id = :1
            """, [record_id])
            record = cur.fetchone()
            
            cur.close()
            conn.close()
            
            return render_template("seminar1/view_employee.html", record=record)
            
        elif entity == "projects":
            cur.execute("""
                SELECT p.project_id, p.project_name, c.client_name, p.description,
                       p.status, p.priority, TO_CHAR(p.start_date, 'DD.MM.YYYY') as start_date,
                       TO_CHAR(p.end_date, 'DD.MM.YYYY') as end_date,
                       e.last_name || ' ' || e.first_name as manager,
                       (SELECT COUNT(*) FROM asu_test_plans tp WHERE tp.project_id = p.project_id) as plans_count,
                       (SELECT COUNT(*) FROM asu_test_cases tc WHERE tc.project_id = p.project_id AND tc.status = 'ACTIVE') as testcases_count,
                       (SELECT COUNT(*) FROM asu_defects d WHERE d.project_id = p.project_id) as defects_total,
                       (SELECT COUNT(*) FROM asu_defects d WHERE d.project_id = p.project_id AND d.status IN ('OPEN', 'IN_PROGRESS')) as open_defects
                FROM asu_projects p
                LEFT JOIN asu_clients c ON p.client_id = c.client_id
                LEFT JOIN asu_employees e ON p.project_manager_id = e.employee_id
                WHERE p.project_id = :1
            """, [record_id])
            record = cur.fetchone()
            
            # Получаем планы тестирования
            cur.execute("""
                SELECT plan_id, plan_name, version, status, 
                       TO_CHAR(release_date, 'DD.MM.YYYY') as release_date
                FROM asu_test_plans
                WHERE project_id = :1
                ORDER BY release_date DESC
            """, [record_id])
            plans = cur.fetchall()
            
            # Получаем тест-кейсы
            cur.execute("""
                SELECT testcase_id, testcase_name, priority, status,
                       (SELECT COUNT(*) FROM asu_defects d WHERE d.testcase_id = tc.testcase_id) as defects
                FROM asu_test_cases tc
                WHERE project_id = :1
                ORDER BY testcase_name
            """, [record_id])
            testcases = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return render_template("seminar1/view_project.html", record=record, plans=plans, testcases=testcases)
            
        elif entity == "testcases":
            cur.execute("""
                SELECT tc.testcase_id, tc.testcase_name, p.project_name, tp.plan_name,
                       tc.description, tc.steps, tc.expected_result,
                       tc.priority, tc.status, e.last_name || ' ' || e.first_name as author,
                       TO_CHAR(tc.created_date, 'DD.MM.YYYY') as created,
                       TO_CHAR(tc.modified_date, 'DD.MM.YYYY') as modified
                FROM asu_test_cases tc
                LEFT JOIN asu_projects p ON tc.project_id = p.project_id
                LEFT JOIN asu_test_plans tp ON tc.plan_id = tp.plan_id
                LEFT JOIN asu_employees e ON tc.author_id = e.employee_id
                WHERE tc.testcase_id = :1
            """, [record_id])
            record = cur.fetchone()
            
            # Получаем связанные дефекты
            cur.execute("""
                SELECT defect_id, defect_title, severity, priority, status,
                       TO_CHAR(created_date, 'DD.MM.YYYY') as created
                FROM asu_defects
                WHERE testcase_id = :1
                ORDER BY created_date DESC
            """, [record_id])
            defects = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return render_template("seminar1/view_testcase.html", record=record, defects=defects)
            
        elif entity == "bugs":
            cur.execute("""
                SELECT d.defect_id, d.defect_title, p.project_name, tc.testcase_name,
                       d.description, d.steps_to_reproduce,
                       d.severity, d.priority, d.status,
                       assigned.last_name || ' ' || assigned.first_name as assigned_to,
                       reported.last_name || ' ' || reported.first_name as reported_by,
                       TO_CHAR(d.created_date, 'DD.MM.YYYY') as created,
                       TO_CHAR(d.resolved_date, 'DD.MM.YYYY') as resolved,
                       TO_CHAR(d.closed_date, 'DD.MM.YYYY') as closed
                FROM asu_defects d
                LEFT JOIN asu_projects p ON d.project_id = p.project_id
                LEFT JOIN asu_test_cases tc ON d.testcase_id = tc.testcase_id
                LEFT JOIN asu_employees assigned ON d.assigned_to = assigned.employee_id
                LEFT JOIN asu_employees reported ON d.reported_by = reported.employee_id
                WHERE d.defect_id = :1
            """, [record_id])
            record = cur.fetchone()
            
            cur.close()
            conn.close()
            
            return render_template("seminar1/view_bug.html", record=record)
        
        return redirect(url_for('seminar1_task3_advanced'))
        
    except Exception as e:
        return render_template("seminar1/task3_advanced.html", error=str(e))

@app.route("/seminar1/task3_advanced/delete/<entity>/<int:record_id>", methods=["POST"])
@login_required
def seminar1_task3_advanced_delete(entity, record_id):
    """Удаление записи"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if entity == "clients":
            # Проверяем, есть ли связанные проекты
            cur.execute("SELECT COUNT(*) FROM asu_projects WHERE client_id = :1", [record_id])
            count = cur.fetchone()[0]
            if count > 0:
                return jsonify({'success': False, 'error': 'Нельзя удалить клиента с проектами'})
            
            cur.execute("DELETE FROM asu_clients WHERE client_id = :1", [record_id])
            
        elif entity == "employees":
            # Проверяем, есть ли связанные записи
            cur.execute("SELECT COUNT(*) FROM asu_projects WHERE project_manager_id = :1", [record_id])
            count = cur.fetchone()[0]
            if count > 0:
                return jsonify({'success': False, 'error': 'Нельзя удалить сотрудника с проектами'})
            
            cur.execute("SELECT COUNT(*) FROM asu_employees WHERE manager_id = :1", [record_id])
            count = cur.fetchone()[0]
            if count > 0:
                return jsonify({'success': False, 'error': 'Нельзя удалить руководителя с подчиненными'})
            
            cur.execute("DELETE FROM asu_employees WHERE employee_id = :1", [record_id])
            
        elif entity == "projects":
            # Проверяем, есть ли связанные тест-планы
            cur.execute("SELECT COUNT(*) FROM asu_test_plans WHERE project_id = :1", [record_id])
            count = cur.fetchone()[0]
            if count > 0:
                return jsonify({'success': False, 'error': 'Нельзя удалить проект с планами тестирования'})
            
            cur.execute("SELECT COUNT(*) FROM asu_test_cases WHERE project_id = :1", [record_id])
            count = cur.fetchone()[0]
            if count > 0:
                return jsonify({'success': False, 'error': 'Нельзя удалить проект с тест-кейсами'})
            
            cur.execute("SELECT COUNT(*) FROM asu_defects WHERE project_id = :1", [record_id])
            count = cur.fetchone()[0]
            if count > 0:
                return jsonify({'success': False, 'error': 'Нельзя удалить проект с дефектами'})
            
            cur.execute("DELETE FROM asu_projects WHERE project_id = :1", [record_id])
            
        elif entity == "testcases":
            # Проверяем, есть ли связанные дефекты
            cur.execute("SELECT COUNT(*) FROM asu_defects WHERE testcase_id = :1", [record_id])
            count = cur.fetchone()[0]
            if count > 0:
                return jsonify({'success': False, 'error': 'Нельзя удалить тест-кейс с дефектами'})
            
            cur.execute("DELETE FROM asu_test_cases WHERE testcase_id = :1", [record_id])
            
        elif entity == "bugs":
            cur.execute("DELETE FROM asu_defects WHERE defect_id = :1", [record_id])
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})




@app.route("/seminar2")
def seminar2_index():
    """Главная страница семинара 2"""
    return render_template("seminar2/index.html")

@app.route("/seminar2/report")
def seminar2_report():
    """Отчет о конфигурации БД Oracle XE"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Информация о БД
        cur.execute("SELECT name, value FROM v$parameter WHERE name IN ('db_name', 'compatible')")
        db_params = {row[0]: row[1] for row in cur.fetchall()}
        
        cur.execute("SELECT SYS_CONTEXT('USERENV', 'SERVER_HOST') FROM dual")
        host = cur.fetchone()[0]
        
        cur.execute("SELECT banner FROM v$version WHERE rownum=1")
        version = cur.fetchone()[0]
        
        db_info = {
            'name': db_params.get('db_name', 'XE'),
            'version': version,
            'host': host
        }
        
        # Common Options
        cur.execute("SELECT COUNT(*) FROM dba_users WHERE username='HR'")
        hr_exists = cur.fetchone()[0] > 0
        
        common_options = [
            {'name': 'Example Schemas', 'selected': 'true (HR схема присутствует)' if hr_exists else 'false'},
            {'name': 'Oracle Data Mining', 'selected': 'true'},
            {'name': 'Oracle Intermedia', 'selected': 'false'},
            {'name': 'Oracle JVM', 'selected': 'true'},
            {'name': 'Oracle Label Security', 'selected': 'false'},
            {'name': 'Oracle OLAP', 'selected': 'true'},
            {'name': 'Oracle Spatial', 'selected': 'false'},
            {'name': 'Oracle Text', 'selected': 'true'},
            {'name': 'Oracle Ultra Search', 'selected': 'false'},
            {'name': 'Oracle XML DB', 'selected': 'true'},
        ]
        
        # Initialization Parameters
        cur.execute("""
            SELECT name, value FROM v$parameter 
            WHERE name IN ('db_name', 'db_block_size', 'compatible', 'processes', 
                          'undo_tablespace', 'control_files')
            ORDER BY name
        """)
        init_params = [{'name': row[0], 'value': row[1]} for row in cur.fetchall()]
        
        # Character Sets
        cur.execute("""
            SELECT 'Database Character Set', value FROM nls_database_parameters WHERE parameter='NLS_CHARACTERSET'
            UNION ALL
            SELECT 'National Character Set', value FROM nls_database_parameters WHERE parameter='NLS_NCHAR_CHARACTERSET'
        """)
        char_sets = [{'name': row[0], 'value': row[1]} for row in cur.fetchall()]
        
        # Control Files
        cur.execute("SELECT name FROM v$controlfile")
        control_files = [row[0] for row in cur.fetchall()]
        
        # Tablespaces
        cur.execute("SELECT tablespace_name, status, contents FROM dba_tablespaces ORDER BY tablespace_name")
        tablespaces = [{'name': row[0], 'status': row[1], 'type': row[2]} for row in cur.fetchall()]
        
        # Data Files
        cur.execute("""
            SELECT tablespace_name, file_name, ROUND(bytes/1024/1024) 
            FROM dba_data_files 
            ORDER BY tablespace_name
        """)
        data_files = [{'tablespace': row[0], 'file': row[1], 'size': row[2]} for row in cur.fetchall()]
        
        # Redo Logs
        cur.execute("SELECT group#, ROUND(bytes/1024), status FROM v$log ORDER BY group#")
        redo_logs = [{'group': row[0], 'size': row[1], 'status': row[2]} for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return render_template(
            "seminar2/report.html",
            db_info=db_info,
            common_options=common_options,
            init_params=init_params,
            char_sets=char_sets,
            control_files=control_files,
            tablespaces=tablespaces,
            data_files=data_files,
            redo_logs=redo_logs,
            student_name="Иванов И.И."
        )
        
    except Exception as e:
        return f"Ошибка получения данных: {str(e)}"

@app.route("/seminar2/users")
@login_required
def seminar2_users():
    """Страница с примерами управления пользователями"""
    return render_template("seminar2/users.html")


@app.route('/hr_verify')
def hr_verify():
    """
    Страница пошаговой верификации схемы HR с полным выводом результатов запросов
    """
    results = {
        'hr_user_status': 'Не проверено',
        'tables_count': 0,
        'employees_count': 0,
        'departments_count': 0,
        'regions_count': 0,
        'countries_count': 0,
        'locations_count': 0,
        'jobs_count': 0,
        'job_history_count': 0,
        'orphan_records': 0,
        'emp_dates': None,
        'indexes_count': 0,
        'indexes_list': [],
        'triggers_count': 0,
        'triggers_list': [],
        'dependencies_count': 0,
        'quotas_info': 'Нет данных',
        'privileges_count': 0,
        'fk_count': 0,
        'pk_indexes': 0,
        'error_message': None,
        
        # Добавляем поля для полного вывода
        'step1_result': [],
        'step1_roles_result': [],
        'step1_privs_result': [],
        'step2_objects_result': [],
        'step2_tables_result': [],
        'step3_desc_result': [],
        'step3_constraints_result': [],
        'step3_fk_result': [],
        'step4_counts_result': [],
        'step4_stats_result': [],
        'step5_indexes_result': [],
        'step5_index_cols_result': [],
        'step6_triggers_result': [],
        'step7_dependencies_result': [],
        'step8_orphans_result': [],
        'step9_quotas_result': [],
        'step9_roles_privs_result': []
    }
    
    connection = None
    try:
        # Подключаемся через SYSTEM
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        cursor = connection.cursor()
        
        # ===== ШАГ 1: Статус пользователя и схема =====
        cursor.execute("""
            SELECT USERNAME, ACCOUNT_STATUS, EXPIRY_DATE, DEFAULT_TABLESPACE, TEMPORARY_TABLESPACE
            FROM DBA_USERS 
            WHERE USERNAME = 'HR'
        """)
        rows = cursor.fetchall()
        for row in rows:
            results['step1_result'].append({
                'USERNAME': row[0],
                'ACCOUNT_STATUS': row[1],
                'EXPIRY_DATE': row[2] if row[2] else 'NULL',
                'DEFAULT_TABLESPACE': row[3],
                'TEMPORARY_TABLESPACE': row[4]
            })
        
        # Роли HR
        cursor.execute("SELECT GRANTED_ROLE FROM DBA_ROLE_PRIVS WHERE GRANTEE = 'HR'")
        rows = cursor.fetchall()
        for row in rows:
            results['step1_roles_result'].append({'GRANTED_ROLE': row[0]})
        
        # Привилегии HR
        cursor.execute("SELECT PRIVILEGE FROM DBA_SYS_PRIVS WHERE GRANTEE = 'HR'")
        rows = cursor.fetchall()
        for row in rows:
            results['step1_privs_result'].append({'PRIVILEGE': row[0]})
        
        # ===== ШАГ 2: Проверка объектов схемы =====
        cursor.execute("""
            SELECT OBJECT_TYPE, COUNT(*)
            FROM DBA_OBJECTS
            WHERE OWNER = 'HR'
            GROUP BY OBJECT_TYPE
            ORDER BY OBJECT_TYPE
        """)
        rows = cursor.fetchall()
        for row in rows:
            results['step2_objects_result'].append({
                'OBJECT_TYPE': row[0],
                'COUNT': row[1]
            })
        
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM DBA_TABLES 
            WHERE OWNER = 'HR'
            ORDER BY TABLE_NAME
        """)
        rows = cursor.fetchall()
        results['step2_tables_result'] = [row[0] for row in rows]
        results['tables_count'] = len(rows)
        
        # ===== ШАГ 5: Проверка индексов =====
        cursor.execute("""
            SELECT INDEX_NAME, TABLE_NAME, UNIQUENESS, STATUS
            FROM DBA_INDEXES
            WHERE OWNER = 'HR'
            ORDER BY TABLE_NAME, INDEX_NAME
        """)
        rows = cursor.fetchall()
        results['indexes_count'] = len(rows)
        for row in rows:
            results['step5_indexes_result'].append({
                'INDEX_NAME': row[0],
                'TABLE_NAME': row[1],
                'UNIQUENESS': row[2],
                'STATUS': row[3]
            })
        
        cursor.execute("""
            SELECT INDEX_NAME, COLUMN_NAME, COLUMN_POSITION
            FROM DBA_IND_COLUMNS
            WHERE INDEX_OWNER = 'HR'
            ORDER BY INDEX_NAME, COLUMN_POSITION
        """)
        rows = cursor.fetchall()
        for row in rows:
            results['step5_index_cols_result'].append({
                'INDEX_NAME': row[0],
                'COLUMN_NAME': row[1],
                'COLUMN_POSITION': row[2]
            })
        
        # ===== ШАГ 6: Проверка триггеров =====
        cursor.execute("""
            SELECT TRIGGER_NAME, TABLE_NAME, STATUS, TRIGGER_TYPE, TRIGGERING_EVENT
            FROM DBA_TRIGGERS
            WHERE OWNER = 'HR'
        """)
        rows = cursor.fetchall()
        results['triggers_count'] = len(rows)
        for row in rows:
            results['step6_triggers_result'].append({
                'TRIGGER_NAME': row[0],
                'TABLE_NAME': row[1],
                'STATUS': row[2],
                'TRIGGER_TYPE': row[3],
                'TRIGGERING_EVENT': row[4]
            })
        
        # ===== ШАГ 7: Проверка зависимостей =====
        cursor.execute("""
            SELECT * FROM DBA_DEPENDENCIES
            WHERE REFERENCED_OWNER = 'HR' AND ROWNUM <= 20
        """)
        rows = cursor.fetchall()
        results['dependencies_count'] = len(rows)
        if rows and len(rows[0]) >= 4:
            for row in rows:
                results['step7_dependencies_result'].append({
                    'OWNER': row[0] if len(row) > 0 else '',
                    'NAME': row[1] if len(row) > 1 else '',
                    'TYPE': row[2] if len(row) > 2 else '',
                    'REFERENCED_NAME': row[3] if len(row) > 3 else ''
                })
        
        # ===== ШАГ 9: Квоты и привилегии =====
        cursor.execute("SELECT TABLESPACE_NAME, MAX_BYTES FROM DBA_TS_QUOTAS WHERE USERNAME = 'HR'")
        rows = cursor.fetchall()
        for row in rows:
            results['step9_quotas_result'].append({
                'TABLESPACE_NAME': row[0],
                'MAX_BYTES': row[1]
            })
        
        # Пробуем подключиться к HR для проверки данных
        hr_password = os.environ.get("HR_PASSWORD", "hr")
        try:
            conn_hr = oracledb.connect(user='HR', password=hr_password, dsn=DB_DSN)
            cursor_hr = conn_hr.cursor()
            
            # ===== ШАГ 3: Структура таблиц =====
            cursor_hr.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, NULLABLE, DATA_DEFAULT
                FROM USER_TAB_COLUMNS 
                WHERE TABLE_NAME = 'EMPLOYEES'
                ORDER BY COLUMN_ID
            """)
            rows = cursor_hr.fetchall()
            for row in rows:
                results['step3_desc_result'].append({
                    'COLUMN_NAME': row[0],
                    'DATA_TYPE': row[1],
                    'NULLABLE': row[2],
                    'DATA_DEFAULT': row[3] if row[3] else ''
                })
            
            # Все ограничения
            cursor_hr.execute("""
                SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE, TABLE_NAME, SEARCH_CONDITION, STATUS
                FROM USER_CONSTRAINTS
                ORDER BY TABLE_NAME, CONSTRAINT_TYPE
            """)
            rows = cursor_hr.fetchall()
            for row in rows:
                results['step3_constraints_result'].append({
                    'CONSTRAINT_NAME': row[0],
                    'TYPE': row[1],
                    'TABLE_NAME': row[2],
                    'SEARCH_CONDITION': str(row[3])[:50] + '...' if row[3] and len(str(row[3])) > 50 else row[3],
                    'STATUS': row[4]
                })
            
            # Foreign Keys
            cursor_hr.execute("""
                SELECT 
                    a.table_name AS child_table,
                    a.constraint_name AS fk_name,
                    c_pk.table_name AS parent_table
                FROM user_constraints a
                JOIN user_constraints c_pk ON a.r_constraint_name = c_pk.constraint_name
                WHERE a.constraint_type = 'R'
            """)
            rows = cursor_hr.fetchall()
            results['fk_count'] = len(rows)
            for row in rows:
                results['step3_fk_result'].append({
                    'CHILD_TABLE': row[0],
                    'FK_NAME': row[1],
                    'PARENT_TABLE': row[2]
                })
            
            # ===== ШАГ 4: Проверка наполнения данными =====
            cursor_hr.execute("""
                SELECT 
                    'REGIONS' AS TABLE_NAME, COUNT(*) AS ROWS_COUNT FROM REGIONS UNION ALL
                    SELECT 'COUNTRIES', COUNT(*) FROM COUNTRIES UNION ALL
                    SELECT 'LOCATIONS', COUNT(*) FROM LOCATIONS UNION ALL
                    SELECT 'DEPARTMENTS', COUNT(*) FROM DEPARTMENTS UNION ALL
                    SELECT 'JOBS', COUNT(*) FROM JOBS UNION ALL
                    SELECT 'EMPLOYEES', COUNT(*) FROM EMPLOYEES UNION ALL
                    SELECT 'JOB_HISTORY', COUNT(*) FROM JOB_HISTORY
            """)
            rows = cursor_hr.fetchall()
            counts = {}
            for row in rows:
                counts[row[0]] = row[1]
                results['step4_counts_result'].append({
                    'TABLE_NAME': row[0],
                    'ROWS_COUNT': row[1]
                })
            
            results['employees_count'] = counts.get('EMPLOYEES', 0)
            results['departments_count'] = counts.get('DEPARTMENTS', 0)
            results['regions_count'] = counts.get('REGIONS', 0)
            results['countries_count'] = counts.get('COUNTRIES', 0)
            results['locations_count'] = counts.get('LOCATIONS', 0)
            results['jobs_count'] = counts.get('JOBS', 0)
            results['job_history_count'] = counts.get('JOB_HISTORY', 0)
            
            # Статистика по сотрудникам
            cursor_hr.execute("""
                SELECT 
                    MIN(HIRE_DATE) AS FIRST_EMPLOYEE, 
                    MAX(HIRE_DATE) AS LAST_EMPLOYEE,
                    MIN(SALARY) AS MIN_SALARY,
                    MAX(SALARY) AS MAX_SALARY,
                    ROUND(AVG(SALARY), 2) AS AVG_SALARY,
                    COUNT(DISTINCT DEPARTMENT_ID) AS DEPTS_WITH_EMPLOYEES
                FROM EMPLOYEES
            """)
            row = cursor_hr.fetchone()
            if row:
                results['emp_dates'] = (row[0], row[1])
                results['step4_stats_result'] = {
                    'FIRST_HIRE': row[0],
                    'LAST_HIRE': row[1],
                    'MIN_SALARY': row[2],
                    'MAX_SALARY': row[3],
                    'AVG_SALARY': row[4],
                    'DEPTS_WITH_EMPLOYEES': row[5]
                }
            
            # ===== ШАГ 8: Проверка целостности данных =====
            cursor_hr.execute("""
                SELECT COUNT(*) AS ORPHAN_EMPLOYEES
                FROM EMPLOYEES e
                WHERE e.DEPARTMENT_ID IS NOT NULL 
                  AND NOT EXISTS (SELECT 1 FROM DEPARTMENTS d WHERE d.DEPARTMENT_ID = e.DEPARTMENT_ID)
            """)
            results['orphan_records'] = cursor_hr.fetchone()[0]
            
            results['step8_orphans_result'] = [{'ORPHAN_COUNT': results['orphan_records']}]
            
            conn_hr.close()
            
        except oracledb.Error as e:
            results['employees_count'] = f"Ошибка HR: {str(e)}"
            results['step3_desc_result'] = [{'ERROR': str(e)}]
            
        cursor.close()
        
    except oracledb.Error as e:
        results['error_message'] = str(e)
    finally:
        if connection:
            connection.close()
    
    return render_template('hr_verify.html', results=results)


# =====================================================================
# СЕМИНАР 6 - Подсистема ввода/вывода
# =====================================================================

@app.route("/seminar6")
def seminar6_index():
    """Главная страница семинара 6"""
    return render_template("seminar6/index.html")

@app.route("/seminar6/task1_1", methods=["GET", "POST"])
@login_required
def seminar6_task1_1():
    """Семинар 6, задание 1.1 - Ввод данных SQL скриптами"""
    results = None
    error = None
    sql_script = ""
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "example":
            sql_script = """-- Заполнение справочника клиентов
                            INSERT INTO asu_clients (client_id, client_name, contact_person, phone, email, priority)
                            VALUES (seq_client_id.NEXTVAL, 'ООО "Ромашка"', 'Иванов Иван', '+7(495)111-22-33', 'ivanov@romashka.ru', 1);

                            INSERT INTO asu_clients (client_id, client_name, contact_person, phone, email, priority)
                            VALUES (seq_client_id.NEXTVAL, 'АО "ТехноСервис"', 'Петров Петр', '+7(495)222-33-44', 'petrov@ts.ru', 2);

                            SELECT * FROM asu_clients;"""
            
        elif action == "execute":
            sql_script = request.form.get("sql_script", "").strip()
            
            if sql_script:
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    
                    statements = [s.strip() for s in sql_script.split(';') if s.strip()]
                    
                    last_result = None
                    for stmt in statements:
                        cur.execute(stmt)
                        if stmt.strip().upper().startswith('SELECT'):
                            rows = cur.fetchall()
                            if rows:
                                columns = [desc[0] for desc in cur.description]
                                data = []
                                for row in rows:
                                    row_dict = {}
                                    for i, col in enumerate(columns):
                                        row_dict[col] = row[i]
                                    data.append(row_dict)
                                last_result = {
                                    'columns': columns,
                                    'data': data,
                                    'rowcount': len(data)
                                }
                        else:
                            conn.commit()
                            last_result = {
                                'rowcount': cur.rowcount
                            }
                    
                    results = last_result
                    conn.commit()
                    cur.close()
                    conn.close()
                    
                except Exception as e:
                    error = str(e)
                    if conn:
                        conn.rollback()
    
    return render_template("seminar6/task1_1.html", 
                         results=results, 
                         error=error,
                         sql_script=sql_script)

@app.route("/seminar6/task1_2", methods=["GET"])
def seminar6_task1_2():
    """Главная страница задания 1.2"""
    view = request.args.get('view', 'clients')
    view_data = None
    view_columns = []
    view_title = ""
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if view == 'clients':
            cur.execute("SELECT client_id, client_name, contact_person, phone, email, priority FROM asu_clients ORDER BY client_id")
            rows = cur.fetchall()
            view_columns = ['ID', 'Название', 'Контактное лицо', 'Телефон', 'Email', 'Приоритет']
            view_data = []
            for row in rows:
                view_data.append({
                    'ID': row[0],
                    'Название': row[1],
                    'Контактное лицо': row[2] or '',
                    'Телефон': row[3] or '',
                    'Email': row[4] or '',
                    'Приоритет': row[5]
                })
            view_title = "Список клиентов"
            
        elif view == 'employees':
            cur.execute("SELECT employee_id, first_name, last_name, position, department, email, phone, salary FROM asu_employees ORDER BY employee_id")
            rows = cur.fetchall()
            view_columns = ['ID', 'Имя', 'Фамилия', 'Должность', 'Отдел', 'Email', 'Телефон', 'Оклад']
            view_data = []
            for row in rows:
                view_data.append({
                    'ID': row[0],
                    'Имя': row[1],
                    'Фамилия': row[2],
                    'Должность': row[3] or '',
                    'Отдел': row[4] or '',
                    'Email': row[5] or '',
                    'Телефон': row[6] or '',
                    'Оклад': row[7] or ''
                })
            view_title = "Список сотрудников"
            
        elif view == 'projects':
            cur.execute("""
                SELECT p.project_id, p.project_name, c.client_name, p.status, p.priority 
                FROM asu_projects p 
                LEFT JOIN asu_clients c ON p.client_id = c.client_id 
                ORDER BY p.project_id
            """)
            rows = cur.fetchall()
            view_columns = ['ID', 'Проект', 'Клиент', 'Статус', 'Приоритет']
            view_data = []
            for row in rows:
                view_data.append({
                    'ID': row[0],
                    'Проект': row[1],
                    'Клиент': row[2] or '',
                    'Статус': row[3] or '',
                    'Приоритет': row[4]
                })
            view_title = "Список проектов"
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
    
    return render_template("seminar6/task1_2.html", 
                         view_data=view_data, 
                         view_columns=view_columns,
                         view_title=view_title)

@app.route("/seminar6/task1_2/add_client", methods=["POST"])
def seminar6_add_client():
    """Добавление нового клиента"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO asu_clients (client_id, client_name, contact_person, phone, email, priority)
            VALUES (seq_client_id.NEXTVAL, :1, :2, :3, :4, :5)
        """, (
            request.form['client_name'],
            request.form.get('contact_person', ''),
            request.form.get('phone', ''),
            request.form.get('email', ''),
            int(request.form['priority'])
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return render_template("seminar6/task1_2.html", 
                             success_message="Клиент успешно добавлен!")
        
    except Exception as e:
        return render_template("seminar6/task1_2.html", 
                             error_message=str(e))

@app.route("/seminar6/task1_2/add_employee", methods=["POST"])
def seminar6_add_employee():
    """Добавление нового сотрудника"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO asu_employees (employee_id, first_name, last_name, position, department, email, phone, salary)
            VALUES (seq_employee_id.NEXTVAL, :1, :2, :3, :4, :5, :6, :7)
        """, (
            request.form['first_name'],
            request.form['last_name'],
            request.form.get('position', ''),
            request.form['department'],
            request.form.get('email', ''),
            request.form.get('phone', ''),
            int(request.form['salary']) if request.form.get('salary') else None
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return render_template("seminar6/task1_2.html", 
                             success_message="Сотрудник успешно добавлен!")
        
    except Exception as e:
        return render_template("seminar6/task1_2.html", 
                             error_message=str(e))

@app.route("/seminar6/task1_3", methods=["GET"])
def seminar6_task1_3():
    return redirect(url_for('seminar1_task3_login'))

@app.route("/seminar6/task1_4", methods=["GET"])
def seminar6_task1_4():
    """Страница загрузки данных из файла"""
    success = request.args.get('success', '')
    error = request.args.get('error', '')
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Получаем статистику
        cur.execute("SELECT COUNT(*) FROM asu_clients")
        clients_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM asu_employees")
        employees_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM asu_projects")
        projects_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM asu_test_cases")
        testcases_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM asu_defects")
        defects_count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        stats = {
            'clients': clients_count,
            'employees': employees_count,
            'projects': projects_count,
            'testcases': testcases_count,
            'defects': defects_count
        }
        
    except Exception as e:
        stats = {'clients': 0, 'employees': 0, 'projects': 0, 'testcases': 0, 'defects': 0}
    
    return render_template("seminar6/task1_4.html", 
                         stats=stats, 
                         success=success,
                         error=error)

@app.route("/seminar6/task1_4/upload", methods=["POST"])
def seminar6_upload_file():
    """Обработка загруженного файла"""
    if 'data_file' not in request.files:
        return redirect(url_for('seminar6_task1_4', error="Файл не выбран"))
    
    file = request.files['data_file']
    
    if file.filename == '':
        return redirect(url_for('seminar6_task1_4', error="Файл не выбран"))
    
    if not (file.filename.endswith('.csv') or file.filename.endswith('.txt')):
        return redirect(url_for('seminar6_task1_4', error="Неверный формат файла. Используйте .csv или .txt"))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Читаем CSV файл
        csv_file = TextIOWrapper(file, encoding='utf-8')
        reader = csv.DictReader(csv_file)
        
        # Определяем тип данных по заголовкам
        headers = reader.fieldnames
        
        if headers and 'client_name' in headers:
            # Импорт клиентов
            count = 0
            for row in reader:
                cur.execute("""
                    INSERT INTO asu_clients (client_id, client_name, contact_person, phone, email, priority)
                    VALUES (seq_client_id.NEXTVAL, :1, :2, :3, :4, :5)
                """, (
                    row['client_name'],
                    row.get('contact_person', ''),
                    row.get('phone', ''),
                    row.get('email', ''),
                    int(row.get('priority', 3))
                ))
                count += 1
            conn.commit()
            success = f"✅ Успешно импортировано {count} клиентов"
            
        elif headers and 'first_name' in headers and 'last_name' in headers:
            # Импорт сотрудников
            count = 0
            for row in reader:
                cur.execute("""
                    INSERT INTO asu_employees (employee_id, first_name, last_name, position, department, email, phone, salary)
                    VALUES (seq_employee_id.NEXTVAL, :1, :2, :3, :4, :5, :6, :7)
                """, (
                    row['first_name'],
                    row['last_name'],
                    row.get('position', ''),
                    row.get('department', 'TESTING'),
                    row.get('email', ''),
                    row.get('phone', ''),
                    int(row.get('salary', 0)) if row.get('salary') else None
                ))
                count += 1
            conn.commit()
            success = f"✅ Успешно импортировано {count} сотрудников"
            
        else:
            cur.close()
            conn.close()
            return redirect(url_for('seminar6_task1_4', 
                                   error="Не удалось определить тип данных. Проверьте заголовки CSV файла"))
        
        cur.close()
        conn.close()
        
        # Перенаправляем на страницу с сообщением об успехе
        return redirect(url_for('seminar6_task1_4', success=success))
        
    except Exception as e:
        return redirect(url_for('seminar6_task1_4', 
                               error=f"Ошибка при импорте: {str(e)}"))

@app.route("/seminar6/task1_5", methods=["GET"])
def seminar6_task1_5():
    """Страница эмуляции сканера штрих-кодов"""
    return render_template("seminar6/task1_5.html")

@app.route("/seminar6/task2_1", methods=["GET", "POST"])
def seminar6_task2_1():
    """Задание 2.1 - Иерархический отчет"""
    results = None
    error = None
    
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT 
                    LPAD(' ', 2 * (LEVEL - 1), '.') || LAST_NAME AS employee,
                    SYS_CONNECT_BY_PATH(LAST_NAME, '/') AS hierarchy
                FROM HR.EMPLOYEES
                START WITH LAST_NAME = 'Kochhar'
                CONNECT BY PRIOR EMPLOYEE_ID = MANAGER_ID
                ORDER SIBLINGS BY LAST_NAME
            """)
            
            rows = cur.fetchall()
            results = [{'employee': r[0], 'hierarchy': r[1]} for r in rows]
            
            cur.close()
            conn.close()
            
        except Exception as e:
            error = str(e)
    
    return render_template("seminar6/task2_1.html", results=results, error=error)

@app.route("/seminar6/task2_2", methods=["GET", "POST"])
def seminar6_task2_2():
    """Задание 2.2 - Отчет Больше среднего"""
    results = None
    error = None
    
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            query = """
                SELECT 
                    e1.LAST_NAME AS employee,
                    e1.SALARY,
                    e2.LAST_NAME AS colleague,
                    e2.SALARY AS colleague_salary,
                    e1.DEPARTMENT_ID,
                    ROUND(AVG(e1.SALARY) OVER(PARTITION BY e1.DEPARTMENT_ID), 2) AS avg_salary
                FROM HR.EMPLOYEES e1
                JOIN HR.EMPLOYEES e2 ON e1.DEPARTMENT_ID = e2.DEPARTMENT_ID
                WHERE e1.DEPARTMENT_ID IN (60, 80)
                    AND e1.SALARY > (SELECT AVG(SALARY) FROM HR.EMPLOYEES WHERE DEPARTMENT_ID = e1.DEPARTMENT_ID)
                    AND e2.SALARY > e1.SALARY
                ORDER BY e1.DEPARTMENT_ID, e1.SALARY DESC, e1.LAST_NAME, e2.SALARY DESC
            """
            
            cur.execute(query)
            rows = cur.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    'employee': row[0],
                    'salary': row[1],
                    'colleague': row[2],
                    'colleague_salary': row[3],
                    'department': row[4],
                    'avg_salary': row[5]
                })
            
            cur.close()
            conn.close()
            
        except Exception as e:
            error = str(e)
    
    return render_template("seminar6/task2_2.html", results=results, error=error)

@app.route("/seminar6/task2_3", methods=["GET", "POST"])
def seminar6_task2_3():
    """Задание 2.3 - Размножение строк"""
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Создаем таблицу и заполняем данными
            cur.execute("BEGIN EXECUTE IMMEDIATE 'DROP TABLE EMP_SELECTED'; EXCEPTION WHEN OTHERS THEN NULL; END;")
            
            cur.execute("""
                CREATE TABLE EMP_SELECTED (
                    First_name VARCHAR2(20) NOT NULL,
                    Last_name VARCHAR2(20) NOT NULL,
                    N INTEGER NOT NULL
                )
            """)
            
            cur.execute("INSERT INTO EMP_SELECTED VALUES('Ellen', 'ABEL', 3)")
            cur.execute("INSERT INTO EMP_SELECTED VALUES('Matthew', 'WEISS', 5)")
            conn.commit()
            
            # Запрос из методички
            query = """
                SELECT 
                    ROW_NUMBER() OVER(ORDER BY Last_name, First_name) AS "Сквозной №",
                    ROW_NUMBER() OVER(PARTITION BY Last_name, First_name ORDER BY Last_name, First_name) AS "№ в группе",
                    First_name AS "Имя",
                    Last_name AS "Фамилия"
                FROM EMP_SELECTED,
                    (SELECT LEVEL Lev FROM DUAL 
                     CONNECT BY LEVEL <= (SELECT MAX(N) FROM EMP_SELECTED))
                WHERE Lev <= N
                ORDER BY Last_name, First_name
            """
            
            cur.execute(query)
            rows = cur.fetchall()
            
            results = [{
                'num': r[0],
                'group_num': r[1],
                'first': r[2],
                'last': r[3]
            } for r in rows]
            
            cur.close()
            conn.close()
            
            return render_template("seminar6/task2_3.html", 
                                 results=results,
                                 sql=query)
            
        except Exception as e:
            return render_template("seminar6/task2_3.html", error=str(e))
    
    return render_template("seminar6/task2_3.html")

@app.route("/seminar6/task2_4", methods=["GET", "POST"])
def seminar6_task2_4():
    """Задание 2.4 - Выборка зарплат и экспорт в разные форматы"""
    if request.method == "POST":
        format_type = request.form.get('format')
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # SQL запрос из задания
            query = """
                SELECT Salary, Hire_Date FROM (
                    SELECT Salary, MAX(Hire_Date) as Hire_Date 
                    FROM (
                        SELECT Hire_Date, Salary 
                        FROM (
                            SELECT Hire_Date, Salary 
                            FROM HR.EMPLOYEES 
                            ORDER BY Hire_Date DESC, Salary DESC
                        ) 
                        WHERE ROWNUM <= 50
                    )
                    GROUP BY Salary 
                    ORDER BY 2 DESC
                )
                WHERE ROWNUM < 20
            """
            
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            
            # Формируем данные для ответа
            if format_type == 'csv':
                # CSV формат
                output = StringIO()
                writer = csv.writer(output, delimiter=';')
                writer.writerow(['Salary', 'Hire_Date'])
                for row in rows:
                    writer.writerow([row[0], row[1].strftime('%Y-%m-%d') if row[1] else ''])
                
                return Response(
                    output.getvalue(),
                    mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=salaries.csv'}
                )
                
            elif format_type == 'excel':
                # XLS (CSV с другим расширением)
                output = StringIO()
                output.write('Salary\tHire_Date\n')
                for row in rows:
                    output.write(f"{row[0]}\t{row[1].strftime('%Y-%m-%d') if row[1] else ''}\n")
                
                return Response(
                    output.getvalue(),
                    mimetype='application/vnd.ms-excel',
                    headers={'Content-Disposition': 'attachment; filename=salaries.xls'}
                )
                
            else:
                # HTML отображение
                results = [{'salary': r[0], 'hire_date': r[1].strftime('%Y-%m-%d') if r[1] else ''} for r in rows]
                return render_template("seminar6/task2_4.html", results=results, sql=query)
                
        except Exception as e:
            return render_template("seminar6/task2_4.html", error=str(e))
    
    return render_template("seminar6/task2_4.html")

@app.route("/seminar6/task2_4a", methods=["GET", "POST"])
def seminar6_task2_4a():
    """Задание 2.4а - Вывод с штрихкодами"""
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # SQL запрос из задания 2.4
            query = """
                SELECT Salary, Hire_Date FROM (
                    SELECT Salary, MAX(Hire_Date) as Hire_Date 
                    FROM (
                        SELECT Hire_Date, Salary 
                        FROM (
                            SELECT Hire_Date, Salary 
                            FROM HR.EMPLOYEES 
                            ORDER BY Hire_Date DESC, Salary DESC
                        ) 
                        WHERE ROWNUM <= 50
                    )
                    GROUP BY Salary 
                    ORDER BY 2 DESC
                )
                WHERE ROWNUM < 20
            """
            
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            
            results = [{
                'salary': r[0],
                'hire_date': r[1].strftime('%Y-%m-%d') if r[1] else ''
            } for r in rows]
            
            return render_template("seminar6/task2_4a.html", 
                                 results=results, 
                                 sql=query)
            
        except Exception as e:
            return render_template("seminar6/task2_4a.html", error=str(e))
    
    return render_template("seminar6/task2_4a.html")

@app.route("/seminar6/task2_5", methods=["GET", "POST"])
def seminar6_task2_5():
    """Задание 2.5 - Обмен значениями первичных ключей"""
    data = None
    message = None
    error = None
    
    if request.method == "POST":
        action = request.form.get('action')
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            if action == "create":
                # Создаем тестовую таблицу T2
                cur.execute("BEGIN EXECUTE IMMEDIATE 'DROP TABLE T2'; EXCEPTION WHEN OTHERS THEN NULL; END;")
                
                cur.execute("""
                    CREATE TABLE T2 (
                        N INTEGER PRIMARY KEY
                    )
                """)
                
                # Заполняем данными 190-200 для наглядности
                for i in range(190, 201):
                    if i not in [194, 195]:  # Пропускаем 194 и 195, добавим отдельно
                        cur.execute("INSERT INTO T2 VALUES (:1)", [i])
                
                # Добавляем 194 и 195 с задержкой для наглядности
                cur.execute("INSERT INTO T2 VALUES (194)")
                cur.execute("INSERT INTO T2 VALUES (195)")
                conn.commit()
                
                message = "✅ Таблица T2 создана и заполнена данными (190-200)"
                
            elif action == "show":
                # Показываем данные
                cur.execute("SELECT ROWID, N FROM T2 WHERE N BETWEEN 190 AND 200 ORDER BY N")
                rows = cur.fetchall()
                
                data = [{'rowid': str(r[0]), 'n': r[1]} for r in rows]
                
            elif action == "swap":
                # Выполняем обмен значениями 194 и 195
                cur.execute("""
                    UPDATE T2 
                    SET N = DECODE(N, 194, 195, 195, 194) 
                    WHERE N IN (194, 195)
                """)
                conn.commit()
                
                # Показываем обновленные данные
                cur.execute("SELECT ROWID, N FROM T2 WHERE N BETWEEN 190 AND 200 ORDER BY N")
                rows = cur.fetchall()
                
                data = [{'rowid': str(r[0]), 'n': r[1]} for r in rows]
                message = "✅ Обмен выполнен: 194 и 195 поменялись местами"
            
            cur.close()
            conn.close()
            
        except Exception as e:
            error = str(e)
    
    return render_template("seminar6/task2_5.html", data=data, message=message, error=error)

@app.route("/seminar6/task2_6", methods=["GET", "POST"])
def seminar6_task2_6():
    """Задание 2.6 - Номер дня недели"""
    result = None
    error = None
    
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Получаем текущую дату
            cur.execute("SELECT TO_CHAR(SYSDATE, 'DD.MM.YYYY') FROM DUAL")
            current_date = cur.fetchone()[0]
            
            # Получаем название дня на английском
            cur.execute("SELECT TO_CHAR(SYSDATE, 'DY', 'NLS_DATE_LANGUAGE = AMERICAN') FROM DUAL")
            day_name = cur.fetchone()[0]
            
            # Вычисляем номер дня (пн=1)
            cur.execute("""
                SELECT (INSTR('MONTUEWEDTHUFRISATSUN', 
                             TO_CHAR(SYSDATE, 'DY', 'NLS_DATE_LANGUAGE = AMERICAN')) + 2) / 3 
                FROM DUAL
            """)
            day_number = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            
            result = {
                'current_date': current_date,
                'day_name': day_name,
                'day_number': int(day_number)
            }
            
        except Exception as e:
            error = str(e)
    
    return render_template("seminar6/task2_6.html", result=result, error=error)

@app.route("/seminar6/task2_7", methods=["GET", "POST"])
def seminar6_task2_7():
    """Задание 2.7 - Отчет с ROLLUP"""
    results = None
    error = None
    
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            query = """
                SELECT 
                    CASE 
                        WHEN GROUPING(e.MANAGER_ID) = 1 AND GROUPING(e.JOB_ID) = 1 THEN NULL
                        WHEN GROUPING(e.JOB_ID) = 1 THEN e.MANAGER_ID
                        ELSE e.MANAGER_ID
                    END AS manager_id,
                    CASE 
                        WHEN GROUPING(e.JOB_ID) = 1 THEN NULL
                        ELSE e.JOB_ID
                    END AS job_id,
                    COUNT(*) AS emp_count,
                    ROUND(SUM(e.SALARY + NVL(e.COMMISSION_PCT, 0) * e.SALARY), 2) AS total_payment,
                    CASE 
                        WHEN GROUPING(e.MANAGER_ID) = 1 AND GROUPING(e.JOB_ID) = 1 THEN 'GRAND TOTAL'
                        WHEN GROUPING(e.JOB_ID) = 1 THEN 'MANAGER TOTAL'
                        ELSE 'DETAIL'
                    END AS row_type
                FROM HR.EMPLOYEES e
                WHERE e.MANAGER_ID IS NOT NULL
                GROUP BY ROLLUP (e.MANAGER_ID, e.JOB_ID)
                ORDER BY 
                    CASE WHEN e.MANAGER_ID IS NULL THEN 999999 ELSE e.MANAGER_ID END,
                    CASE WHEN e.JOB_ID IS NULL THEN 999999 ELSE 1 END
            """
            
            cur.execute(query)
            rows = cur.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    'manager_id': row[0],
                    'job_id': row[1],
                    'emp_count': row[2],
                    'total_payment': row[3],
                    'type': row[4]
                })
            
            cur.close()
            conn.close()
            
        except Exception as e:
            error = str(e)
    
    return render_template("seminar6/task2_7.html", results=results, error=error)

@app.route("/seminar6/task2_8", methods=["GET", "POST"])
def seminar6_task2_8():
    """Задание 2.8 - Отчет по руководителям с итогами"""
    results = None
    error = None
    
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            query = """
                WITH manager_payments AS (
                    SELECT 
                        m.EMPLOYEE_ID AS manager_id,
                        m.FIRST_NAME || ' ' || m.LAST_NAME AS manager_name,
                        m.JOB_ID AS manager_job,
                        e.EMPLOYEE_ID AS emp_id,
                        e.JOB_ID AS emp_job,
                        e.SALARY + NVL(e.COMMISSION_PCT, 0) * e.SALARY AS payment
                    FROM HR.EMPLOYEES e
                    JOIN HR.EMPLOYEES m ON e.MANAGER_ID = m.EMPLOYEE_ID
                    WHERE e.MANAGER_ID IS NOT NULL
                ),
                job_titles AS (
                    SELECT JOB_ID, JOB_TITLE FROM HR.JOBS
                )
                SELECT 
                    CASE 
                        WHEN GROUPING(mp.manager_id) = 1 THEN '...О Б Щ И Й'
                        WHEN GROUPING(mp.emp_job) = 1 THEN '...' || mp.manager_name || ' итоги:'
                        ELSE mp.manager_name
                    END AS manager_name,
                    CASE 
                        WHEN GROUPING(mp.manager_id) = 1 THEN ''
                        WHEN GROUPING(mp.emp_job) = 1 THEN (SELECT JOB_TITLE FROM job_titles WHERE JOB_ID = mp.manager_job)
                        ELSE (SELECT JOB_TITLE FROM job_titles WHERE JOB_ID = mp.emp_job)
                    END AS job_title,
                    COUNT(mp.emp_id) AS emp_count,
                    ROUND(SUM(mp.payment), 2) AS total_payment,
                    CASE 
                        WHEN GROUPING(mp.manager_id) = 1 THEN 'GRAND TOTAL'
                        WHEN GROUPING(mp.emp_job) = 1 THEN 'MANAGER TOTAL'
                        ELSE 'DETAIL'
                    END AS row_type
                FROM manager_payments mp
                GROUP BY ROLLUP (mp.manager_id, mp.manager_name, mp.manager_job, mp.emp_job)
                HAVING GROUPING(mp.manager_id) = 1 
                    OR GROUPING(mp.emp_job) = 1 
                    OR (GROUPING(mp.manager_id) = 0 AND GROUPING(mp.emp_job) = 0)
                ORDER BY 
                    CASE WHEN mp.manager_id IS NULL THEN 999999 ELSE mp.manager_id END,
                    CASE WHEN mp.emp_job IS NULL THEN 999999 ELSE 1 END
            """
            
            cur.execute(query)
            rows = cur.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    'manager_name': row[0],
                    'job_title': row[1],
                    'emp_count': row[2],
                    'total_payment': row[3],
                    'type': row[4]
                })
            
            cur.close()
            conn.close()
            
        except Exception as e:
            error = str(e)
    
    return render_template("seminar6/task2_8.html", results=results, error=error)






























if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
#    execute_sql_script("create_asu_tables.sql")