from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from contextlib import closing
import sqlite3

app = Flask(__name__)
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Python Hacking', version='0.0.1')


def db_conn():
    conn = sqlite3.connect("services.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/services")
def services(methods=["GET"]):
    data = []
    with closing(db_conn()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM services")
        for row in cur.fetchall():
            data.append(dict(row))
    return jsonify(data)


@app.route("/service/<id>")
def service(id, methods=["GET"]):
    with closing(db_conn()) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM services WHERE id={id}")
        for row in cur.fetchall():
            return jsonify(dict(row))


if __name__ == "__main__":
    app.run(debug=True)
