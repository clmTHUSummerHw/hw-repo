CREATE USER IF NOT EXISTS flask IDENTIFIED BY '123456';
CREATE DATABASE IF NOT EXISTS flask;
GRANT ALL ON flask.* TO 'flask'@'%' IDENTIFIED BY '123456';
SELECT concat('DROP TABLE IF EXISTS ', table_name, ';') FROM information_schema.tables WHERE table_schema = 'flask';