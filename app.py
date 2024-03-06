from flask import Flask, jsonify, request
import psycopg2 as psycopg
import os

app = Flask(__name__)

# SQL
DB_HOST = "db.doc.ic.ac.uk"
DB_USER = "sf23"
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = "sf23"
DB_PORT = "5432"


def get_db_connection():
    server_params = {
        "dbname": DB_USER,
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "client_encoding": "utf-8",
    }
    return psycopg.connect(**server_params)


@app.route("/register_submit", methods=["POST"])
def register_submit():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    full_name = first_name + " " + last_name
    DoB = data.get("DoB")
    username = data.get("username")
    password = data.get("password")

    if not all([full_name, username, password]):
        return jsonify("Missing data"), 400

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql_command = "INSERT INTO notes_user_2 (name, dob, userid, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_command, (full_name, DoB, username, password))
            connection.commit()
            return jsonify("Deadline added successfully"), 201
        except (Exception, psycopg.Error) as error:
            print("Error while inserting data into PostgreSQL", error)
            return jsonify("Failed to register user"), 500
        finally:
            if connection is not None:
                connection.close()
    else:
        return jsonify("Failed to connect to the database"), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify("Missing username"), 400
    if not password:
        return jsonify("Missing password"), 400

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM notes_user_2 WHERE userid = %s AND password = %s"
            cursor.execute(query, (username, password))
            if cursor.rowcount == 0:
                return jsonify("Wrong username or password"), 404
            user = cursor.fetchone()
        except (Exception, psycopg.Error) as error:
            print("Error retrieving user info: ", error)
        finally:
            connection.close()
    else:
        return jsonify("Failed to connect to the database"), 500
    return jsonify(user), 200


@app.route("/delete_account", methods=["POST"])
def delete_account():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify("Missing username"), 400

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql_command = "DELETE FROM notes_user_2 WHERE userid = %s"
            cursor.execute(sql_command, (username,))
            connection.commit()
            return jsonify("Account deleted"), 200
        except (Exception, psycopg.Error) as error:
            print("Error deleting account: ", error)
        finally:
            connection.close()
    else:
        return jsonify("Failed to connect to the database"), 500


if __name__ == "__main__":
    app.run(debug=True)
