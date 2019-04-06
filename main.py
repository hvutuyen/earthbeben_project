from flask import Flask, url_for, render_template
import erdbebenanalyse

app = Flask(__name__)

@app.route("/disclaimer", methods=["GET", "POST"])
def disclaimer():
    return render_template("disclaimer.html")

@app.route("/", methods=["GET", "POST"]) # Karte
def index():
    erdbebenanalyse.mapping() # funktion das erdbebenanalyse.py ausfuehren

    iframe = url_for('static', filename="Karte.html")
    #iframe= "/Users/hoangvutuyen/Desktop/earthbeben/static/Karte.html"
    return render_template("index.html", iframe=iframe)

@app.route("/was-sind-erdbeben", methods=["GET", "POST"]) # Was sind Erdbeben
def index1():
    return render_template("index1.html")

@app.route("/was-sind-erdbeben", methods=["POST"]) 
def reply1():
    return render_template("index1.html")

@app.route("/die-staerksten-erdbeben", methods=["GET", "POST"]) # Die staerksten Erdbeben
def index2():
    return render_template("index2.html")

@app.route("/index2", methods=["POST"])
def reply2():
    return render_template("index2.html")

@app.route("/datenschutz", methods=["GET", "POST"])
def datenschutz():
    return render_template("datenschutz.html")

@app.route("/impressum", methods=["GET", "POST"])
def impressum():
    return render_template("impressum.html")


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(port = 1337, debug = True, threaded= True) # debug bei deploy auf False setzen