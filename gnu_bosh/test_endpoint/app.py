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
        return Response(f"""<!DOCTYPE html>
                        <html>
                        <head>
                        <style>
                        table {{
                        font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                        }}

                        td, th {{
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                        }}

                        tr:nth-child(even) {{
                        background-color: #dddddd;
                        }}
                        </style>
                        </head>
                        <body>
                        <h1>Welcome to Red Team\'s Bashtrap Reciving Endpoint</h1>\n
                        Boy I hope we replace this with something more official, works tho.<br>Here\'s what blue team is up to.<br>
                        {get_formatted_data()}
                        <br><br>ᓚᘏᗢ
                        </body>
                        </html>
                        """, 200)
    elif request.method == 'POST':
        add_data(request.get_json(force=True))
        return Response('Post recieved at default endpoint, added to data', 200)


if __name__ == "__main__":
    with open(filename, "w") as save:
        save.write("[\n")
    app.run(port=8080, host="0.0.0.0")
    with open(filename, "a") as save:
        save.write("\n]")