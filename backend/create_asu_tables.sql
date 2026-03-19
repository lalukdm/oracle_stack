-- Создание таблиц для АСУ отдела тестирования ПО

-- Клиенты
CREATE TABLE asu_clients (
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
);

-- Сотрудники
CREATE TABLE asu_employees (
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
);

-- Проекты
CREATE TABLE asu_projects (
    project_id NUMBER PRIMARY KEY,
    project_name VARCHAR2(200) NOT NULL,
    client_id NUMBER REFERENCES asu_clients(client_id),
    description CLOB,
    start_date DATE,
    end_date DATE,
    status VARCHAR2(20) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'ON_HOLD', 'COMPLETED', 'CANCELLED')),
    priority NUMBER(1) DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    project_manager_id NUMBER REFERENCES asu_employees(employee_id),
    created_date DATE DEFAULT SYSDATE
);

-- Планы тестирования (релизы/итерации)
CREATE TABLE asu_test_plans (
    plan_id NUMBER PRIMARY KEY,
    project_id NUMBER REFERENCES asu_projects(project_id),
    plan_name VARCHAR2(200) NOT NULL,
    version VARCHAR2(20),
    release_date DATE,
    status VARCHAR2(20) DEFAULT 'PLANNED' CHECK (status IN ('PLANNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    description CLOB,
    created_by NUMBER REFERENCES asu_employees(employee_id),
    created_date DATE DEFAULT SYSDATE
);

-- Тест-кейсы
CREATE TABLE asu_test_cases (
    testcase_id NUMBER PRIMARY KEY,
    testcase_name VARCHAR2(500) NOT NULL,
    project_id NUMBER REFERENCES asu_projects(project_id),
    plan_id NUMBER REFERENCES asu_test_plans(plan_id),
    description CLOB,
    steps CLOB,
    expected_result CLOB,
    priority NUMBER(1) DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    status VARCHAR2(20) DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'ACTIVE', 'DEPRECATED')),
    author_id NUMBER REFERENCES asu_employees(employee_id),
    created_date DATE DEFAULT SYSDATE,
    modified_date DATE
);

-- Дефекты (Bug-трекер)
CREATE TABLE asu_defects (
    defect_id NUMBER PRIMARY KEY,
    defect_title VARCHAR2(500) NOT NULL,
    project_id NUMBER REFERENCES asu_projects(project_id),
    testcase_id NUMBER REFERENCES asu_test_cases(testcase_id),
    description CLOB,
    steps_to_reproduce CLOB,
    severity VARCHAR2(20) CHECK (severity IN ('BLOCKER', 'CRITICAL', 'MAJOR', 'MINOR', 'TRIVIAL')),
    priority NUMBER(1) DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    status VARCHAR2(20) DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'IN_PROGRESS', 'FIXED', 'VERIFIED', 'CLOSED', 'REOPENED')),
    assigned_to NUMBER REFERENCES asu_employees(employee_id),
    reported_by NUMBER REFERENCES asu_employees(employee_id),
    created_date DATE DEFAULT SYSDATE,
    resolved_date DATE,
    closed_date DATE
);

-- Отчёты
CREATE TABLE asu_reports (
    report_id NUMBER PRIMARY KEY,
    report_name VARCHAR2(200) NOT NULL,
    project_id NUMBER REFERENCES asu_projects(project_id),
    plan_id NUMBER REFERENCES asu_test_plans(plan_id),
    report_type VARCHAR2(50) CHECK (report_type IN ('PROGRESS', 'DEFECTS', 'COVERAGE', 'SUMMARY')),
    report_data CLOB,
    created_by NUMBER REFERENCES asu_employees(employee_id),
    created_date DATE DEFAULT SYSDATE,
    report_date DATE
);

-- Последовательности для ID
CREATE SEQUENCE seq_client_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_employee_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_project_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_plan_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_testcase_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_defect_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_report_id START WITH 1 INCREMENT BY 1;

-- Индексы для поиска
CREATE INDEX idx_clients_name ON asu_clients(client_name);
CREATE INDEX idx_clients_status ON asu_clients(status);
CREATE INDEX idx_employees_name ON asu_employees(last_name, first_name);
CREATE INDEX idx_employees_status ON asu_employees(status);
CREATE INDEX idx_projects_name ON asu_projects(project_name);
CREATE INDEX idx_projects_status ON asu_projects(status);
CREATE INDEX idx_testcases_name ON asu_test_cases(testcase_name);
CREATE INDEX idx_testcases_status ON asu_test_cases(status);
CREATE INDEX idx_defects_status ON asu_defects(status);
CREATE INDEX idx_defects_severity ON asu_defects(severity);


-- Заполнение тестовыми данными -------------------------------------

