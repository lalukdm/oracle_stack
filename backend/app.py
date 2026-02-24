import os

from flask import Flask, jsonify, request, render_template
import oracledb

# --- Инициализация Oracle client (thick mode) ---
oracledb.init_oracle_client(lib_dir="/opt/oracle/instantclient")

app = Flask(__name__)

# --- Параметры подключения к БД из переменных окружения ---
DB_USER = os.environ.get("ORACLE_USER", "system")
DB_PASSWORD = os.environ.get("ORACLE_PASSWORD", "oracle")
DB_DSN = os.environ.get("ORACLE_DSN", "oracle-db:1521/XE")


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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)