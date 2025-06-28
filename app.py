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
   "garlic": {
    "soil": "Loamy soil",
    "climate": "Cool - mid",
    "tips": "Plant individual cloves,Water moderately"
},
"sweet potato": {
    "soil": " Sandy loamy soil",
    "climate": "warm and humid",
    "tips": "Use slips (vine cuttings) rather than seeds"
},
"tamarind": {
    "soil":
    "Sandy loam or loamy soil",
    "climate":
    "Tropical to subtropical",
    "tips":
    "Water young trees regularly and Intercrop with legumes or herbs in early years"
},
"pepper": {
    "soil": "Rich, well-drained loamy soil with high organic content",
    "climate": "Hot and humid",
    "tips": "Requires a support tree or pole to climb"
},
"mango": {
    "soil": "Well-drained loamy soil",
    "climate": "Tropical to subtropical",
    "tips": "Use grafted saplings water consistently"
},
"apple": {
    "soil": "Well-drained loamy soil",
    "climate": "Cool",
    "tips": "Prune regularly and provide adequate sunlight."
},
"lemon": {
    "soil": "Well-drained loamy soil",
    "climate": "Warm",
    "tips": "Water consistently and provide adequate sunlight."
},
"papaya": {
    "soil": "Loamy soil",
    "climate": "Warm",
    "tips": "Water consistently and provide adequate sunlight."
},
"wheat": {
    "soil": "Clay loam",
    "climate": "Cool",
    "tips": "Use certified seeds and rotate crops."
},
"sunflower": {
    "soil": "Neutral loam",
    "climate": "Warm",
    "tips": "Rotate crops to reduce pest risk."
},
"maize": {
    "soil": "Fertile loam",
    "climate": "Warm with rain",
    "tips": "Weed early and apply nitrogen fertilizer."
},
"sugarcane": {
    "soil": "Deep loam",
    "climate": "Hot, humid",
    "tips": "Practice ratooning and irrigate during dry phases."
},
"cotton": {
    "soil": "Black soil",
    "climate": "Warm, dry",
    "tips": "Monitor for bollworms and use resistant varieties."
},
"millet": {
    "soil": "Sandy loam",
    "climate": "Arid to semi-arid",
    "tips": "Ideal for intercropping in dryland areas."
},
"soybean": {
    "soil": "Neutral pH loam",
    "climate": "Warm and moist",
    "tips": "Inoculate seeds with Rhizobium bacteria."
},
"barley": {
    "soil": "Sandy loam",
    "climate": "Cool season",
    "tips": "Avoid waterlogging and ensure timely sowing."
},
"groundnut": {
    "soil": "Sandy loam",
    "climate": "Dry to moist",
    "tips": "Use gypsum during pegging for better pod formation."
},
"chickpea": {
    "soil": "Loamy",
    "climate": "Cool and dry",
    "tips": "Apply Trichoderma to seeds for fungal resistance."
},
"mustard": {
    "soil": "Clay or loam",
    "climate": "Cool, dry",
    "tips": "Early sowing ensures higher oil yield."
},
"sorghum": {
    "soil": "Loamy",
    "climate": "Semi-arid",
    "tips": "Remove excess tillers to ensure better grain quality."
},
"banana": {
    "soil": "Fertile loam",
    "climate": "Tropical",
    "tips": "Potassium is essential at flowering."
},
"tomato": {
    "soil": "Sandy loam",
    "climate": "Warm and dry",
    "tips": "Stake plants and maintain even watering."
},
"onion": {
    "soil": "Light loam",
    "climate": "Cool start, warm finish",
    "tips": "Avoid standing water."
},
"potato": {
    "soil": "Sandy loam",
    "climate": "Cool",
    "tips": "Hilling helps with tuber development."
},
"brinjal": {
    "soil": "Loamy",
    "climate": "Warm and humid",
    "tips": "Watch for shoot borers and use neem-based sprays."
},
"carrot": {
    "soil": "Sandy loam",
    "climate": "Cool",
    "tips": "Thin early for better root shape."
},
"cabbage": {
    "soil": "Loamy",
    "climate": "Cool",
    "tips": "Maintain proper spacing for head formation."
},
"cauliflower": {
    "soil": "Sandy loam",
    "climate": "Cool",
    "tips": "Avoid excess nitrogen late in the season."
},
"green gram": {
    "soil": "Sandy loam",
    "climate": "Warm",
    "tips": "Ideal for Kharif and summer cropping."
},
"black gram": {
    "soil": "Loam to clay",
    "climate": "Warm and moist",
    "tips": "Rotate crops to break disease cycles."
},
"pigeon pea": {
    "soil": "Well-drained loam",
    "climate": "Semi-arid",
    "tips": "Deep roots, requires minimal irrigation."
},
"peas": {
    "soil": "Loamy",
    "climate": "Cool",
    "tips": "Harvest before pods become fibrous."
},
"lentil": {
    "soil": "Loam to clay loam",
    "climate": "Cool",
    "tips": "Avoid overwatering."
},
"spinach": {
    "soil": "Loamy",
    "climate": "Cool",
    "tips": "Frequent harvesting encourages regrowth."
},
"cucumber": {
    "soil": "Loamy",
    "climate": "Warm and moist",
    "tips": "Trellis improves yield and airflow."
},
"bitter gourd": {
    "soil": "Sandy loam",
    "climate": "Hot and moist",
    "tips": "Use well-rotted compost at planting."
},
"ridge gourd": {
    "soil": "Loam",
    "climate": "Warm",
    "tips": "Grow on trellises for straighter fruits."
},
"pumpkin": {
    "soil": "Sandy loam",
    "climate": "Warm and dry",
    "tips": "Mulch well to retain soil moisture."
},
"ladyfinger": {
    "soil": "Loamy",
    "climate": "Warm",
    "tips": "Pick pods when tender every alternate day."
},
"amaranth": {
    "soil": "Loamy",
    "climate": "Tropical to temperate",
    "tips": "Harvest early for softer leaves."
},
"fenugreek": {
    "soil": "Sandy loam",
    "climate": "Cool",
    "tips": "Green manure use improves fertility."
},
"beetroot": {
    "soil": "Sandy loam",
    "climate": "Cool",
    "tips": "Thin seedlings to prevent crowding."
},
"turnip": {
    "soil": "Loamy",
    "climate": "Cool",
    "tips": "Harvest young for best flavor."
},
"radish": {
    "soil": "Sandy loam",
    "climate": "Cool",
    "tips": "Harvest before roots get woody."
},
"lettuce": {
    "soil": "Fertile, moist",
    "climate": "Cool",
    "tips": "Use mulch in warmer zones."
},
"celery": {
    "soil": "Moist loam",
    "climate": "Cool and humid",
    "tips": "Continuous water supply needed."
},
"capsicum": {
    "soil": "Loam",
    "climate": "Mild",
    "tips": "Support with sticks and harvest gradually."
},
"chilli": {
    "soil": "Loamy",
    "climate": "Warm",
    "tips": "Prune for more branching."
},
"ginger": {
    "soil": "Loamy with organic matter",
    "climate": "Warm and humid",
    "tips": "Needs partial shade and good drainage."
},
"turmeric": {
    "soil": "Well-drained loam",
    "climate": "Tropical",
    "tips": "Needs 7–9 month growing period."
},
"cardamom": {
    "soil": "Rich forest loam",
    "climate": "Humid, shaded",
    "tips": "Grows best under filtered sunlight."
},
"coffee": {
    "soil": "Laterite",
    "climate": "Cool hills with shade",
    "tips": "Mulch for moisture retention."
},
"tea": {
    "soil": "Acidic loam",
    "climate": "Misty and humid",
    "tips": "Regular pruning encourages growth."
},
"rubber": {
    "soil": "Deep loamy",
    "climate": "Hot and moist",
    "tips": "Tap trees after 6 years."
},
"coconut": {
    "soil": "Sandy loam",
    "climate": "Tropical coastal",
    "tips": "Apply compost at least twice yearly."
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