-- Клиенты
INSERT INTO asu_clients (client_id, client_name, contact_person, phone, email, priority, responsible_emp_id)
VALUES (seq_client_id.NEXTVAL, 'ООО "ТехноИнновации"', 'Иванов Петр', '+7(495)123-45-67', 'info@techno.ru', 1, 1);
INSERT INTO asu_clients (client_id, client_name, contact_person, phone, email, priority, responsible_emp_id)
VALUES (seq_client_id.NEXTVAL, 'АО "Банк Финанс"', 'Сидорова Анна', '+7(495)234-56-78', 'contact@bankfinance.ru', 2, 2);
INSERT INTO asu_clients (client_id, client_name, contact_person, phone, email, priority, responsible_emp_id)
VALUES (seq_client_id.NEXTVAL, 'ООО "Ритейл Плюс"', 'Петров Иван', '+7(495)345-67-89', 'info@retailplus.ru', 3, 1);
INSERT INTO asu_clients (client_id, client_name, contact_person, phone, email, status, priority, responsible_emp_id)
VALUES (seq_client_id.NEXTVAL, 'ЗАО "Старый проект"', 'Козлов Дмитрий', '+7(495)456-78-90', 'old@inactive.ru', 'INACTIVE', 5, 3);

-- Сотрудники
INSERT INTO asu_employees (employee_id, first_name, last_name, position, department, email, phone, manager_id)
VALUES (seq_employee_id.NEXTVAL, 'Алексей', 'Смирнов', 'Руководитель отдела', 'MANAGEMENT', 'a.smirnov@testlab.ru', '+7(903)111-22-33', NULL);
INSERT INTO asu_employees (employee_id, first_name, last_name, position, department, email, phone, manager_id)
VALUES (seq_employee_id.NEXTVAL, 'Елена', 'Петрова', 'Ведущий тестировщик', 'TESTING', 'e.petrova@testlab.ru', '+7(903)222-33-44', 1);
INSERT INTO asu_employees (employee_id, first_name, last_name, position, department, email, phone, manager_id)
VALUES (seq_employee_id.NEXTVAL, 'Дмитрий', 'Иванов', 'Тестировщик', 'TESTING', 'd.ivanov@testlab.ru', '+7(903)333-44-55', 2);
INSERT INTO asu_employees (employee_id, first_name, last_name, position, department, email, phone, manager_id)
VALUES (seq_employee_id.NEXTVAL, 'Ольга', 'Соколова', 'Аналитик', 'ANALYSIS', 'o.sokolova@testlab.ru', '+7(903)444-55-66', 1);
INSERT INTO asu_employees (employee_id, first_name, last_name, position, department, email, phone, status, manager_id)
VALUES (seq_employee_id.NEXTVAL, 'Иван', 'Петров', 'Тестировщик', 'TESTING', 'i.petrov@testlab.ru', '+7(903)555-66-77', 'INACTIVE', 2);

-- Проекты
INSERT INTO asu_projects (project_id, project_name, client_id, description, start_date, status, priority, project_manager_id)
VALUES (seq_project_id.NEXTVAL, 'Мобильное приложение "Банк-Клиент"', 2, 'Разработка и тестирование мобильного приложения для банка', DATE '2024-01-15', 'ACTIVE', 1, 2);
INSERT INTO asu_projects (project_id, project_name, client_id, description, start_date, status, priority, project_manager_id)
VALUES (seq_project_id.NEXTVAL, 'Интернет-магазин "Ритейл Плюс"', 3, 'Тестирование интернет-магазина', DATE '2024-02-01', 'ACTIVE', 2, 2);
INSERT INTO asu_projects (project_id, project_name, client_id, description, start_date, status, priority, project_manager_id)
VALUES (seq_project_id.NEXTVAL, 'CRM для ТехноИнновации', 1, 'Внутренняя CRM система', DATE '2023-10-10', 'ON_HOLD', 3, 1);
INSERT INTO asu_projects (project_id, project_name, client_id, description, start_date, end_date, status, priority, project_manager_id)
VALUES (seq_project_id.NEXTVAL, 'Старый проект (завершен)', 4, 'Завершенный проект', DATE '2023-01-01', DATE '2023-12-31', 'COMPLETED', 4, 3);

-- Планы тестирования
INSERT INTO asu_test_plans (plan_id, project_id, plan_name, version, release_date, status, created_by)
VALUES (seq_plan_id.NEXTVAL, 1, 'Релиз 1.0 - Мобильное приложение', '1.0', DATE '2024-03-15', 'IN_PROGRESS', 2);
INSERT INTO asu_test_plans (plan_id, project_id, plan_name, version, release_date, status, created_by)
VALUES (seq_plan_id.NEXTVAL, 1, 'Релиз 1.1 - Мобильное приложение', '1.1', DATE '2024-04-15', 'PLANNED', 2);
INSERT INTO asu_test_plans (plan_id, project_id, plan_name, version, release_date, status, created_by)
VALUES (seq_plan_id.NEXTVAL, 2, 'Релиз 1.0 - Интернет-магазин', '1.0', DATE '2024-03-01', 'COMPLETED', 3);

