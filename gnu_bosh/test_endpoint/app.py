from flask import Flask, Response, request, jsonify

app = Flask(__name__)

debug = "<h2>Debug Start:</h2><br>"

def get_debug():
    global debug
    return debug

def append_debug(s):
    global debug
    debug += "<br>" + str(s)
    return debug

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return Response('<h1>Welcome to Bored API</h1>\nThis is the debug screen, if you are seeing this in production then don\'t.<br><br>\n' + get_debug(), 200)
    elif request.method == 'POST':
        append_debug(request.get_json(force=True))
        return Response('Post recieved at default endpoint, added to debug', 200)


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")