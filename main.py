import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from lib import blockchain

first_node = '127.0.0.1:8080'
app = Flask(__name__)
CORS(app)
user =[]
voters=[]
chain = blockchain.BlockChain(first_node=first_node)

@app.route('/init')
def init():
    return requests.get('http://{first_node}/add-nodes/{host}/{port}'.format(first_node=first_node, host=host, port=port)).json()

@app.route('/candidates', methods=['GET'])
def candidates():

    candidates = {
        "1":"Shatrughn",
        "2":"Akash",
        "3":"Adinath",
        "4":"Adesh"
         
    }
    
    return jsonify(candidates)


@app.route('/new-vote', methods=['POST'])
def new_vote():
 
    try:
        values = request.json
        print(values)
        if values['voters_id'] == '' or values['vote'] == '':
            return 'Missing values', 400
        for i in voters:
            if i == values['voters_id']:
                return jsonify({'message': f'You voted before'})
        index = chain.new_vote(values['voters_id'], values['vote'])
        if index:
            voters.append(values["voters_id"])
            response = {'message': f'Your vote added to block'}
            return jsonify(response), 201
        else:
            response = {'message': f'You voted before'}
            return jsonify(response), 400
    except Exception as e:
            return jsonify(e)
           


@app.route('/add-nodes/<host>/<port>', methods=['GET'])
def add_nodes(host, port):
    req_url = host + ':' + port
    chain.nodes.add(req_url)
    response = {
        'nodes': list(chain.nodes),
        'length': len(chain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes', methods=['GET'])
def nodes():
    response = {
        'nodes': list(chain.nodes),
        'length': len(chain.nodes),
    }
    return jsonify(response), 201

@app.route('/current-votes', methods=['GET'])
def current_votes():
    #chain.update_current_votes()
    response = {
        'current_votes': chain.current_votes,
        'length': len(chain.current_votes),
    }
    return jsonify(response), 201



@app.route('/counts', methods=['GET'])
def count():
        
    Shatrughn=0
    Akash=0
    Adinath=0
    Adesh=0
    for i  in chain.current_votes:
        if i["vote"]=="Shatrughn":
            Shatrughn= Shatrughn+1
        if i["vote"]=="Akash":
            Akash= Akash+1
        if i["vote"]=="Adinath":
            Adinath= Adinath+1
        if i["vote"]=="Adesh":
            Adesh= Adesh+1
                   
    if Shatrughn > Akash:
        winners1 = {
            "winner":"Shatrughn",
            "votes":Shatrughn
        }
        
    else:
        winners1 ={
            "winner":"Akash",
            "votes":Akash
        }
            
    if Adinath > Adesh:
        winners2 = {
            "winner":"Adinath",
            "votes":Adinath
        }
    else:
        winners2 = {
            "winner":"Adesh",
            "votes":Adesh
        }
    if winners1["votes"]>winners2["votes"]:
        winners = winners1
    else:
        winners = winners2
        
    return jsonify(winners)

@app.route('/chain' , methods=['GET'])
def full_chain():
    #chain.resolve_conflicts()
    response = {
        'chain': chain.chain,
        'length': len(chain.chain), 
    }
    return jsonify(response), 200

@app.route('/update-block')
def update_block():
    chain.update_block()
    response = {'message': f'Everything is update'}
    return jsonify(response), 400

@app.route('/mine', methods=['GET'])
def mine():
    chain.update_block()
    if len(chain.current_votes) != 0:
        last_block = chain.last_block()
        last_proof = last_block['proof']
        proof = chain.pow(last_proof)
        
        pre_hash = chain.hash(last_block)
        block = chain.new_block(proof, pre_hash)
        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'votes': block['votes'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200
    else:
        response = {'message': f'Do not exist vote(s) for mining'}
        return jsonify(response), 200

@app.route('/count-votes',methods=['GET'] )
def count_votes():
   try:
        count = dict()
        chain.resolve_conflicts()
        len_chain = len(chain.chain)
        for i in range(len_chain):
            for j in range(len(chain.chain[i]['votes'])):
                for k in range(len(list(chain.chain[i]['votes'][j]['vote']))):
                    if list(chain.chain[i]['votes'][j]['vote'])[k] == '1':
                        if str(k) not in count.keys():
                            count[str(k)] = 1
                        else:
                            count[str(k)] += 1
                    
        return jsonify(count), 400
   except Exception as e:
       return jsonify(e)
 
  
 
@app.route("/login",methods=["POST"])
def login():
    values = request.json
    print(values)
    if values['username'] == '' or values['password'] == '':
        return 'Missing values', 400
    if values['username'] in user:
        return jsonify({"message":"login successful","code":"success"}), 200
    else:
        return jsonify({"message":"you are not a user","code":"not found"})
       
            
 
@app.route("/register",methods=["POST"])
def register():
        try:
            values = request.json
            print(values)
            if values['username'] == '' or values['password'] == '':
                return 'Missing values', 400
            else:
                user.append(values["username"])
                return jsonify("signup successful"), 200
        except Exception as e:
                return jsonify(e)
 
 

@app.route('/vote')
def get_votes():
    return jsonify(user), 200



if __name__ == '__main__':
    host = input('Enter your host : \n')
    port = input('Enter your port : \n')
    app.run(host=host, port=port)