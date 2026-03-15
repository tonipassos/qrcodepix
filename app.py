from flask import Flask, render_template, request, send_file
import qrcode
import mercadopago
import os

app = Flask(__name__)

ACCESS_TOKEN = "APP_USR-7805412692690237-072118-7991a0a58b9308b5461fdca4530de68d__LC_LB__-219875516"

sdk = mercadopago.SDK(ACCESS_TOKEN)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pagar", methods=["POST"])
def pagar():

    link = request.form["link"]

    preference_data = {
        "items": [
            {
                "title": "Gerar QR Code",
                "quantity": 1,
                "unit_price": 10.00
            }
        ]
    }

    preference = sdk.preference().create(preference_data)

    return render_template(
        "pagar.html",
        init_point=preference["response"]["init_point"],
        link=link
    )


@app.route("/gerar")
def gerar():

    link = request.args.get("link")

    img = qrcode.make(link)

    caminho = "qrcode.png"
    img.save(caminho)

    return send_file(caminho, as_attachment=True)


app.run(host="0.0.0.0", port=10000)