from flask import Flask, jsonify, request
from repository.database import db
from db_models.payement import Payment
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from os import getenv


load_dotenv('.env')
DATABASE_URL = getenv('DATABASE_URL')
SECRET_KEY = getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
    data = request.get_json()

    if 'value' not in data:
        return jsonify({"error": "O valor do pagamento é obrigatório."}), 400

    expiration_date = datetime.now(timezone.utc) + timedelta(minutes=30)
    new_payment = Payment(
        value=data['value'],
        paid=data.get('paid', False),
        bank_payment_id=data.get('bank_payment_id'),
        qr_code=data.get('qr_code'),
        expiration_date=expiration_date
    )
    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message": "O pagamento foi criado!", "payment": new_payment.to_dict()}), 201

@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confirmation():
    return jsonify({"message": "O pagamento foi confirmado!"})

@app.route('/payments/pix/<int:payment_id>', methods = ['GET'])
def payment_pix_page(payment_id):
    return 'pagamento pix'

if __name__ == "__main__":
    app.run(debug=True, port=5000)


