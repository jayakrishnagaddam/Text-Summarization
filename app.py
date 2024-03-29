from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_pymongo import PyMongo
from transformers import pipeline

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234"
app.config["MONGO_URI"] = "mongodb+srv://2100090162:manigaddam@deepsheild.kzgpo9p.mongodb.net/textsummarizationsDB"
mongo = PyMongo(app)

@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.form.get('text')
    summarized_text = summarize_text(data)
    return jsonify(summarized_text=summarized_text)

def summarize_text(text):
    summarization_pipeline = pipeline("summarization", model="t5-small", tokenizer="t5-small")
    summary = summarization_pipeline(text, max_length=1000, min_length=2, do_sample=False)  # Increased max_length
    summarized_sentences = summary[0]['summary_text'].split('. ')  # Split sentences by '. '
    bullet_points = '\n- '.join(summarized_sentences)  # Join sentences with bullet points
    return bullet_points

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_data = mongo.db.users.find_one({'username': username, 'password': password})
        if user_data:
            firstname = user_data['first_name']
            session['username'] = username
            session['name'] = firstname  # Storing name in session
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)

@app.route('/home')
def home():
    if 'username' in session:
        # Retrieve name from session
        name = session.get('name')
        return render_template('home.html', name=name)
    else:
        return redirect(url_for('login'))


@app.route('/homepage')
def homepage():
    # Retrieve name from session
    name = session.get('name')
    return render_template('homepage.html', name=name)

@app.route('/careers')
def careers():
    return render_template('careers.html')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  
    flash('You have been logged out', 'success') 
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data = {
            'first_name': request.form.get('firstname'),
            'last_name': request.form.get('lastname'),
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }

        mongo.db.users.insert_one(user_data)

        flash('SIGN UP SUCCESSFULL...YOU CAN NOW LOGIN HERE...', 'success')  # Flash success message
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
