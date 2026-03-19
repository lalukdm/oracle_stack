--======================================================================
-- Наименование подсистемы: Семинар 2 - Управление пользователями
-- Наименование модуля: Создание и управление пользователями
-- Версия: 1.0
-- Дата последнего обновления: 2026-03-07
-- Разработчик: Student
-- Краткое назначение: Примеры создания пользователей, назначения привилегий и ролей
--======================================================================

SPOOL seminar2_users.lst

PROMPT ======================================================================
PROMPT НАЧАЛО РАБОТЫ: УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ
PROMPT ======================================================================

PROMPT
PROMPT ----------------------------------------------------------------------
PROMPT 1. СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ (CREATE USER)
PROMPT ----------------------------------------------------------------------

PROMPT
PROMPT Пример 1: Создание простого пользователя
PROMPT ------------------------------------------------------------
CREATE USER asu_user1 IDENTIFIED BY asu123
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP
QUOTA 10M ON USERS
ACCOUNT UNLOCK;

PROMPT Пользователь asu_user1 создан

PROMPT
PROMPT Пример 2: Создание пользователя с ограничениями (как в методичке)
PROMPT ------------------------------------------------------------
CREATE USER asu_test IDENTIFIED BY test123
PROFILE DEFAULT
DEFAULT TABLESPACE USERS
QUOTA UNLIMITED ON USERS
QUOTA UNLIMITED ON SYSTEM
QUOTA UNLIMITED ON TEMP
ACCOUNT UNLOCK;

PROMPT Пользователь asu_test создан

PROMPT
PROMPT Пример 3: Создание административного пользователя
PROMPT ------------------------------------------------------------
CREATE USER asu_admin IDENTIFIED BY admin123
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP
QUOTA UNLIMITED ON USERS
PROFILE DEFAULT
ACCOUNT UNLOCK;

PROMPT Пользователь asu_admin создан

PROMPT
PROMPT ----------------------------------------------------------------------
PROMPT 2. НАЗНАЧЕНИЕ ПРИВИЛЕГИЙ (GRANT)
PROMPT ----------------------------------------------------------------------

PROMPT
PROMPT 2.1. Системные привилегии
PROMPT ------------------------------------------------------------
GRANT CREATE SESSION TO asu_user1;
GRANT CREATE TABLE TO asu_user1;
GRANT CREATE VIEW TO asu_user1;
GRANT CREATE SEQUENCE TO asu_user1;
GRANT CREATE PROCEDURE TO asu_user1;
GRANT CREATE TRIGGER TO asu_user1;

PROMPT Системные привилегии назначены пользователю asu_user1

PROMPT
PROMPT 2.2. Назначение ролей
PROMPT ------------------------------------------------------------
GRANT CONNECT TO asu_test;
GRANT RESOURCE TO asu_test;
GRANT DBA TO asu_admin;

PROMPT Роли назначены

PROMPT
PROMPT ----------------------------------------------------------------------
PROMPT 3. ПРОВЕРКА ПРИВИЛЕГИЙ
PROMPT ----------------------------------------------------------------------

PROMPT
PROMPT 3.1. Просмотр системных привилегий пользователей
PROMPT ------------------------------------------------------------
SELECT GRANTEE, PRIVILEGE, ADMIN_OPTION
FROM DBA_SYS_PRIVS
WHERE GRANTEE IN ('ASU_USER1', 'ASU_TEST', 'ASU_ADMIN')
ORDER BY GRANTEE, PRIVILEGE;

PROMPT
PROMPT 3.2. Просмотр ролей пользователей
PROMPT ------------------------------------------------------------
SELECT GRANTEE, GRANTED_ROLE, ADMIN_OPTION, DEFAULT_ROLE
FROM DBA_ROLE_PRIVS
WHERE GRANTEE IN ('ASU_USER1', 'ASU_TEST', 'ASU_ADMIN')
ORDER BY GRANTEE, GRANTED_ROLE;

PROMPT
PROMPT 3.3. Просмотр квот пользователей на табличные пространства
PROMPT ------------------------------------------------------------
SELECT TABLESPACE_NAME, USERNAME, BYTES/1024/1024 AS QUOTA_MB, MAX_BYTES/1024/1024 AS MAX_QUOTA_MB
FROM DBA_TS_QUOTAS
WHERE USERNAME IN ('ASU_USER1', 'ASU_TEST', 'ASU_ADMIN')
ORDER BY USERNAME, TABLESPACE_NAME;

PROMPT
PROMPT ----------------------------------------------------------------------
PROMPT 4. СОЗДАНИЕ И УПРАВЛЕНИЕ РОЛЯМИ
PROMPT ----------------------------------------------------------------------

