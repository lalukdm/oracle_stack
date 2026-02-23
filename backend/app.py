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


@app.route("/seminar2/interface")
def seminar2_interface():
    """Шаблон интерфейса АСУ отдела тестирования ПО."""
    return render_template("seminar2/interface.html", title="АСУ отдела тестирования ПО")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
