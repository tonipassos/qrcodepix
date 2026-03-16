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

    tipo = request.form.get("tipo")
    link = request.form.get("link")
    chave = request.form.get("chave")
    nome = request.form.get("nome")
    cidade = request.form.get("cidade")
    valor = request.form.get("valor")

    # salvar tudo na URL
    dados = f"tipo={tipo}&link={link}&chave={chave}&nome={nome}&cidade={cidade}&valor={valor}"

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
            "success": "https://qrcodepix-zscq.onrender.com/sucesso?" + dados,
            "failure": "https://qrcodepix-zscq.onrender.com/erro"
        },
        "auto_return": "approved"
    }

    preference = sdk.preference().create(preference_data)

    return redirect(preference["response"]["init_point"])


@app.route("/sucesso")
def sucesso():

    tipo = request.args.get("tipo")
    link = request.args.get("link")
    chave = request.args.get("chave")
    nome = request.args.get("nome")
    cidade = request.args.get("cidade")
    valor = request.args.get("valor")

    return redirect(
        f"/gerar?tipo={tipo}&link={link}&chave={chave}&nome={nome}&cidade={cidade}&valor={valor}"
    )


@app.route("/gerar")
def gerar():

    tipo = request.args.get("tipo")

    if tipo == "site":

        link = request.args.get("link")

        if not link:
            return "Link vazio"

        dados = link


    elif tipo == "pix":

        chave = request.args.get("chave")
        nome = request.args.get("nome")
        cidade = request.args.get("cidade")
        valor = request.args.get("valor")

        if not chave:
            return "Chave vazia"

        dados = f"""
000201
26360014BR.GOV.BCB.PIX01{len(chave):02}{chave}
52040000
5303986
54{len(valor):02}{valor}
5802BR
59{len(nome):02}{nome}
60{len(cidade):02}{cidade}
62070503***
6304
"""


    else:
        return "Tipo inválido"


    img = qrcode.make(dados)

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
