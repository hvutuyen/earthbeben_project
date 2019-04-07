from flask import Flask, url_for, render_template, send_file
import erdbebenanalyse

app = Flask(__name__)

@app.route("/disclaimer", methods=["GET", "POST"])
def disclaimer():
    return render_template("disclaimer.html")

@app.route("/", methods=["GET", "POST"]) # Karte
def index():
    erdbebenanalyse.mapping() # funktion das erdbebenanalyse.py ausfuehren
    return render_template("index.html")

@app.route("/was-sind-erdbeben", methods=["GET", "POST"]) # Was sind Erdbeben
def index1():
    return render_template("index1.html")

@app.route("/die-staerksten-erdbeben", methods=["GET", "POST"]) # Die staerksten Erdbeben
def index2():
    return render_template("index2.html")

@app.route("/quellen", methods=["GET", "POST"])
def quellen():
    return render_template("quellen.html")

@app.route("/impressum", methods=["GET", "POST"])
def impressum():
    return render_template("impressum.html")

@app.route("/templates/karte.html")
def show_map():
    return send_file("templates/karte.html")


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(port = 1337, debug = True, threaded= True) # debug bei deploy auf False setzen