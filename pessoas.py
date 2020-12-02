from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import yaml

app = Flask(__name__)
config = yaml.load(open('database.yaml'))
client = MongoClient(config['uri'])
# db = client.lin_flask
db = client['lin_flask']
CORS(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        nome = body['nome']
        idade = body['idade']

        # db.users.insert_one({
        db['users'].insert_one({
            "nome":nome,
            "idade": idade
        })
        return jsonify({
            'status': 'Cadastrado ',
            'nome': nome,
            'idade': idade
        })
    
   
    if request.method == 'GET':
        allData = db['users'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            nome = data['nome']
            idade = data['idade']
            dataDict = {
                'id': str(id),
                'nome': name,
                'idade': idade
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)

@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = db['users'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        nome = data['nome']
        idade = data['idade']
        dataDict = {
            'id': str(id),
            'nome': nome,
            'idade': idade
        }
        print(dataDict)
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        db['users'].delete_many({'_id': ObjectId(id)})
        print('\n # Removido # \n')
        return jsonify({'status': 'Data id: ' + id + ' Removido'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        nome = body['nome']
        idade = body['idade']

        db['users'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "nome":nome,
                    "idade":idade
                }
            }
        )

        print('\n # Alerado com sucesso # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})

if __name__ == '__main__':
    app.debug = True
    app.run()
