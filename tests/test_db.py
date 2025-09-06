import pytest
from app.database import engine
from sqlalchemy import text

def test_database_connection():
    """Test that we can connect to the database"""
    with engine.connect() as connection:
        result = connection.execute(text('SELECT 1'))
        assert result.fetchone()[0] == 1
