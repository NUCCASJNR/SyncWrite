-- sql script


CREATE DATABASE IF NOT EXISTS SyncWrite_db;
       CREATE USER IF NOT EXISTS 'Sync_user'@'localhost' IDENTIFIED BY 'Sync_pwd123@';
              GRANT ALL PRIVILEGES ON SyncWrite_db.* TO 'Sync_user'@'localhost';
                                      GRANT SELECT ON performance_schema.* TO 'Sync_user'@'localhost';
FLUSH PRIVILEGES;