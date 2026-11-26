from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB = 'threats.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            severity TEXT NOT NULL,
            source TEXT,
            description TEXT,
            date_logged TEXT NOT NULL
        )
    ''')
    # Seed with sample data if empty
    if conn.execute('SELECT COUNT(*) FROM threats').fetchone()[0] == 0:
        sample = [
            ('WannaCry', 'Ransomware', 'Critical', 'DHS Alert', 'Encrypts files and demands ransom payment via Bitcoin.', '2024-01-15'),
            ('Emotet', 'Malware', 'High', 'CISA Advisory', 'Banking trojan that spreads via phishing emails and steals credentials.', '2024-02-03'),
            ('SolarWinds SUNBURST', 'APT', 'Critical', 'NSA Report', 'Supply chain attack targeting government and enterprise networks.', '2024-02-20'),
            ('Phishing Campaign - IRS', 'Phishing', 'Medium', 'Internal', 'Spoofed IRS emails targeting federal employees during tax season.', '2024-03-01'),
            ('Log4Shell Exploit', 'Vulnerability Exploit', 'Critical', 'MITRE ATT&CK', 'Remote code execution via Log4j library affecting thousands of systems.', '2024-03-10'),
            ('BlackCat Ransomware', 'Ransomware', 'High', 'FBI Flash', 'Ransomware-as-a-service targeting critical infrastructure.', '2024-04-05'),
        ]
        conn.executemany(
            'INSERT INTO threats (name, type, severity, source, description, date_logged) VALUES (?,?,?,?,?,?)',
            sample
        )
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    search = request.args.get('search', '')
    type_filter = request.args.get('type', '')
    severity_filter = request.args.get('severity', '')

    query = 'SELECT * FROM threats WHERE 1=1'
    params = []

    if search:
        query += ' AND (name LIKE ? OR description LIKE ?)'
        params += [f'%{search}%', f'%{search}%']
    if type_filter:
        query += ' AND type = ?'
        params.append(type_filter)
    if severity_filter:
        query += ' AND severity = ?'
        params.append(severity_filter)

    query += ' ORDER BY date_logged DESC'
    threats = conn.execute(query, params).fetchall()

    # Stats
    total = conn.execute('SELECT COUNT(*) FROM threats').fetchone()[0]
    critical = conn.execute("SELECT COUNT(*) FROM threats WHERE severity='Critical'").fetchone()[0]
    high = conn.execute("SELECT COUNT(*) FROM threats WHERE severity='High'").fetchone()[0]
    types = conn.execute('SELECT type, COUNT(*) as count FROM threats GROUP BY type').fetchall()

    conn.close()
    return render_template('index.html', threats=threats, total=total,
                           critical=critical, high=high, types=types,
                           search=search, type_filter=type_filter,
                           severity_filter=severity_filter)

@app.route('/add', methods=['GET', 'POST'])
def add_threat():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        severity = request.form['severity']
        source = request.form['source']
        description = request.form['description']
        date_logged = datetime.now().strftime('%Y-%m-%d')

        conn = get_db()
        conn.execute(
            'INSERT INTO threats (name, type, severity, source, description, date_logged) VALUES (?,?,?,?,?,?)',
            (name, type_, severity, source, description, date_logged)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/threat/<int:id>')
def threat_detail(id):
    conn = get_db()
    threat = conn.execute('SELECT * FROM threats WHERE id = ?', (id,)).fetchone()
    conn.close()
    if not threat:
        return 'Threat not found', 404
    return render_template('detail.html', threat=threat)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_threat(id):
    conn = get_db()
    conn.execute('DELETE FROM threats WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
