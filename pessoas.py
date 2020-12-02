from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import yaml

app = Flask(__name__)
config = yaml.load(open('database.yaml'))
client = MongoClient(config['uri'])
db = client['crud_pessoa']
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
        cpf = body['cpf']
        email = body['email']

        # db.users.insert_one({
        db['pessoa'].insert_one({
            "nome": nome,
            "cpf" : cpf,
            "email": email
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            'nome': nome,
            'cpf' : cpf,
            'email': email
        })
    
    # GET all data from database
    if request.method == 'GET':
        allData = db['pessoa'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            nome = data['nome']
            cpf = data['cpf']
            email = data['email']
            dataDict = {
                'id': str(id),
                'nome': nome,
                'cpf': cpf,
                'email' : email
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)

@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = db['pessoa'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        nome = data['nome']
        cpf = data['cpf']
        email = data['email']
        dataDict = {
            'id': str(id),
            'nome': nome,
            'cpf': cpf,
            'email' : email
        }
        print(dataDict)
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        db['pessoa'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        nome = body['nome']
        cpf = body['cpf']
        email = body['email']

        db['pessoa'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "nome":nome,
                    "cpf":cpf
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})

if __name__ == '__main__':
    app.debug = True
    app.run()
