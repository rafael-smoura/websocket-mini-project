from flask import Flask, jsonify, request
from repository.database import db
from dotenv import load_dotenv
from os import getenv

load_dotenv('.env')
DATABASE_URL = getenv('DATABASE_URL')
SECRET_KEY = getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

@app.route('/payment/pix', methods=['POST'])
def create_payment_pix():
    return jsonify({"message": "O pagamento foi criado!"})

@app.route('/payment/pix/confirmation', methods=['POST'])
def pix_confirmation():
    return jsonify({"message": "O pagamento foi confirmado!"})

@app.route('/payment/pix/<int:payment_id>', methods = ['GET'])
def payment_pix_page(payment_id):
    return 'pagamento pix'

if __name__ == "__main__":
    app.run(debug=True, port=5000)


