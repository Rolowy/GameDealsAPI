from flask import Flask, jsonify
from markupsafe import escape
from requests_html import HTMLSession

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

jsonlist  = []

def refresh(url):
    session = HTMLSession()
    r = session.get("https://gg.deals/deals/best-deals/" + url)

    r.html.render()
    name = r.html.find('.ellipsis.title')
    price = r.html.find('.numeric')

    for i in range(len(name)):
        jsonlist.append({"name":name[i].text,
        "price":price[i].text.replace("zł", "zl")})
    session.close()

for i in range(1,6):
    refresh("?page="+str(i))

@app.route("/")
def index():
    print(jsonlist)
    return jsonify(keys=jsonlist)