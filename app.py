from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from forms import BuyerRegistrationForm, SellerRegistrationForm, BuyerLoginForm, SellerLoginForm
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///construcomparar.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure key
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    if Buyer.query.get(int(user_id)):
        return Buyer.query.get(int(user_id))
    else:
        return Seller.query.get(int(user_id))


# Database models

class Buyer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Add other fields as needed

class Seller(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Add other fields as needed

# Wrap the db.create_all() call inside an app.app_context()
with app.app_context():
    db.create_all()

# Routes

@app.route('/')
def index():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    buyer_form = BuyerRegistrationForm()
    seller_form = SellerRegistrationForm()
    if request.method == 'POST':
        if buyer_form.validate_on_submit():
            hashed_password = generate_password_hash(buyer_form.password.data, method='sha256')
            new_buyer = Buyer(email=buyer_form.email.data, password=hashed_password)
            db.session.add(new_buyer)
            db.session.commit()
            flash('Congratulations, you are now a registered buyer!', 'success')
            return redirect(url_for('login'))
        elif seller_form.validate_on_submit():
            hashed_password = generate_password_hash(seller_form.password.data, method='sha256')
            new_seller = Seller(email=seller_form.email.data, password=hashed_password)
            db.session.add(new_seller)
            db.session.commit()
            flash('Congratulations, you are now a registered seller!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration Unsuccessful. Please check the entered data.', 'danger')
    return render_template('register.html', title='Register', buyer_form=buyer_form, seller_form=seller_form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    buyer_form = BuyerLoginForm()
    seller_form = SellerLoginForm()
    if buyer_form.validate_on_submit():
        user = Buyer.query.filter_by(email=buyer_form.email.data).first()
        if user and check_password_hash(user.password, buyer_form.password.data):
            login_user(user, remember=buyer_form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('buyer_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    elif seller_form.validate_on_submit():
        user = Seller.query.filter_by(email=seller_form.email.data).first()
        if user and check_password_hash(user.password, seller_form.password.data):
            login_user(user, remember=seller_form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('seller_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
     return render_template('login.html', title='Login', buyer_form=buyer_form, seller_form=seller_form)

@app.route('/buyer_dashboard')
@login_required
def buyer_dashboard():
    # You can add logic here to fetch and display active quotes or show a button to create a quote request
    return render_template('buyer_dashboard.html', title='Buyer Dashboard')

@app.route('/seller_dashboard')
@login_required
def seller_dashboard():
    # You can add logic here to fetch and display submitted quotes for active quote requests
    return render_template('seller_dashboard.html', title='Seller Dashboard')


    return render_template('login.html', title='Login', buyer_form=buyer_form, seller_form=seller_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Main entry point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)