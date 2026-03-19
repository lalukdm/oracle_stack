import oracledb
import os

# --- Параметры подключения (скопируйте из вашего app.py) ---
DB_USER = os.environ.get("ORACLE_USER", "system")
DB_PASSWORD = os.environ.get("ORACLE_PASSWORD", "oracle")
DB_DSN = os.environ.get("ORACLE_DSN", "oracle-db:1521/XE")

def execute_sql_script(filename):
    """Выполняет SQL скрипт из файла"""
    try:
        # Читаем SQL скрипт
        with open(filename, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Разделяем на отдельные команды
        # Удаляем комментарии и разделяем по точкам с запятой
        commands = []
        current_cmd = []
        
        for line in sql_script.split('\n'):
            # Пропускаем комментарии
            if line.strip().startswith('--'):
                continue
            
            current_cmd.append(line)
            
            # Если строка заканчивается на ';', это конец команды
            if line.strip().endswith(';'):
                commands.append('\n'.join(current_cmd))
                current_cmd = []
        
        # Подключаемся к БД
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        cur = conn.cursor()
        
        print(f"Подключено к {DB_USER}@{DB_DSN}")
        
        # Выполняем каждую команду
        for i, cmd in enumerate(commands, 1):
            if cmd.strip():
                try:
                    cur.execute(cmd)
                    print(f"✓ Команда {i} выполнена успешно")
                except Exception as e:
                    print(f"✗ Ошибка в команде {i}: {e}")
                    print(f"Команда: {cmd[:100]}...")
        
        conn.commit()
        print("✅ Все изменения зафиксированы")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    execute_sql_script("create_asu_tables.sql")