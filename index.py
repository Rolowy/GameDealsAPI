import threading
from flask import Flask, jsonify
from markupsafe import escape
from requests.sessions import session
from requests_html import HTMLSession



def loadRoute(app):
    @app.route("/")
    def index():
        print(jsonlist)
        return jsonify(keys=jsonlist)

class Session:
    def __init__(self, url) -> None:
        self.jsonlist  = []
        self.session = HTMLSession()
        print("Wywołanie sesji") 
   
        if self.get_page(url):
            print('Pobranie elementów zakończone sukcesem')
            print(self.get_Json())
        
    def get_Json(self):
        return self.jsonlist

    def get_page(self, url):
        r = self.session.get("https://gg.deals/deals/best-deals/" + url)
        print(f"Pobrano stronę | Status {r}")  
        
        if self.refresh(r):
            r.close()
            return True

    def refresh(self, r): 
        r.html.render(timeout=30)
        name = r.html.find('.ellipsis.title')
        price = r.html.find('.numeric')

        for i in range(len(name)):
            self.jsonlist.append({"name":name[i].text,
            "price":price[i].text.replace("zł", "zl")})

        print("Pobrano elementy")
        return True

    def close_session(self) -> None:
        session.close()
        print('Zamknięto sesję')

class FlaskApp:
    def __init__(self) -> None:
        app = Flask(__name__)
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        app.run(threaded=True)

        loadRoute(app)

        print("Flask App: Enabled")


if __name__ == "__main__":
    t = threading.Thread(target=FlaskApp)
    t2 = threading.Thread(target=Session, args=("?page=1",))
    
    t2.start()
    t2.join()
    t.start()
    t.join()

    


    # for i in range(1,6):
    #     Session("?page="+str(i))


