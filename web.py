from requests_html import HTMLSession

jsonlist = []

def refresh():
    session = HTMLSession()
    r = session.get("https://gg.deals/deals/best-deals/")

    r.html.render()
    name = r.html.find('.ellipsis.title')
    price = r.html.find('.numeric')

    for names in name:
        jsonlist.append({ "name":names.text })
    for prices in price:
        jsonlist.append({ "price":prices.text })
    
        # print(names.text)

    # for prices in price:
    #     print(prices.text)

   
    print(jsonlist)
# print(about.text)


refresh()
