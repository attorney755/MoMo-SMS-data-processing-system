-- MoMo SMS Database Setup
-- Schema, constraints, indexes, sample data, and CRUD test queries
-- Target: MySQL 8.0+

-- Safety: create schema if not exists and switch to it
CREATE DATABASE IF NOT EXISTS momo_sms
  /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE momo_sms;

-- Drop tables in dependency order for idempotency in development
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS system_logs;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS transaction_categories;
DROP TABLE IF EXISTS users_customers;
SET FOREIGN_KEY_CHECKS = 1;

-- Users/Customers
CREATE TABLE users_customers (
  user_id INT NOT NULL AUTO_INCREMENT COMMENT 'Primary key for user/customer',
  name VARCHAR(100) NOT NULL COMMENT 'Full name from SMS or KYC',
  phone_number VARCHAR(20) NOT NULL COMMENT 'MSISDN in international format, e.g. +233xxxxxxxxx',
  email VARCHAR(120) NULL COMMENT 'Email if available',
  registration_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'When the user first appeared in the system',
  account_status ENUM('active','pending','suspended','closed') NOT NULL DEFAULT 'active' COMMENT 'Operational status of the account',
  PRIMARY KEY (user_id),
  UNIQUE KEY uq_users_phone (phone_number),
  UNIQUE KEY uq_users_email (email),
  CONSTRAINT chk_users_phone CHECK (phone_number REGEXP '^[+0-9][0-9]{6,14}$'),
  CONSTRAINT chk_users_email CHECK (email IS NULL OR email LIKE '%@%')
) COMMENT='People who send or receive MoMo transactions';

-- Transaction Categories
CREATE TABLE transaction_categories (
  category_id INT NOT NULL AUTO_INCREMENT COMMENT 'Primary key for transaction category',
  category_name VARCHAR(60) NOT NULL COMMENT 'Human-friendly category like Transfer, Airtime, Bills',
  description TEXT NULL COMMENT 'Longer description of the category',
  PRIMARY KEY (category_id),
  UNIQUE KEY uq_categories_name (category_name)
) COMMENT='Reference data for classifying transactions';

-- Transactions (core facts)
CREATE TABLE `Transactions` (
  `transaction_id` VARCHAR(50),
  `amount` DECIMAL(15, 2),
  `sender_id` VARCHAR(20),
  `receiver_id` VARCHAR(20),
  `timestamp` DATETIME,
  `fee` DECIMAL(15, 2),
  `new_balance` DECIMAL(15, 2),
  `message` VARCHAR(255),
  `financial_transaction_id` VARCHAR(50),
  `external_transaction_id` VARCHAR(50),
  `service_center` VARCHAR(20),
  `transaction_type` VARCHAR(20),
  `readable_date` VARCHAR(50),
  PRIMARY KEY (`financial_transaction_id`)
);

-- System Logs (ETL/processing events)
CREATE TABLE system_logs (
  log_id BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Primary key for a system log record',
  transaction_id BIGINT NULL COMMENT 'Optional link to a transaction this log refers to',
  log_messages TEXT NOT NULL COMMENT 'Free-text log details',
  log_type ENUM('info','warning','error','debug') NOT NULL DEFAULT 'info' COMMENT 'Severity/type of log message',
  timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'When the event occurred',
  PRIMARY KEY (log_id),
  KEY idx_log_tx (transaction_id),
  KEY idx_log_time (timestamp),
  CONSTRAINT fk_log_tx
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
    ON UPDATE CASCADE ON DELETE SET NULL
) COMMENT='Operational logs for data ingestion and processing';

-- Sample Data --------------------------------------------------------------

