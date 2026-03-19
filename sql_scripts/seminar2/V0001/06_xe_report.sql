--======================================================================
-- Наименование подсистемы: Семинар 2 - Отчет о БД
-- Наименование модуля: Информация о БД Oracle XE
-- Версия: 1.0
-- Дата последнего обновления: 2026-03-07
-- Разработчик: Student
-- Краткое назначение: Получение информации о БД для отчета
--======================================================================

SPOOL /tmp/06_xe_report.lst

SET LINESIZE 150
SET PAGESIZE 100
SET FEEDBACK OFF
SET HEADING ON
SET VERIFY OFF

PROMPT ======================================================================
PROMPT         ИНФОРМАЦИЯ О БАЗЕ ДАННЫХ ORACLE XE
PROMPT ======================================================================
PROMPT 

PROMPT 1. Common Options (Опции БД)
PROMPT -------------------------------------------------------------
SELECT 'Example Schemas' AS "Option Name", 
       DECODE((SELECT COUNT(*) FROM dba_users WHERE username = 'HR'), 0, 'false', 'true') AS "Selected"
FROM dual
UNION ALL
SELECT 'Oracle Data Mining', 'true' FROM dual
UNION ALL
SELECT 'Oracle Intermedia', 'false' FROM dual
UNION ALL
SELECT 'Oracle JVM', 'true' FROM dual
UNION ALL
SELECT 'Oracle Label Security', 'false' FROM dual
UNION ALL
SELECT 'Oracle OLAP', 'true' FROM dual
UNION ALL
SELECT 'Oracle Spatial', 'false' FROM dual
UNION ALL
SELECT 'Oracle Text', 'true' FROM dual
UNION ALL
SELECT 'Oracle Ultra Search', 'false' FROM dual
UNION ALL
SELECT 'Oracle XML DB', 'true' FROM dual;

PROMPT 
PROMPT 2. Initialization Parameters (Параметры инициализации)
PROMPT -------------------------------------------------------------
SELECT name, value
FROM v$parameter
WHERE name IN ('db_name', 'db_block_size', 'db_cache_size', 'shared_pool_size',
               'processes', 'sessions', 'compatible', 'control_files',
               'undo_tablespace', 'db_domain', 'open_cursors')
ORDER BY name;

PROMPT 
PROMPT 3. Character Sets (Кодировки)
PROMPT -------------------------------------------------------------
SELECT 'Database Character Set' AS "Name", value AS "Value"
FROM nls_database_parameters
WHERE parameter = 'NLS_CHARACTERSET'
UNION ALL
SELECT 'National Character Set', value
FROM nls_database_parameters
WHERE parameter = 'NLS_NCHAR_CHARACTERSET';

PROMPT 
PROMPT 4. Control Files (Файлы управления)
PROMPT -------------------------------------------------------------
SELECT name AS "Control File" FROM v$controlfile;

PROMPT 
PROMPT 5. Tablespaces (Табличные пространства)
PROMPT -------------------------------------------------------------
SELECT tablespace_name AS "Name", 
       status AS "Status",
       contents AS "Type"
FROM dba_tablespaces
ORDER BY tablespace_name;

PROMPT 
PROMPT 6. Data Files (Файлы данных)
PROMPT -------------------------------------------------------------
SELECT tablespace_name AS "Tablespace",
       ROUND(bytes/1024/1024) AS "Size(MB)",
       autoextensible AS "Auto"
FROM dba_data_files
ORDER BY tablespace_name;

PROMPT 
PROMPT 7. Redo Log Groups (Группы логов)
PROMPT -------------------------------------------------------------
SELECT group# AS "Group", 
       ROUND(bytes/1024) AS "Size(KB)",
       status AS "Status"
FROM v$log
ORDER BY group#;

PROMPT ======================================================================
PROMPT                     ОТЧЕТ ЗАВЕРШЕН
PROMPT ======================================================================

SPOOL OFF
EXIT;
