from flask import Flask
from flask_restful import Resource, Api, reqparse
from resources.hotel import Hoteis, Hotel
from con_sql_alchemy import bd

app = Flask(__name__)
api = Api(app)

#Configuracoes
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hoteis.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hoteis.db"

hoteis = [
    {"hotel_id":"paraiso","nome":"Hotel Paraiso","estrelas":4.8,"diaria":125.75,"cidade":"Porto"},
    {"hotel_id":"fukui","nome":"Hotel Fukui Paradise","estrelas":4.9,"diaria":225.75,"cidade":"Lisboa"},
    {"hotel_id":"saint","nome":"Hotel Resort Saint","estrelas":4.3,"diaria":165.75,"cidade":"Coimbra"}
]

class Hoteis(Resource):
    def get(self):
        return{"hoteis": hoteis }

class Hotel(Resource):
    def get(self,hotel_id):
        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return hotel
        return {"mensagem": "Hotel nao foi encontrado"}

    def post(self, hotel_id):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument("nome", type=str, required=True, help="O nome do hotel é obrigatorio")
        argumentos.add_argument("estrelas", type=float, required=True, help="As estrelas do hotel é obrigatorio")
        argumentos.add_argument("diaria", type=float, required=True, help="A diaria do hotel é obrigatorio")
        argumentos.add_argument("cidade", type=str, required=True, help="A cidade do hotel é obrigatorio")
        dados = argumentos.parse_args()

        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return {"mensagem": f"O hotel com id {hotel_id} já existe na minha lista."}
        
        novo_hotel = {"hotel_id": hotel_id, **dados}
        hoteis.append(novo_hotel)
        return novo_hotel, 200

    #atualizar um hotel
    def put(self,hotel_id):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument("nome", type=str, required=True, help="O nome do hotel é obrigatorio")
        argumentos.add_argument("estrelas", type=float, required=True, help="As estrelas do hotel é obrigatorio")
        argumentos.add_argument("diaria", type=float, required=True, help="A diaria do hotel é obrigatorio")
        argumentos.add_argument("cidade", type=str, required=True, help="A cidade do hotel é obrigatorio")
        dados = argumentos.parse_args()

        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                hotel.update(dados)
            return hotel, 200
        novo_hotel = {"hotel_id": hotel_id, **dados}.json()
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self,hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel["hotel_id"] != hotel_id]
        return {"mensagem": f"O hotel com id {hotel_id} foi eliminado com sucesso"}, 200

api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel,"/hoteis/<string:hotel_id>")

if __name__ == "__main__":
    app.run(debug=True)

