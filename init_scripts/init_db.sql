CREATE DATABASE IF NOT EXISTS task_scheduler;

CREATE USER IF NOT EXISTS 'test_user'@'%' IDENTIFIED BY 'test_password';

GRANT ALL PRIVILEGES ON task_scheduler.* TO 'test_user'@'%';
GRANT ALL PRIVILEGES ON test_task_scheduler.* TO 'test_user'@'%';

ALTER USER 'root'@'%' IDENTIFIED BY 'test';

FLUSH PRIVILEGES;
