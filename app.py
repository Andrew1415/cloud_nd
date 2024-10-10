from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

CSV_FILE = 'data.csv'

# Load data from CSV
def load_data():
    data = []
    try:
        with open(CSV_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass
    return data

# Save data to CSV
def save_data(data):
    with open(CSV_FILE, 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/create', methods=['POST'])
def create():
    data = load_data()
    new_id = str(len(data) + 1)
    new_entry = {
        'id': new_id,
        'name': request.form['name'],
        'email': request.form['email']
    }
    data.append(new_entry)
    save_data(data)
    return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    data = load_data()
    data = [entry for entry in data if entry['id'] != id]
    save_data(data)
    return redirect('/')

@app.route('/update/<id>', methods=['POST'])
def update(id):
    data = load_data()
    for entry in data:
        if entry['id'] == id:
            entry['name'] = request.form['name']
            entry['email'] = request.form['email']
    save_data(data)
    return redirect('/')

@app.route('/edit/<id>')
def edit(id):
    data = load_data()
    entry = next((item for item in data if item['id'] == id), None)
    return render_template('edit.html', entry=entry)

if __name__ == '__main__':
    app.run(debug=True)
