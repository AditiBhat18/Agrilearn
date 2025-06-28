from flask import Flask, render_template, request, redirect, session, jsonify
import json, os
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "agri_secret_key"
CORS(app)


# ------------------- Helper Functions ------------------- #
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)


# ------------------- Crop Data ------------------- #
crop_data = {
    "rice": {
        "soil": "Loamy soil",
        "climate": "Warm, humid",
        "tips": "Transplant seedlings after 25–30 days."
    },
    "corn": {
        "soil": "clay loam or silt loam",
        "climate": "warm",
        "tips": "water consistently and proper spacing"
    },
   
    "arecanut": {
        "soil": "Alluvial or loam",
        "climate": "Humid tropics",
        "tips": "Shade and irrigation are essential."
    }
}


# ------------------- Auth Routes ------------------- #
@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        users = load_users()

        if email in users:
            return "<h3>Email already registered.</h3><a href='/'>Login</a>"

        users[email] = {
            'name': name,
            'password': password,
            'progress': {
                'organic': False,
                'composting': False,
                'drip': False,
                'pest': False,
                'rainwater': False,
                'intercropping': False
            }
        }

        save_users(users)
        session['user'] = name
        session['email'] = email
        return redirect('/home')

    return render_template('signup.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    users = load_users()
    user = users.get(email)

    if user and user['password'] == password:
        session['user'] = user['name']
        session['email'] = email
        return redirect('/home')

    return "<h3>Invalid credentials.</h3><a href='/'>Try again</a>"


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ------------------- Page Routes ------------------- #
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template('home.html', username=session['user'])


@app.route('/learn')
def learn():
    if 'user' not in session or 'email' not in session:
        return redirect('/')
    users = load_users()
    email = session['email']
    valid_modules = [
        'organic', 'composting', 'dripirigation', 'pest', 'rainwater',
        'intercropping'
    ]
    progress = {
        k: users.get(email, {}).get('progress', {}).get(k, False)
        for k in valid_modules
    }
    total = len(valid_modules)

    completed = sum(1 for v in progress.values() if v)
    return render_template('learn.html',
                           progress=progress,
                           completed=completed,
                           total=total)


@app.route('/module/<module_name>')
def module_page(module_name):
    if 'user' not in session:
        return redirect('/')
    return render_template(f'modules/{module_name}.html')


@app.route('/mark_complete', methods=['POST'])
def mark_complete():
    if 'email' not in session:
        return jsonify({"status": "unauthorized"}), 401

    data = request.get_json()
    module = data.get('module')

    if not module:
        return jsonify({"status": "failed"}), 400

    users = load_users()
    email = session['email']

    if email not in users:
        return jsonify({"status": "user not found"}), 404

    if 'progress' not in users[email]:
        users[email]['progress'] = {}

    users[email]['progress'][module] = True
    save_users(users)

    return jsonify({"status": "success"})


@app.route('/get_progress')
def get_progress():
    if 'email' not in session:
        return jsonify({"completed_modules": []})
    users = load_users()
    email = session['email']
    completed = [
        k for k, v in users.get(email, {}).get('progress', {}).items() if v
    ]
    return jsonify({"completed_modules": completed})


@app.route('/fix_existing_progress')
def fix_existing_progress():
    users = load_users()
    changed = False
    default_progress = {
        'organic': False,
        'composting': False,
        'drip': False,
        'pest': False,
        'rainwater': False,
        'intercropping': False
    }
    for u in users.values():
        if 'progress' not in u:
            u['progress'] = default_progress.copy()
            changed = True
    if changed:
        save_users(users)
        return "Progress field added!"
    return "All users are up to date."


# ------------------- Assistant & Certificate ------------------- #
@app.route('/assistant')
def assistant():
    if 'user' not in session:
        return redirect('/')
    return render_template('assistant.html')


@app.route('/get_crop_info')
def get_crop_info():
    crop = request.args.get("crop", "").lower()
    data = crop_data.get(crop)
    if data:
        return jsonify({"status": "success", "crop": crop, "data": data})
    return jsonify({"status": "error", "message": "Crop not found"}), 404


@app.route('/certificate')
def certificate():
    if 'email' not in session:
        return redirect('/')

    users = load_users()
    user = users.get(session['email'], {})
    progress = user.get('progress', {})

    valid_modules = [
        'organic', 'composting', 'dripirigation', 'pest', 'rainwater',
        'intercropping'
    ]
    if all(progress.get(k) for k in valid_modules):
        return render_template('certificate.html', name=user['name'])

    return "<h3>Finish all lessons to unlock your certificate 🎓</h3><a href='/learn'>Go back</a>"


@app.route('/cleanup_progress')
def cleanup_progress():
    users = load_users()
    valid = [
        'organic', 'composting', 'dripirigation', 'pest', 'rainwater',
        'intercropping'
    ]
    for u in users.values():
        if 'progress' in u:
            u['progress'] = {
                k: v
                for k, v in u['progress'].items() if k in valid
            }
    save_users(users)
    return "Extra progress keys cleaned!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
