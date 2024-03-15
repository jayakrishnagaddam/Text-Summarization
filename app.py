from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_pymongo import PyMongo
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234"
app.config["MONGO_URI"] = "mongodb+srv://2100090162:manigaddam@deepsheild.kzgpo9p.mongodb.net/textsummarizationsDB"
mongo = PyMongo(app)

@app.route('/send_otp', methods=['POST'])
def send_otp():
    # Add your logic to send OTP here
    return jsonify({'message': 'OTP sent successfully'})
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        mobile_number = request.form.get('mobile_number')
        otp_entered = request.form.get('otp')

        # Fetch user from database based on mobile number
        user_data = mongo.db.users.find_one({'mobile_number': mobile_number})

        if user_data:
            # Generate OTP
            otp_generated = ''.join(random.choices('0123456789', k=6))
            
            # Save OTP to session
            session['otp'] = otp_generated
            
            # Send OTP
            send_otp(mobile_number, otp_generated)
            
            # Redirect to verify OTP
            return redirect(url_for('verify_otp'))
        else:
            error = 'Mobile number not registered'

    return render_template('login.html', error=error)

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'otp' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        otp_entered = request.form.get('otp')
        otp_generated = session['otp']
        
        if otp_entered == otp_generated:
            # OTP is correct, login successful
            return redirect(url_for('homepage', name="User"))  # Redirect to homepage
        else:
            flash('Invalid OTP. Please try again.', 'error')

    return render_template('verify_otp.html')

@app.route('/homepage/<name>')
def homepage(name):
    return render_template('homepage.html', name=name)

@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/localmarkets')
def localmarkets():
    return render_template('localmarkets.html')

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