-- Users (≥5)
INSERT INTO users_customers (name, phone_number, email, account_status)
VALUES
  ('Ama Mensah', '+233201111111', 'ama@example.com', 'active'),
  ('Kofi Boateng', '+233202222222', 'kofi@example.com', 'active'),
  ('Yaw Asare', '+233203333333', NULL, 'pending'),
  ('Abena Owusu', '+233204444444', 'abena@example.com', 'active'),
  ('Kojo Antwi', '+233205555555', 'kojo@example.com', 'active'),
  ('Esi Adjei', '+233206666666', 'esi@example.com', 'suspended');

-- Categories (≥5)
INSERT INTO transaction_categories (category_name, description)
VALUES
  ('Transfer', 'Peer-to-peer money transfer'),
  ('Airtime', 'Mobile top-up purchase'),
  ('Bills', 'Utility and bill payments'),
  ('CashOut', 'Withdrawal at agent'),
  ('Merchant', 'Payment to merchant');

-- Transactions (≥5)
-- For deterministic FKs, fetch some user and category ids
-- (Assumes AUTO_INCREMENT starts at 1 in a fresh schema.)
INSERT INTO transactions (amount, category_id, sender_id, receiver_id, time, status, reference, note)
VALUES
  (150.00, 1, 1, 2, NOW() - INTERVAL 10 DAY, 'completed', 'TX-0001', 'Rent split'),
  (20.00, 2, 1, 3, NOW() - INTERVAL 9 DAY, 'completed', 'TX-0002', 'Airtime top-up'),
  (75.50, 3, 4, 5, NOW() - INTERVAL 8 DAY, 'completed', 'TX-0003', 'Electricity bill'),
  (500.00, 4, 2, 1, NOW() - INTERVAL 7 DAY, 'failed', 'TX-0004', 'Cash-out attempt'),
  (42.75, 5, 5, 4, NOW() - INTERVAL 6 DAY, 'completed', 'TX-0005', 'Groceries'),
  (99.99, 5, 1, 6, NOW() - INTERVAL 5 DAY, 'reversed', 'TX-0006', 'Refunded purchase');

-- Logs (≥5)
INSERT INTO system_logs (transaction_id, log_messages, log_type, timestamp)
VALUES
  (1, 'Parsed SMS and created transaction record', 'info', NOW() - INTERVAL 10 DAY),
  (1, 'Webhook confirmed completion', 'info', NOW() - INTERVAL 10 DAY + INTERVAL 2 MINUTE),
  (4, 'Provider returned insufficient funds', 'warning', NOW() - INTERVAL 7 DAY),
  (6, 'Chargeback initiated by provider', 'warning', NOW() - INTERVAL 5 DAY),
  (NULL, 'Scheduled ETL started', 'debug', NOW());

-- CRUD Test Queries --------------------------------------------------------

-- Create: insert a new user
-- INSERT INTO users_customers (name, phone_number, email) VALUES ('Test User', '+233209999999', 'test@example.com');

-- Read: list last 10 completed transfers with sender/receiver names
-- SELECT t.transaction_id, t.amount, t.time, c.category_name,
--        s.name AS sender_name, r.name AS receiver_name
-- FROM transactions t
-- JOIN transaction_categories c ON c.category_id = t.category_id
-- JOIN users_customers s ON s.user_id = t.sender_id
-- JOIN users_customers r ON r.user_id = t.receiver_id
-- WHERE t.status = 'completed'
-- ORDER BY t.time DESC
-- LIMIT 10;

-- Update: change a user status
-- UPDATE users_customers SET account_status = 'suspended' WHERE user_id = 6;

-- Delete: remove a log entry (safe; logs can be deleted)
-- DELETE FROM system_logs WHERE log_id = 1;

-- Example analytics: total sent per user in the last 30 days
-- SELECT s.user_id, s.name, SUM(t.amount) AS total_sent
-- FROM transactions t
-- JOIN users_customers s ON s.user_id = t.sender_id
-- WHERE t.status = 'completed' AND t.time >= NOW() - INTERVAL 30 DAY
-- GROUP BY s.user_id, s.name
-- ORDER BY total_sent DESC;
