from requests_html import HTMLSession

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
