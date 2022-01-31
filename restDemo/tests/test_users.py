import pytest
import os
import tempfile

testing = True
from app import app

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    #app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)