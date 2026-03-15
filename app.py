from flask import Flask, render_template, request, send_file, redirect
import mercadopago
import qrcode

app = Flask(__name__)

sdk = mercadopago.SDK("APP_USR-7805412692690237-072118-7991a0a58b9308b5461fdca4530de68d__LC_LB__-219875516")

pagamento_ok = False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pagar")
def pagar():

    global pagamento_ok
    pagamento_ok = False

    preference_data = {
        "items": [
            {
                "title": "Gerar QR Code",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 5
            }
        ],

        "back_urls": {
            "success": "https://qrcodepix.onrender.com/sucesso",
            "failure": "https://qrcodepix.onrender.com/erro"
        },

        "auto_return": "approved"
    }

    preference = sdk.preference().create(preference_data)

    link = preference["response"]["init_point"]

    return redirect(link)


@app.route("/sucesso")
def sucesso():

    global pagamento_ok
    pagamento_ok = True

    return render_template("sucesso.html")


@app.route("/gerar")
def gerar():

    global pagamento_ok

    if not pagamento_ok:
        return "Pagamento não confirmado"

    link = request.args.get("link")

    img = qrcode.make(link)
    img.save("qr.png")

    return send_file("qr.png", as_attachment=True)


app.run(host="0.0.0.0", port=10000)