-- Тест-кейсы
INSERT INTO asu_test_cases (testcase_id, testcase_name, project_id, plan_id, description, steps, expected_result, priority, status, author_id)
VALUES (seq_testcase_id.NEXTVAL, 'Проверка авторизации в мобильном приложении', 1, 1, 'Тест проверяет возможность входа в приложение', 
'1. Открыть приложение\n2. Ввести логин\n3. Ввести пароль\n4. Нажать кнопку "Войти"', 
'Пользователь успешно входит в приложение', 1, 'ACTIVE', 3);
INSERT INTO asu_test_cases (testcase_id, testcase_name, project_id, plan_id, description, steps, expected_result, priority, status, author_id)
VALUES (seq_testcase_id.NEXTVAL, 'Проверка добавления товара в корзину', 2, 3, 'Тест проверяет добавление товара в корзину', 
'1. Открыть сайт\n2. Найти товар\n3. Нажать "Добавить в корзину"', 
'Товар появляется в корзине', 2, 'ACTIVE', 3);
INSERT INTO asu_test_cases (testcase_id, testcase_name, project_id, plan_id, description, steps, expected_result, priority, status, author_id)
VALUES (seq_testcase_id.NEXTVAL, 'Проверка оформления заказа', 2, 3, 'Тест проверяет оформление заказа', 
'1. Добавить товар в корзину\n2. Перейти к оформлению\n3. Заполнить данные\n4. Подтвердить заказ', 
'Заказ успешно оформлен', 1, 'ACTIVE', 2);
INSERT INTO asu_test_cases (testcase_id, testcase_name, project_id, status, priority, author_id)
VALUES (seq_testcase_id.NEXTVAL, 'Устаревший тест-кейс', 3, 'DEPRECATED', 5, 1);

-- Дефекты
INSERT INTO asu_defects (defect_id, defect_title, project_id, testcase_id, description, steps_to_reproduce, severity, priority, status, assigned_to, reported_by)
VALUES (seq_defect_id.NEXTVAL, 'Приложение вылетает при входе', 1, 1, 'Краш приложения после ввода логина и пароля', 
'1. Открыть приложение\n2. Ввести логин\n3. Ввести пароль\n4. Нажать "Войти"', 
'CRITICAL', 1, 'IN_PROGRESS', 3, 2);
INSERT INTO asu_defects (defect_id, defect_title, project_id, testcase_id, description, steps_to_reproduce, severity, priority, status, assigned_to, reported_by)
VALUES (seq_defect_id.NEXTVAL, 'Неверный расчет суммы заказа', 2, 3, 'Итоговая сумма заказа не совпадает с суммой товаров', 
'1. Добавить несколько товаров\n2. Перейти к оформлению\n3. Сравнить суммы', 
'MAJOR', 2, 'OPEN', 3, 4);
INSERT INTO asu_defects (defect_id, defect_title, project_id, description, severity, priority, status, assigned_to, reported_by)
VALUES (seq_defect_id.NEXTVAL, 'Опечатка в интерфейсе', 2, 'В кнопке "Оформить заказ" опечатка', 
'MINOR', 4, 'FIXED', 3, 4);
INSERT INTO asu_defects (defect_id, defect_title, project_id, severity, priority, status, assigned_to, reported_by)
VALUES (seq_defect_id.NEXTVAL, 'Медленная загрузка страницы', 1, 'MAJOR', 3, 'OPEN', 3, 2);
INSERT INTO asu_defects (defect_id, defect_title, project_id, severity, priority, status, assigned_to, reported_by)
VALUES (seq_defect_id.NEXTVAL, 'Некорректное отображение на iPad', 1, 'MINOR', 3, 'VERIFIED', 3, 2);

-- Представление для статистики
CREATE VIEW asu_dashboard_stats AS
SELECT 
    (SELECT COUNT(*) FROM asu_clients WHERE status = 'ACTIVE') as active_clients,
    (SELECT COUNT(*) FROM asu_projects WHERE status = 'ACTIVE') as active_projects,
    (SELECT COUNT(*) FROM asu_defects WHERE status IN ('OPEN', 'IN_PROGRESS', 'REOPENED')) as open_defects,
    (SELECT COUNT(*) FROM asu_test_cases WHERE status = 'ACTIVE') as active_testcases,
    (SELECT COUNT(*) FROM asu_test_plans WHERE status IN ('PLANNED', 'IN_PROGRESS')) as active_plans
FROM dual;

COMMIT;



-- -- Создание синонимов для таблиц
-- CREATE PUBLIC SYNONYM ASU_CLIENTS FOR SYSTEM.ASU_CLIENTS;
-- CREATE PUBLIC SYNONYM ASU_EMPLOYEES FOR SYSTEM.ASU_EMPLOYEES;
-- CREATE PUBLIC SYNONYM ASU_PROJECTS FOR SYSTEM.ASU_PROJECTS;
-- CREATE PUBLIC SYNONYM ASU_TEST_PLANS FOR SYSTEM.ASU_TEST_PLANS;
-- CREATE PUBLIC SYNONYM ASU_TEST_CASES FOR SYSTEM.ASU_TEST_CASES;
-- CREATE PUBLIC SYNONYM ASU_DEFECTS FOR SYSTEM.ASU_DEFECTS;
-- CREATE PUBLIC SYNONYM ASU_REPORTS FOR SYSTEM.ASU_REPORTS;