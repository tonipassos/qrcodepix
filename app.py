from flask import Flask, render_template, request, send_file, redirect
import mercadopago
import qrcode
from io import BytesIO

app = Flask(__name__)

sdk = mercadopago.SDK("SEU_TOKEN_AQUI")

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


@app.route("/gerar", methods=["GET", "POST"])
def gerar():

    global pagamento_ok

    if not pagamento_ok:
        return "Pagamento não confirmado"

    # aceita GET ou POST
    link = request.args.get("link") or request.form.get("link")

    if not link:
        return "Link vazio"

    img = qrcode.make(link)

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=True,
        download_name="qrcode.png"
    )


app.run(host="0.0.0.0", port=10000)


