import json

from flask import Flask, Response, request, jsonify

app = Flask(__name__)

import time
filename = f"data_save_{str(time.time())}.json"

data = {}

def get_formatted_data():
    global data
    if len(data.keys()) == 0:
        return "No Hosts"
    super_out = ""
    for host in data.keys():
        super_out += f"<br><h3>Host:{host}</h3>"
        if len(data[host]) != 0:
            out = "<table>\n<tr>\n"
            for key in data[host][0].keys():
                out += f"\t<th>{key}</th>\n"
            out += "</tr>\n"
            for json in data[host]:
                out += "<tr>\n"
                for key in json.keys():
                    out += f"\t<td>{json[key]}</td>\n"
                out += "</tr>\n"
            out += "</table>\n"
            super_out += out

        else:
            super_out += "No Data"
    return super_out
            

def add_data(s):
    global data
    if "hostname" in s.keys():
        src_hostname = s["hostname"]
        if not src_hostname in data.keys():
            data[src_hostname] = []
        data[src_hostname].append(s)
    with open(filename, "a") as save:
        save.write(f"\t{str(s)},\n")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return Response(jsonify(data), 200)
    elif request.method == 'POST':
        add_data(request.get_json(force=True))
        return Response('Post recieved at default endpoint, added to data', 200)
@app.route('/view', methods=['GET'])
def get_view():
    return Response(f"""<!DOCTYPE html>\n
        <html>\n
        <head>\n
        <style>\n
        * {{\n
        font-family: 'Courier New', monospace;\n
        }}\n
        table {{\n
        font-family: arial, sans-serif;\n
        border-collapse: collapse;\n
        width: 100%;\n
        }}\n
\n
        td, th {{\n
        border: 1px solid #dddddd;\n
        text-align: left;\n
        padding: 8px;\n
        }}\n
\n
        tr:nth-child(even) {{\n
        background-color: #dddddd;\n
        }}\n
        </style>\n
        </head>\n
        <body>\n
        <h1>Welcome to Red Team\'s Bashtrap Reciving Endpoint</h1>\n
        <br>Here\'s what blue team is up to.<br>\n
        {get_formatted_data()}\n
        <br><br>ᓚᘏᗢ\n
        </body>\n
        </html>\n
        """, 200)


if __name__ == "__main__":
    with open(filename, "w") as save:
        save.write("[\n")
    app.run(port=8080, host="0.0.0.0")
    with open(filename, "a") as save:
        save.write("\n]")
    with open(f"sorted_data_save_{str(time.time())}.json", "w") as final_save:
        final_save.write(str(json.dumps(data)))