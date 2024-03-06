import unittest
import psycopg2 as psycopg
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from app import app, get_db_connection
from flask import json

# Load environment variables from .env file
load_dotenv()


class TestDatabaseConnection(unittest.TestCase):
    def test_db_connection(self):
        """Test database connection."""
        try:
            connection = get_db_connection()
            # If we can get the server version, we have a working connection
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print("Connected to PostgreSQL version:", db_version)
        except psycopg.Error as e:
            self.fail("PostgreSQL Error: " + str(e))
        finally:
            if connection:
                connection.close()
                print("Database connection closed.")


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def mock_get_db_connection_success():
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        # Setup for register_submit
        mock_cursor.rowcount = 1  # Simulate an insert
        # Setup for login
        mock_cursor.fetchone.return_value = {
            "userid": "testuser",
            "password": "password",
        }
        mock_cursor.rowcount = 1  # Simulate a successful login
        return mock_conn

    def mock_get_db_connection_fail():
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        # Setup for a failed login
        mock_cursor.fetchone.return_value = None
        mock_cursor.rowcount = 0  # Simulate a failed login
        return mock_conn

        # Mock setups for delete_account

    def mock_delete_account_success():
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        # Simulate a successful delete operation
        mock_cursor.rowcount = 1  # Rowcount reflects the number of rows deleted
        return mock_conn

    @patch("app.get_db_connection", side_effect=mock_get_db_connection_success)
    def test_register_submit(self, mock_get_db_connection):
        response = self.client.post(
            "/register_submit",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "DoB": "2000-01-01",
                "username": "johndoe",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data, "Deadline added successfully")

    @patch("app.get_db_connection", side_effect=mock_get_db_connection_success)
    def test_login_success(self, mock_get_db_connection):
        response = self.client.post(
            "/login", json={"username": "johndoe", "password": "password123"}
        )
        self.assertEqual(response.status_code, 200)
        # The exact assertion here depends on how your application formats the successful login response

    @patch("app.get_db_connection", side_effect=mock_get_db_connection_fail)
    def test_login_fail(self, mock_get_db_connection):
        response = self.client.post(
            "/login", json={"username": "wronguser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data, "Wrong username or password")

    @patch("app.get_db_connection", side_effect=mock_delete_account_success)
    def test_delete_account_success(self, mock_get_db_connection):
        # Assuming the user "johndoe" exists and the deletion is successful
        response = self.client.post("/delete_account", json={"username": "johndoe"})
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
