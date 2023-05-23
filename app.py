import os
import psycopg2
from apps.validador_cliente import ValidadorCliente
from apps.calculadora_energia import calculadora_de_energia
from dotenv import load_dotenv
from flask import *
from flask_cors import CORS


def conexao():
    url = os.getenv("DATABASE_URL")
    _conexao = psycopg2.connect(url)
    return _conexao


load_dotenv()

INSERT_WALLET = "INSERT INTO carteira (client_id,saldo) VALUES (%s,0)"
SELECT_WALLET = "SELECT * FROM carteira WHERE client_id = (%s)"
INSERT_CLIENT = "INSERT INTO cliente (name,email,idade,cpf,cep,senha) VALUES (%s,%s,%s,%s,%s,%s)"
SELECT_CLIENT = "SELECT * FROM cliente WHERE id = (%s)"
SELECT_ALL_CLIENT = "SELECT id,name FROM cliente ORDER BY id"
SELECT_550W_CHART = "SELECT month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12 " \
                    "FROM rendimento_painel WHERE model = %s"
app = Flask(__name__)
CORS(app)
connection = conexao()

@app.post("/api/create/acount")
def create_cliente():
    data = request.get_json()
    nome = data["nome"]
    email = data["email"]
    idade = data["idade"]
    cpf = data["cpf"]
    cep = data["cep"]
    senha = data["senha"]
    try:
        validador = ValidadorCliente(nome,email,idade,cpf,cep)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_CLIENT, (nome,email,idade,cpf,cep,senha))
        return "201"
    except Exception as e:
        print("An error occurred:", str(e))
        return str(e)


@app.route("/api/update/cliente", methods=["GET", "POST"])
def update_cliente():
    data = json.loads(request.data)
    nome = data["nome"]
    parametro = data["parametro"]
    valor_para_parametro = data["valParametro"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE cliente SET {parametro} = ({valor_para_parametro}) WHERE name = ('{nome}')")
    return "201"

@app.get("/api/get/client")
def get_cliente():
    id = request.args.get("id")
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(SELECT_CLIENT, (id,))
                cliente = cursor.fetchall()[0]
                compilado = {"nome": cliente[1],
                             "email": cliente[2],
                             "idade": cliente[3],
                             "cpf": cliente[4],
                             "cep": cliente[5]}
                response = make_response(compilado)
                response.mimetype = "text/plain"
                print(response.mimetype)
            except Exception as e:
                return "id de cliente invalido erro = " + str(e)
    return response

@app.get("/api/get/client/list")
def get_client_list():
    dicionario = {}
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_CLIENT)
            cliente = cursor.fetchall()
            index = 0
            for c in cliente:
                dados_novos = {index: {"id": c[0], "nome": c[1]}}
                dicionario.update(dados_novos)
                index += 1
            response = make_response(dicionario)
            response.mimetype = "text/plain"
            print(response.mimetype)
    return response

@app.get("/api/rendimento/painel")
def get_rendimemnto_painel():
    model = request.args.get("model")
    quantidade = request.args.get("qtd")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_550W_CHART, (model,))
            tabela_energia = cursor.fetchall()
            tabela_energia = tabela_energia[0]
    kwh = calculadora_de_energia(tabela_energia)
    return "KV/H " + str(int(kwh) * int(quantidade))

@app.post("/api/create/wallet")
def create_wallet():
    data = request.get_json()
    id = data["id"]
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_WALLET, (id,))
        return "201"
    except Exception as e:
        print("Carteira ja existente", str(e))
        return str(e)

@app.post("/api/wallet/exchange")
def wallet_exchange():
    data = request.get_json()
    id = data["id"]
    amount = data["amount"]
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_WALLET, (id,))
                dados = cursor.fetchall()
                saldo = dados[0][2]
                pos_tranferencia = saldo + amount
                cursor.execute(f"UPDATE carteira SET saldo = {pos_tranferencia} WHERE client_id = {id}")
        return "201"
    except Exception as e:
        print("Erro na transação ", str(e))
        return str(e)

@app.get("/api/get/wallet")
def get_wallet():
    id = request.args.get("id")
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(SELECT_WALLET, (id,))
                dados = cursor.fetchall()
                compilado = {"id": dados[0][1], "saldo": dados[0][2]}
                response = make_response(compilado)
                response.mimetype = "text/plain"
                print(response.mimetype)
            except Exception as e:
                return "id de cliente invalido erro = " + str(e)
    return response