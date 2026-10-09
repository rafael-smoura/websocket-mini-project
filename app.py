from datetime import datetime, timedelta, timezone
from os import getenv
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file, render_template
from flask_socketio import SocketIO
from db_models.payement import Payment
from payments.pix import Pix
from repository.database import db

load_dotenv('.env')
DATABASE_URL = getenv('DATABASE_URL')
SECRET_KEY = getenv('SECRET_KEY')
ALLOWED_ORIGINS = getenv('ALLOWED_ORIGINS').split(',')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins=ALLOWED_ORIGINS)  # Restringe as rotas que podem ter acesso ao servidor

@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
    data = request.get_json() or {}

    if 'value' not in data or data['value'] is None:
        return jsonify({"error": "O valor do pagamento é obrigatório."}), 400

    # Gera os dados do Pix/QR Code no banco simulado/API externa
    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()

    # Define a expiração (30 min em UTC)
    expiration_date = datetime.now(timezone.utc) + timedelta(minutes=30)

    new_payment = Payment(
        value=data['value'],
        paid=False,
        bank_payment_id=data_payment_pix['bank_payment_id'],
        qr_code=data_payment_pix['qr_code_path'],
        expiration_date=expiration_date
    )

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({
        "message": "O pagamento foi criado!",
        "payment": new_payment.to_dict()
    }), 201

@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confirmation():
    data = request.get_json() or {}

    # validations
    if "bank_payment_id" not in data and "value" not in data:
        return jsonify({"error": "Invalid payment data"}), 400

    # payment confirmation
    payment = Payment.query.filter_by(bank_payment_id=data.get('bank_payment_id')).first()

    if not payment:
        return render_template('404.html'), 404
    
    elif payment.paid:
        return jsonify({"error": "Invalid payment"}), 400

    if data.get("value") != payment.value:
        return jsonify({"error": "Invalid payment value"}), 400

    payment.paid = True
    db.session.commit()

    return render_template('confirmed_payment.html')

@app.route('/payments/pix/qr_code/<file_name>',methods=['GET'])
def get_image(file_name):
    return send_file(f"static/img/{file_name}.png", mimetype='image/png')

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    payment = db.session.get(Payment, payment_id)  # Apenas para verificar se o pagamento existe

    if not payment:
        return render_template('404.html'), 404
    return render_template('payment.html', 
                           payment_id=payment_id, 
                           value=payment.value, 
                           host="http://localhost:5000", 
                           qr_code = payment.qr_code)

# websockets
@socketio.on('connect') # espera evento 
def hand_shake():
    print('Client connected to the server')

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000) # Sockets implementado
   