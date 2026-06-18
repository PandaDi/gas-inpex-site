from flask import Flask, render_template

app = Flask(__name__)

# Force serving static files correctly for Frozen-Flask
app.config["FREEZER_DESTINATION"] = "build"
app.config["FREEZER_RELATIVE_URLS"] = False

BASE_URL = "https://pandadi.github.io/gas-inpex-site"


@app.route("/")
def index():
    return render_template("index.html", url=BASE_URL + "/")


@app.route("/index.html")
def index_html():
    return render_template("index.html", url=BASE_URL + "/")


@app.route("/services.html")
def services():
    return render_template("services.html", url=BASE_URL + "/services.html")


@app.route("/contacts.html")
def contacts():
    return render_template("contacts.html", url=BASE_URL + "/contacts.html")


@app.route("/objects.html")
def objects():
    return render_template("objects.html", url=BASE_URL + "/objects.html")


@app.route("/partners.html")
def partners():
    return render_template("partners.html", url=BASE_URL + "/partners.html")


@app.route("/certificates.html")
def certificates():
    return render_template(
        "certificates.html", url=BASE_URL + "/certificates.html"
    )


@app.route("/service-detail.html")
def service_detail():
    return render_template(
        "service-detail.html", url=BASE_URL + "/service-detail.html"
    )


@app.route("/catalog-boilers.html")
def catalog_boilers():
    return render_template(
        "catalog-boilers.html", url=BASE_URL + "/catalog-boilers.html"
    )


@app.route("/catalog-industrial.html")
def catalog_industrial():
    return render_template(
        "catalog-industrial.html",
        url=BASE_URL + "/catalog-industrial.html",
    )


@app.route("/catalog-kipia.html")
def catalog_kipia():
    return render_template(
        "catalog-kipia.html", url=BASE_URL + "/catalog-kipia.html"
    )


@app.route("/catalog-smarthome.html")
def catalog_smarthome():
    return render_template(
        "catalog-smarthome.html", url=BASE_URL + "/catalog-smarthome.html"
    )


if __name__ == "__main__":
    app.run(debug=True, port=3000)
