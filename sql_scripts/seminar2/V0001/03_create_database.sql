--======================================================================
-- Наименование подсистемы: Семинар 2 - Создание БД
-- Наименование модуля: Создание базы данных
-- Версия: 1.0
-- Дата последнего обновления: 2026-03-07
-- Разработчик: Student
-- Краткое назначение: Создание базы данных SEM2_DB
--======================================================================

SPOOL /tmp/03_create_database.lst

PROMPT ======================================================================
PROMPT Начало создания базы данных SEM2_DB
PROMPT ======================================================================

-- Создаем базу данных (модифицированный пример)
CREATE DATABASE sem2_db
MAXINSTANCES 1
MAXLOGHISTORY 1
MAXLOGFILES 5
MAXLOGMEMBERS 3
MAXDATAFILES 100

-- Файл данных SYSTEM
DATAFILE '/u01/app/oracle/oradata/sem2_db/system01.dbf' 
SIZE 100M REUSE 
AUTOEXTEND ON NEXT 10M 
MAXSIZE UNLIMITED
EXTENT MANAGEMENT LOCAL

-- Временное табличное пространство по умолчанию
DEFAULT TEMPORARY TABLESPACE TEMP
TEMPFILE '/u01/app/oracle/oradata/sem2_db/temp01.dbf' 
SIZE 20M REUSE 
AUTOEXTEND ON NEXT 5M 
MAXSIZE UNLIMITED 

-- Табличное пространство UNDO
UNDO TABLESPACE "UNDOTBS1" 
DATAFILE '/u01/app/oracle/oradata/sem2_db/undotbs01.dbf' 
SIZE 50M REUSE 
AUTOEXTEND ON NEXT 5M 
MAXSIZE UNLIMITED 

-- Кодировки
CHARACTER SET AL32UTF8
NATIONAL CHARACTER SET UTF8

-- Группы логов
LOGFILE 
GROUP 1 ('/u01/app/oracle/oradata/sem2_db/redo01.log') SIZE 50M,
GROUP 2 ('/u01/app/oracle/oradata/sem2_db/redo02.log') SIZE 50M,
GROUP 3 ('/u01/app/oracle/oradata/sem2_db/redo03.log') SIZE 50M;

PROMPT ======================================================================
PROMPT База данных SEM2_DB создана
PROMPT ======================================================================

SPOOL OFF
EXIT;
