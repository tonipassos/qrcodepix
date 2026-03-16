from flask import Flask, render_template, request, send_file, redirect
import mercadopago
import qrcode
from io import BytesIO

app = Flask(__name__)

sdk = mercadopago.SDK("APP_USR-7805412692690237-072118-7991a0a58b9308b5461fdca4530de68d__LC_LB__-219875516")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pagar", methods=["POST"])
def pagar():

    link = request.form.get("link")

    if not link:
        return "Link não enviado"

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
            "success": "https://qrcodepix-zscq.onrender.com/sucesso?link=" + link,
            "failure": "https://qrcodepix-zscq.onrender.com/erro"
        },
        "auto_return": "approved"
    }

    preference = sdk.preference().create(preference_data)

    return redirect(preference["response"]["init_point"])


@app.route("/sucesso")
def sucesso():

    link = request.args.get("link")

    if not link:
        return "Link não encontrado"

    return redirect("/gerar?link=" + link)


@app.route("/gerar")
def gerar():

    link = request.args.get("link")

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
