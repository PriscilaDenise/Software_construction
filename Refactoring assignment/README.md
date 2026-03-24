# Banking System Refactoring Project

## 1. Project Overview

This project is a command-line based banking system developed in Python. The system allows users to log in and perform basic banking operations such as deposits, withdrawals, balance inquiries, and viewing account summaries. It also maintains transaction history for each user and persists data using a JSON file.

---

## 2. Initial System Description

### 2.1 Functionality of the Original System

The original implementation was a **single-file Python application** that provided the following features:

* User authentication (login with username and password)
* Deposit money into an account
* Withdraw money from an account
* View account balance
* View bank summary
* View transaction history
* Change password

The system stored user data in a JSON file (`bank_data.json`) to ensure persistence across sessions.

---

### 2.2 Initial Code Structure

The entire system was implemented in **one Python file**, with all functionalities combined. This included:

* Data loading and saving logic
* Authentication logic
* Transaction handling
* User interface (menu system)
* Utility functions

#### Limitations of the Initial Structure

* Lack of modularity (everything in one file)
* Difficult to maintain and extend
* No structured logging (used print statements)
* Weak or inconsistent error handling
* Tight coupling between components
* Reduced readability and scalability

---

## 3. Refactoring Objectives

The refactoring process aimed to:

* Improve code **readability and maintainability**
* Introduce **proper error handling**
* Implement **structured logging**
* Apply **modular design principles**
* Separate concerns across different components

---

## 4. Refactored System Structure

The system was reorganized into multiple modules as shown below:

```text
banking_system/
│
├── main.py              # Application entry point
├── config.py            # Configuration constants
├── logger_config.py     # Logging setup
├── exceptions.py        # Custom exception classes
├── storage.py           # Data loading and saving
├── auth.py              # Authentication logic
├── transactions.py      # Deposit, withdrawal, balance, password
├── reports.py           # Summary and transaction history
├── bank_data.json       # Persistent data file
├── banking.log          # Log file
```

---

## 5. Refactoring Techniques Applied

### 5.1 Separation of Concerns

#### What was done:

The system was divided into independent modules, each handling a specific responsibility.

#### Why:

* Improves maintainability
* Makes code easier to understand and test
* Enables scalability

#### Where:

* `auth.py` → authentication logic
* `transactions.py` → financial operations
* `storage.py` → data persistence
* `reports.py` → reporting functions

---

### 5.2 Modularization 

#### What was done:

Large blocks of logic were extracted into separate modules.

#### Why:

* Reduces complexity in the main file
* Promotes reusability
* Improves organization

#### Where:

* Functions from the original single file were moved into:

  * `auth.py`
  * `transactions.py`
  * `reports.py`
  * `storage.py`

---

### 5.3 Centralized Logging

#### What was done:

Replaced `print()` statements used for debugging with Python’s `logging` module.

#### Why:

* Provides better debugging and traceability
* Allows different logging levels (INFO, WARNING, ERROR, CRITICAL)
* Stores logs in a file for auditing

#### Where:

* `logger_config.py` → centralized logging configuration
* Logging added in:

  * login attempts (`auth.py`)
  * deposits and withdrawals (`transactions.py`)
  * data loading/saving (`storage.py`)
  * system startup and shutdown (`main.py`)

---

### 5.4 Custom Exception Handling

#### What was done:

Defined custom exception classes to handle different types of errors.

#### Why:

* Improves clarity of errors
* Enables better control over failure handling
* Avoids generic and unclear exceptions

#### Where:

* `exceptions.py` defines:

  * `AuthenticationError`
  * `InsufficientFundsError`
  * `InvalidAmountError`
  * `DataStorageError`

---

### 5.5 Improved Error Handling

#### What was done:

Introduced structured `try-except` blocks with meaningful error messages.

#### Why:

* Prevents application crashes
* Improves user experience
* Ensures graceful failure handling

#### Where:

* Login validation (`auth.py`)
* Deposit and withdrawal validation (`transactions.py`)
* File operations (`storage.py`)
* Application startup (`main.py`)

---

### 5.6 Input Validation

#### What was done:

Validated user inputs before processing transactions.

#### Why:

* Prevents invalid operations
* Enhances system reliability

#### Where:

* Amount validation in deposits and withdrawals (`transactions.py`)

---

### 5.7 Configuration Management

#### What was done:

Moved constants into a dedicated configuration file.

#### Why:

* Improves flexibility
* Centralizes system settings

#### Where:

* `config.py` contains:

  * data file path
  * log file path
  * date format

---

## 6. How to Run the System

### Step 1: Navigate to project directory

```bash
cd banking_system
```

### Step 2: Run the application

```bash
python main.py
```

---

## 7. System Output Files

* `bank_data.json` → stores client data and transactions
* `banking.log` → records system activity and errors

---

## 8. Benefits of Refactoring

The refactored system provides:

* Improved **code readability**
* Better **error handling and reliability**
* Structured **logging for debugging and auditing**
* Enhanced **modularity and scalability**
* Easier **maintenance and future extension**

---

## 9. Conclusion

The refactoring transformed the system from a monolithic, single-file implementation into a well-structured, modular application. By applying best practices such as separation of concerns, logging, and custom error handling, the system is now more robust, maintainable, and suitable for real-world software development standards.

---
