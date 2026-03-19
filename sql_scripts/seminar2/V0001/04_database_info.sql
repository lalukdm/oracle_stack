--======================================================================
-- Наименование подсистемы: Семинар 2 - Информация о БД
-- Наименование модуля: Отчет о конфигурации
-- Версия: 1.0
-- Дата последнего обновления: 2026-03-07
-- Разработчик: Student
-- Краткое назначение: Получение информации о БД для отчета
--======================================================================

SPOOL /tmp/04_database_info.lst

PROMPT ======================================================================
PROMPT ИНФОРМАЦИЯ О БАЗЕ ДАННЫХ
PROMPT ======================================================================

PROMPT 
PROMPT 1. Common Options (Опции БД)
PROMPT -------------------------------------------------------------
SELECT 
    'Example Schemas' AS "Option Name",
    DECODE(value, 'TRUE', 'true', 'false') AS "Selected"
FROM v$parameter WHERE name = 'compatible'
UNION ALL
SELECT 'Oracle Data Mining', 'false' FROM dual
UNION ALL
SELECT 'Oracle Intermedia', 'false' FROM dual
UNION ALL
SELECT 'Oracle JVM', 'true' FROM dual
UNION ALL
SELECT 'Oracle Label Security', 'false' FROM dual
UNION ALL
SELECT 'Oracle OLAP', 'false' FROM dual
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
SELECT 
    name AS "Name",
    value AS "Value"
FROM v$parameter
WHERE name IN (
    'aq_tm_processes',
    'background_dump_dest',
    'compatible',
    'control_files',
    'core_dump_dest',
    'db_block_size',
    'db_cache_size',
    'db_domain',
    'db_file_multiblock_read_count',
    'db_name',
    'dispatchers',
    'fast_start_mttr_target',
    'hash_join_enabled',
    'instance_name',
    'java_pool_size',
    'job_queue_processes',
    'large_pool_size',
    'open_cursors',
    'pga_aggregate_target',
    'processes',
    'query_rewrite_enabled',
    'remote_login_passwordfile',
    'shared_pool_size',
    'sort_area_size',
    'star_transformation_enabled',
    'timed_statistics',
    'undo_management',
    'undo_retention',
    'undo_tablespace',
    'user_dump_dest'
)
ORDER BY name;

PROMPT 
PROMPT 3. Character Sets (Кодировки)
PROMPT -------------------------------------------------------------
SELECT 
    'Database Character Set' AS "Name",
    value AS "Value"
FROM nls_database_parameters
WHERE parameter = 'NLS_CHARACTERSET'
UNION ALL
SELECT 
    'National Character Set',
    value
FROM nls_database_parameters
WHERE parameter = 'NLS_NCHAR_CHARACTERSET';

PROMPT 
PROMPT 4. Control Files (Файлы управления)
PROMPT -------------------------------------------------------------
SELECT name AS "Control file" FROM v$controlfile;

PROMPT 
PROMPT 5. Tablespaces (Табличные пространства)
PROMPT -------------------------------------------------------------
SELECT 
    status AS "Status",
    tablespace_name AS "Name",
    contents AS "Type",
    extent_management AS "Extent management"
FROM dba_tablespaces
ORDER BY tablespace_name;

PROMPT 
PROMPT 6. Data Files (Файлы данных)
PROMPT -------------------------------------------------------------
SELECT 
    status AS "Status",
    file_name AS "Name",
    tablespace_name AS "Tablespace",
    ROUND(bytes/1024/1024) AS "Size(M)"
FROM dba_data_files
ORDER BY tablespace_name, file_name;

PROMPT 
PROMPT 7. Redo Log Groups (Группы логов)
PROMPT -------------------------------------------------------------
SELECT 
    group# AS "Group",
    bytes/1024 AS "Size(K)"
FROM v$log
ORDER BY group#;

PROMPT ======================================================================
PROMPT ОТЧЕТ ЗАВЕРШЕН
PROMPT ======================================================================

SPOOL OFF
EXIT;
