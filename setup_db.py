import sqlite3

def create_db():
    conn = sqlite3.connect("insurance.db")
    cur = conn.cursor()

    # Create users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('admin', 'agent')) NOT NULL
    )
    """)

    # Create customers table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name    TEXT,
        last_name     TEXT,
        email         TEXT    UNIQUE,
        phone         TEXT,
        address       TEXT,
        date_of_birth TEXT
    )
    """)

    # Create claims table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS claims (
        claim_id         INTEGER PRIMARY KEY,
        policy_id        INTEGER REFERENCES [policy ] (policy_id),
        claim_number     TEXT    UNIQUE,
        date_of_claim    TEXT,
        type_of_claim    TEXT    CHECK (type_of_claim IN ('accident', 'theft', 'fire') )   NOT NULL,
        description      TEXT,
        status           TEXT    CHECK (status IN ('Pending', 'Approved', 'Denied') )         NOT NULL,
        resolution_notes TEXT,
        settlement_date  TEXT
    )
    """)


    # Create incidents table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id    INTEGER PRIMARY KEY,
        claim_id       INTEGER REFERENCES claims (claim_id),
        incident_date  TEXT,
        location       TEXT,
        report_details TEXT    NOT NULL
    )
    """)

    # Create logs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        log_id    INTEGER PRIMARY KEY,
        user_id   INTEGER REFERENCES users (user_id),
        action    TEXT    CHECK (action IN ('login', 'added claim', 'deleted claim') ) NOT NULL,
        timestamp TEXT
    )
    """)

    # Create logs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id   INTEGER PRIMARY KEY,
    customer_id  INTEGER REFERENCES customers (customer_id),
    policy_id    INTEGER REFERENCES [policy ] (policy_id),
    payment_date TEXT,
    amount       REAL,
    payment_type TEXT    CHECK (payment_type IN ('premium' OR 'claim payout') ) NOT NULL
    )
    """)


    # Create logs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id   INTEGER PRIMARY KEY,
    customer_id  INTEGER REFERENCES customers (customer_id),
    policy_id    INTEGER REFERENCES [policy ] (policy_id),
    payment_date TEXT,
    amount       REAL,
    payment_type TEXT    CHECK (payment_type IN ('premium' OR 'claim payout') ) NOT NULL
    )
    """)


    # Create logs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS policies (
        policy_id        INTEGER PRIMARY KEY,
        customer_id      INTEGER REFERENCES customers (customer_id),
        policy_number    TEXT    UNIQUE,
        coverage_type    TEXT    UNIQUE,
        start_date       TEXT,
        end_date         TEXT,
        premium_amount   REAL,
        payment_schedule TEXT,
        coverage_limit   REAL,
        exclusions       TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
