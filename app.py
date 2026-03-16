from flask import Flask, render_template, request, send_file, redirect
import mercadopago
import qrcode
from io import BytesIO

app = Flask(__name__)

sdk = mercadopago.SDK("APP_USR-7805412692690237-072118-7991a0a58b9308b5461fdca4530de68d__LC_LB__-219875516")

pagamento_ok = False
link_salvo = ""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pagar", methods=["GET", "POST"])
def pagar():

    link = request.values.get("link")

    if not link:
        return "Link não enviado"

    return "OK"

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
            "success": "https://qrcodepix.onrender.com/sucesso?link=" + link,
            "failure": "https://qrcodepix.onrender.com/erro"
        },
        "auto_return": "approved"
    }

    preference = sdk.preference().create(preference_data)

    return redirect(preference["response"]["init_point"])


@app.route("/sucesso")
def sucesso():

    global pagamento_ok
    global link_salvo

    pagamento_ok = True
    link_salvo = request.args.get("link")

    return render_template("sucesso.html")


@app.route("/gerar")
def gerar():

    global pagamento_ok
    global link_salvo

    if not pagamento_ok:
        return "Pagamento não confirmado"

    if not link_salvo:
        return "Link vazio"

    img = qrcode.make(link_salvo)

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
