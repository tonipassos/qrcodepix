from flask import Flask, render_template, request, send_file, redirect
import mercadopago
import qrcode
from io import BytesIO
import os

app = Flask(__name__)

token = os.environ.get("MP_TOKEN")

sdk = mercadopago.SDK(token)


# ---------------- HOME ----------------

@app.route("/")
def home():

    link = request.args.get("link", "")
    chave = request.args.get("chave", "")
    nome = request.args.get("nome", "")
    tipo = request.args.get("tipo", "")
    msg = request.args.get("msg", "")

    return render_template(
        "index.html",
        link=link,
        chave=chave,
        nome=nome,
        tipo=tipo,
        msg=msg
    )


# ---------------- PAGAR ----------------

@app.route("/pagar", methods=["POST"])
def pagar():

    tipo = request.form.get("tipo")

    link = request.form.get("link")
    chave = request.form.get("chave")
    nome = request.form.get("nome")

    if not tipo:
        return redirect("/?msg=Escolha o tipo")

    if tipo == "site":

        if not link:
            return redirect(
                f"/?msg=Digite o link&tipo={tipo}&link={link}"
            )

        dados = f"tipo=site&link={link}"


    elif tipo == "pix":

        if not chave:
            return redirect(
                f"/?msg=Digite a chave&tipo={tipo}&chave={chave}&nome={nome}"
            )

        if not nome:
            return redirect(
                f"/?msg=Digite o nome&tipo={tipo}&chave={chave}&nome={nome}"
            )

        dados = f"tipo=pix&chave={chave}&nome={nome}"


    else:
        return redirect("/?msg=Tipo invalido")


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
            "failure": "https://qrcodepix-zscq.onrender.com/erro",
            "pending": "https://qrcodepix-zscq.onrender.com/cancelar"
        },

        "auto_return": "approved"
    }

    preference = sdk.preference().create(preference_data)

    return redirect(preference["response"]["init_point"])


# ---------------- SUCESSO ----------------

@app.route("/sucesso")
def sucesso():

    tipo = request.args.get("tipo")
    link = request.args.get("link")
    chave = request.args.get("chave")
    nome = request.args.get("nome")

    return redirect(
        f"/gerar?tipo={tipo}&link={link}&chave={chave}&nome={nome}"
    )


# ---------------- GERAR ----------------

@app.route("/gerar")
def gerar():

    tipo = request.args.get("tipo")

    if tipo == "site":

        link = request.args.get("link")

        if not link:
            return redirect("/?msg=Link vazio")

        dados = link


    elif tipo == "pix":

        chave = request.args.get("chave")
        nome = request.args.get("nome")

        if not chave:
            return redirect("/?msg=Chave vazia")

        if not nome:
            return redirect("/?msg=Nome vazio")

        dados = f"PIX:{chave}:{nome}"


    else:
        return redirect("/?msg=Tipo invalido")


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


# ---------------- ERRO ----------------

@app.route("/erro")
def erro():
    return render_template("erro.html")


@app.route("/cancelar")
def cancelar():
    return render_template("cancelar.html")


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
