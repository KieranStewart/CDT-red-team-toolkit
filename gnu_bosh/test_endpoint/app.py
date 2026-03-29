from flask import Flask, Response, request, jsonify

app = Flask(__name__)

import time
filename = f"data_save_{str(time.time())}.json"

data = []

def get_formatted_data():
    global data
    if len(data) != 0:
        out = "<table>\n<tr>\n"
        for key in data[0].keys():
            out += f"\t<th>{key}</th>\n"
        out += "</tr>\n"
        for json in data:
            out += "<tr>\n"
            for key in json.keys():
                out += f"\t<td>{json[key]}</td>\n"
            out += "</tr>\n"
        out += "</table>\n"
        return out
    else:
        return "No Data"
            

def add_data(s):
    global data
    data.append(s)
    with open(filename, "a") as save:
        save.write(f"\t{str(s)}\n")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return Response(f'<h1>Welcome to Red Team\'s Bashtrap Reciving Endpoint</h1>\nBoy I hope we replace this with something more official, works tho.<br>Here\'s what blue team is up to.<br>\n{get_formatted_data()}<br><br>ᓚᘏᗢ', 200)
    elif request.method == 'POST':
        print(str(request.get_json(force=True)))
        add_data(request.get_json(force=True))
        return Response('Post recieved at default endpoint, added to data', 200)


if __name__ == "__main__":
    with open(filename, "w") as save:
        save.write("[\n")
    app.run(port=8080, host="0.0.0.0")
    with open(filename, "a") as save:
        save.write("\n]")