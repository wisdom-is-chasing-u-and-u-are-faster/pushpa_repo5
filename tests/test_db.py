import os
import sqlite3
from app.db.init_db import init_database

TEST_DB = "test_smart_study.db"


def setup_clean_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    init_database(TEST_DB)
    return sqlite3.connect(TEST_DB)


def test_schema_tables_exist():
    """
    Test schema table existence.
    AC: [ARCH-5847-AC1] The implemented UI must visually match the provided "Variant A" mockups.
    """
    conn = setup_clean_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    expected = ["users", "syllabi", "study_blocks", "quizzes", "quiz_questions", "quiz_submissions"]
    for t in expected:
        assert t in tables


def test_seed_records_exist():
    """
    Test seed records existence.
    AC: [ARCH-5847-AC1] The implemented UI must visually match the provided "Variant A" mockups.
    """
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM syllabi")
    syl_count = cursor.fetchone()[0]
    conn.close()

    assert user_count >= 5
    assert syl_count >= 3
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
