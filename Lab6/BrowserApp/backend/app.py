from flask import Flask
from flask import request, jsonify
from SearchEngine import SearchEngine

app = Flask(__name__)
search_engine = SearchEngine("150k", 150000)


@app.route("/search_query", methods=['POST'])
def search_query():
    if "search_query" not in request.json:
        return "Wrong request", 400

    result = search_engine.query(request.json["search_query"])
    print(result)

    return jsonify({"result": result}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