PROMPT
PROMPT 4.1. Создание пользовательской роли
PROMPT ------------------------------------------------------------
CREATE ROLE asu_developer_role NOT IDENTIFIED;
CREATE ROLE asu_analyst_role IDENTIFIED BY analyst123;
CREATE ROLE asu_manager_role;

PROMPT Роли созданы

PROMPT
PROMPT 4.2. Назначение привилегий ролям
PROMPT ------------------------------------------------------------
-- Для разработчиков
GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO asu_developer_role;
GRANT SELECT ANY TABLE TO asu_developer_role;

-- Для аналитиков
GRANT CREATE SESSION TO asu_analyst_role;
GRANT SELECT ANY TABLE TO asu_analyst_role;

-- Для менеджеров
GRANT CREATE SESSION TO asu_manager_role;
GRANT SELECT ANY TABLE, INSERT ANY TABLE, UPDATE ANY TABLE, DELETE ANY TABLE TO asu_manager_role;

PROMPT Привилегии назначены ролям

PROMPT
PROMPT 4.3. Назначение ролей пользователям
PROMPT ------------------------------------------------------------
GRANT asu_developer_role TO asu_user1;
GRANT asu_analyst_role TO asu_test;
GRANT asu_manager_role TO asu_admin;

PROMPT Роли назначены пользователям

PROMPT
PROMPT ----------------------------------------------------------------------
PROMPT 5. ИЗМЕНЕНИЕ ПОЛЬЗОВАТЕЛЕЙ (ALTER USER)
PROMPT ----------------------------------------------------------------------

PROMPT
PROMPT 5.1. Смена пароля
PROMPT ------------------------------------------------------------
ALTER USER asu_user1 IDENTIFIED BY newpass123;
PROMPT Пароль пользователя asu_user1 изменен

PROMPT
PROMPT 5.2. Блокировка/разблокировка учетной записи
PROMPT ------------------------------------------------------------
ALTER USER asu_test ACCOUNT LOCK;
PROMPT Пользователь asu_test заблокирован

ALTER USER asu_test ACCOUNT UNLOCK;
PROMPT Пользователь asu_test разблокирован

PROMPT
PROMPT 5.3. Изменение квот
PROMPT ------------------------------------------------------------
ALTER USER asu_user1 QUOTA 20M ON USERS;
PROMPT Квота пользователя asu_user1 изменена

PROMPT
PROMPT ----------------------------------------------------------------------
PROMPT 6. ПРОВЕРКА ИЗМЕНЕНИЙ
PROMPT ----------------------------------------------------------------------

PROMPT
PROMPT 6.1. Информация о пользователях
PROMPT ------------------------------------------------------------
SELECT USERNAME, ACCOUNT_STATUS, DEFAULT_TABLESPACE, TEMPORARY_TABLESPACE, CREATED
FROM DBA_USERS
WHERE USERNAME IN ('ASU_USER1', 'ASU_TEST', 'ASU_ADMIN')
ORDER BY USERNAME;

PROMPT
PROMPT 6.2. Обновленные привилегии после назначения ролей
PROMPT ------------------------------------------------------------
SELECT GRANTEE, GRANTED_ROLE, ADMIN_OPTION, DEFAULT_ROLE
FROM DBA_ROLE_PRIVS
WHERE GRANTEE IN ('ASU_USER1', 'ASU_TEST', 'ASU_ADMIN')
ORDER BY GRANTEE, GRANTED_ROLE;

PROMPT
PROMPT ----------------------------------------------------------------------
PROMPT 7. УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ (DROP USER) - демонстрация
PROMPТ ----------------------------------------------------------------------

PROMPT
PROMPT ВНИМАНИЕ: Удаление пользователей закомментировано для безопасности
PROMPT -- DROP USER asu_user1 CASCADE;
PROMPT -- DROP USER asu_test CASCADE;
PROMPT -- DROP USER asu_admin CASCADE;
PROMPT -- DROP ROLE asu_developer_role;
PROMPT -- DROP ROLE asu_analyst_role;
PROMPT -- DROP ROLE asu_manager_role;

PROMPT
PROMPT ======================================================================
PROMPT ИТОГОВАЯ ИНФОРМАЦИЯ
PROMPT ======================================================================

SELECT 'Всего создано пользователей: 3' AS RESULT FROM DUAL;
SELECT 'Всего создано ролей: 3' AS RESULT FROM DUAL;
SELECT 'Всего назначено привилегий: см. выше' AS RESULT FROM DUAL;

PROMPT ======================================================================
PROMPT СКРИПТ ЗАВЕРШЕН
PROMPT ======================================================================

SPOOL OFF
EXIT;
