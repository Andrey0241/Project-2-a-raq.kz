from flask import Flask
from models import db
from routes import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ROOT:ROOT@localhost/Main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
