--======================================================================
-- Наименование подсистемы: Семинар 2 - Отчет о БД
-- Наименование модуля: Информация о БД Oracle XE
-- Версия: 1.0
-- Дата последнего обновления: 2026-03-07
-- Разработчик: Student
-- Краткое назначение: Получение информации о БД для отчета
--======================================================================

SET LINESIZE 200
SET PAGESIZE 100
SET FEEDBACK OFF
SET ECHO OFF
SET HEADING ON
SET VERIFY OFF

SPOOL /tmp/08_xe_final.lst

PROMPT ======================================================================
PROMPT         ИНФОРМАЦИЯ О БАЗЕ ДАННЫХ ORACLE XE
PROMPT ======================================================================

PROMPT
PROMPT 1. Common Options
PROMPT ------------------------------------------------------------
SELECT 'Example Schemas' as "Option Name", 
       DECODE((SELECT COUNT(*) FROM dba_users WHERE username='HR'), 0, 'false', 'true') as "Selected" FROM dual;

SELECT 'Oracle Data Mining' as "Option Name", 'true' as "Selected" FROM dual;
SELECT 'Oracle Intermedia' as "Option Name", 'false' as "Selected" FROM dual;
SELECT 'Oracle JVM' as "Option Name", 'true' as "Selected" FROM dual;
SELECT 'Oracle Label Security' as "Option Name", 'false' as "Selected" FROM dual;
SELECT 'Oracle OLAP' as "Option Name", 'true' as "Selected" FROM dual;
SELECT 'Oracle Spatial' as "Option Name", 'false' as "Selected" FROM dual;
SELECT 'Oracle Text' as "Option Name", 'true' as "Selected" FROM dual;
SELECT 'Oracle Ultra Search' as "Option Name", 'false' as "Selected" FROM dual;
SELECT 'Oracle XML DB' as "Option Name", 'true' as "Selected" FROM dual;

PROMPT
PROMPT 2. Initialization Parameters
PROMPT ------------------------------------------------------------
SELECT 'DB_NAME' as "Parameter", value as "Value" FROM v$parameter WHERE name='db_name' UNION ALL
SELECT 'DB_BLOCK_SIZE', value FROM v$parameter WHERE name='db_block_size' UNION ALL
SELECT 'COMPATIBLE', value FROM v$parameter WHERE name='compatible' UNION ALL
SELECT 'PROCESSES', value FROM v$parameter WHERE name='processes' UNION ALL
SELECT 'UNDO_TABLESPACE', value FROM v$parameter WHERE name='undo_tablespace' UNION ALL
SELECT 'CONTROL_FILES', value FROM v$parameter WHERE name='control_files';

PROMPT
PROMPT 3. Character Sets
PROMPT ------------------------------------------------------------
SELECT 'Database Character Set' as "Name", value as "Value" FROM nls_database_parameters WHERE parameter='NLS_CHARACTERSET'
UNION ALL
SELECT 'National Character Set', value FROM nls_database_parameters WHERE parameter='NLS_NCHAR_CHARACTERSET';

PROMPT
PROMPT 4. Control Files
PROMPT ------------------------------------------------------------
SELECT name as "Control File" FROM v$controlfile;

PROMPT
PROMPT 5. Tablespaces
PROMPT ------------------------------------------------------------
SELECT tablespace_name as "Name", status, contents as "Type" FROM dba_tablespaces ORDER BY tablespace_name;

PROMPT
PROMPT 6. Data Files
PROMPT ------------------------------------------------------------
SELECT tablespace_name as "Tablespace", file_name as "File", bytes/1024/1024 as "Size MB" FROM dba_data_files ORDER BY tablespace_name;

PROMPT
PROMPT 7. Redo Log Groups
PROMPT ------------------------------------------------------------
SELECT group# as "Group", bytes/1024 as "Size KB", status FROM v$log ORDER BY group#;

PROMPT
PROMPT ======================================================================
PROMPT                     ОТЧЕТ ЗАВЕРШЕН
PROMPT ======================================================================

SPOOL OFF
EXIT;
