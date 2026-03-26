from flask import Flask, Response, request, jsonify

app = Flask(__name__)

debug = "Start:"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return Response('<h1>Welcome to Bored API</h1>\nThis is the debug screen, if you are seeing this in production then don\'t.<br><br>\n' + str(debug), 200)
    elif request.method == 'POST':
        debug += str(request.data) + "<br>"
        return Response('Post recieved at default endpoint, added to debug', 200)


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")