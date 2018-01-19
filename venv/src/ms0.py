from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# connect to another MongoDB database than the default one and on the same host
app.config['MONGO_DBNAME'] = 'football'
mongo = PyMongo(app, config_prefix='MONGO')

@app.route('/api')
def my_ms0():

        return jsonify(
            {'from ms0': 'Hello !'}
        )

@app.route('/foot')
def mongo_read():
    print(mongo.db)

    teams = mongo.db.Teams.find({})
    result = dict()
    for i, t in enumerate(teams):
        result[i] = t['nameUK']

    return jsonify(result)


if __name__ == '__main__':
    app.run()