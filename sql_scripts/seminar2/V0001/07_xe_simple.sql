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

SPOOL /tmp/07_xe_simple.lst

PROMPT ======================================================================
PROMPt         ИНФОРМАЦИЯ О БАЗЕ ДАННЫХ ORACLE XE
PROMPT ======================================================================

PROMPT
PROMPT 1. Common Options
PROMPT ------------------------------------------------------------
SELECT 'Example Schemas' as "Option Name",
       decode((select count(*) from dba_users where username='HR'),0,'false','true') as "Selected"
FROM dual;

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
SELECT name, value FROM v$parameter WHERE name='db_name';
SELECT name, value FROM v$parameter WHERE name='db_block_size';
SELECT name, value FROM v$parameter WHERE name='compatible';
SELECT name, value FROM v$parameter WHERE name='processes';
SELECT name, value FROM v$parameter WHERE name='undo_tablespace';
SELECT name, value FROM v$parameter WHERE name='control_files';

PROMPT
PROMPT 3. Character Sets
PROMPT ------------------------------------------------------------
SELECT 'Database Character Set' as "Name", value as "Value"
FROM nls_database_parameters WHERE parameter='NLS_CHARACTERSET';
SELECT 'National Character Set' as "Name", value as "Value"
FROM nls_database_parameters WHERE parameter='NLS_NCHAR_CHARACTERSET';

PROMPT
PROMPT 4. Control Files
PROMPT ------------------------------------------------------------
SELECT name FROM v$controlfile;

PROMPT
PROMPT 5. Tablespaces
PROMPT ------------------------------------------------------------
SELECT tablespace_name as "Name", status, contents as "Type"
FROM dba_tablespaces ORDER BY tablespace_name;

PROMPT
PROMPT 6. Data Files
PROMPT ------------------------------------------------------------
SELECT tablespace_name, file_name, bytes/1024/1024 as "Size MB"
FROM dba_data_files ORDER BY tablespace_name;

PROMPT
PROMPT 7. Redo Log Groups
PROMPT ------------------------------------------------------------
SELECT group#, bytes/1024 as "Size KB", status
FROM v$log ORDER BY group#;

PROMPT
PROMPT ======================================================================
PROMPT                     ОТЧЕТ ЗАВЕРШЕН
PROMPT ======================================================================

SPOOL OFF
EXIT;
