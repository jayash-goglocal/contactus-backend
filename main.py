from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
db = SQLAlchemy(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jayash.s@goglocal.com'
app.config['MAIL_PASSWORD'] = 'StrongSuper$403'
mail = Mail(app)

# Define the database model
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(50))
    company_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    person_name = db.Column(db.String(100))
    website_link = db.Column(db.String(100))
    description = db.Column(db.String(500))

    def __init__(self, designation, company_name, email, phone, person_name, website_link, description):
        self.designation = designation
        self.company_name = company_name
        self.email = email
        self.phone = phone
        self.person_name = person_name
        self.website_link = website_link
        self.description = description

@app.route('/register', methods=['POST'])
def register():
    designation = request.form.get('designation')
    company_name = request.form.get('company_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    person_name = request.form.get('person_name')
    website_link = request.form.get('website_link')
    description = request.form.get('description')

    # Save the registration details to the database
    registration = Registration(designation, company_name, email, phone, person_name, website_link, description)
    db.session.add(registration)
    db.session.commit()

    # Send thank you email
    send_email(email)

    response = {'message': 'Registration successful'}
    return jsonify(response)

def send_email(email):
    recipients = ['jayash.s@goglocal.com', email]
    subject = 'Thank you for your registration'
    body = 'Thank you for registering with us. We appreciate your interest.'
    msg = Message(subject=subject, recipients=recipients, body=body)
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
