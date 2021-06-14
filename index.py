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

    # for names in name:
    #     jsonlist.append({ "name":names.text })

    # for prices in price:
    #     for lists in jsonlist:
    #         lists.update({ "price": prices.text.replace("zł", "zl")})
    
        # print(names.text)

    # for prices in price:
    #     print(prices.text)

    session.close()
    # print(jsonlist)
# print(about.text)

for i in range(1,6):
    refresh("?page="+str(i))


@app.route("/")
def index():
    print(jsonlist)
    return jsonify(keys=jsonlist)