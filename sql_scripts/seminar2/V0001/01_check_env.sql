--======================================================================
-- Наименование подсистемы: Семинар 2 - Создание БД
-- Наименование модуля: Проверка окружения
-- Версия: 1.0
-- Дата последнего обновления: 2026-03-07
-- Разработчик: Student
-- Краткое назначение: Проверка параметров окружения перед созданием БД
--======================================================================

SPOOL 01_check_env.lst

PROMPT ======================================================================
PROMPT Проверка окружения для создания базы данных
PROMPT ======================================================================

-- Информация о текущем подключении
SELECT 
    USER AS current_user,
    SYS_CONTEXT('USERENV', 'DB_NAME') AS db_name,
    SYS_CONTEXT('USERENV', 'INSTANCE_NAME') AS instance_name,
    SYS_CONTEXT('USERENV', 'SERVER_HOST') AS host
FROM dual;

-- Проверка прав (должен быть SYSDBA)
SELECT 
    DECODE(USERENV('ISDBA'), 'TRUE', '✅ Есть права SYSDBA', '❌ НЕТ прав SYSDBA') AS dba_status
FROM dual;

-- Информация о табличных пространствах
SELECT 
    tablespace_name,
    status,
    contents,
    extent_management,
    segment_space_management
FROM dba_tablespaces
ORDER BY tablespace_name;

-- Информация о файлах данных
SELECT 
    file_name,
    tablespace_name,
    bytes/1024/1024 AS size_mb,
    autoextensible,
    status
FROM dba_data_files
ORDER BY tablespace_name;

PROMPT ======================================================================
PROMPT Проверка завершена. Убедитесь, что у вас есть права SYSDBA.
PROMPT ======================================================================

SPOOL OFF
EXIT;
