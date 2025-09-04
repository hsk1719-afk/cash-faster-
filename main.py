from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import csv
import os

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)  # Enable CORS for all routes

CLIENT_DATA = []

def load_client_data():
    global CLIENT_DATA
    data = []
    
    # Load first CSV file
    try:
        with open("استمارةجديدةعميل.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print("File استمارةجديدةعميل.csv not found")
    
    # Load second CSV file
    try:
        with open("نموذج٩-٢-٢٠٢٥.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print("File نموذج٩-٢-٢٠٢٥.csv not found")
    
    CLIENT_DATA = data
    print(f"Loaded {len(CLIENT_DATA)} client records")

@app.route("/api/client/<national_id>")
def get_client_data(national_id):
    for client in CLIENT_DATA:
        # Handle both possible column names for national ID
        client_national_id = client.get("2. رقم العميل القومي") or client.get("2. رقم العميل القومى")
        if client_national_id == national_id:
            return jsonify(client)
    return jsonify({"error": "Client not found"}), 404

@app.route("/api/clients")
def get_all_clients():
    return jsonify(CLIENT_DATA)

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/inquiry.html")
def serve_inquiry():
    return send_from_directory(app.static_folder, "inquiry.html")

@app.route("/loan_confirmation.html")
def serve_loan_confirmation():
    return send_from_directory(app.static_folder, "loan_confirmation.html")

@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    load_client_data()
    app.run(host="0.0.0.0", port=5000, debug=True)

