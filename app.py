import os
import psycopg2
from dotenv import load_dotenv
from flask import *
from flask_cors import CORS


load_dotenv()

INSERT_CLIENT = "INSERT INTO cliente (name,email,idade,cpf,cep,senha) VALUES (%s,%s,%s,%s,%s,%s)"
SELECT_CLIENT = "SELECT * FROM cliente WHERE id = (%s)"
SELECT_ALL_TEXT = "SELECT * FROM texts ORDER BY text_id"
app = Flask(__name__)
CORS(app)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post("/api/create/acount")
def create_cliente():
    data = request.get_json()
    nome = data["nome"]
    email = data["email"]
    idade = data["idade"]
    cpf = data["cpf"]
    cep = data["cep"]
    senha = data["senha"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CLIENT, (nome,email,idade,cpf,cep,senha))
    return "201"


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

    return response

