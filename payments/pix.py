import uuid
import qrcode

class Pix:
    def __init__(self):
        pass

    def create_payment(self):
        # cria o 'pagamento' na instituicao finaceira
        bank_payment_id = str(uuid.uuid4())

        # copia_e_cola_
        hash_payment = f'hash_payment_{bank_payment_id}'

        # qr code
        qrcode.make()
        img = qrcode.make(hash_payment)

        # salva a imagem como arquivo PNG
        img.save(f"static/img/qr_code_payment_{bank_payment_id}.png")

        return {"bank_payment_id": bank_payment_id,
                "qr_code_path": ""}