from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from flask import Flask
from flask import jsonify
from apscheduler.schedulers.background import BackgroundScheduler

import time

class RunChrome:
    def __init__(self, refreshtime):
        self.mylist = {}
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get("https://gg.deals/deals/best-deals/")


        scheduler = BackgroundScheduler()
        scheduler.add_job(func=RunChrome.mylist, trigger="interval", seconds=refreshtime, args=[self])
        scheduler.start()

    def reload(self):
        print('Cleaning list')
        self.mylist = {}

        n = 0;

        
        def loadwebsite(self, x, n):
            print('Load website number %s' % x)
            url = "https://gg.deals/deals/best-deals/?page=" + str(x)
            print(url)
            self.driver.get(url)


            gamename = self.driver.find_elements_by_xpath("//div[@data-game-name]//a[@class='ellipsis title']")
            gameprice = self.driver.find_elements_by_xpath("//div[@data-game-name]//span[@class='numeric']")
            shop = self.driver.find_elements_by_xpath("//div[@data-game-name]")


            # print(len(gamename))
            # print(len(shop))

            i = 0
            
            for el in gamename:
                a = gameprice[i].text
                a = a.replace("ł", "l")

                shop_name = shop[i].get_attribute('data-shop-name')
                i+=1
                n+=1

                self.mylist.update({n:{"name":el.text,"values":a, "store":shop_name}})

            return n


            # tables = [el.text, a, shop_name]
            # self.mylist.append(tables)

        for x in range(1,26):
            n = loadwebsite(self, x, n)
            

        print('Finish')

    def mylist(self):
        RunChrome.reload(self)
        print('Loaded data..')

    def viewlist(self):
        return self.mylist

if __name__ == "__main__":
    runchrome = RunChrome(900)

    runchrome.reload()

    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    @app.route("/")
    def hello_world():
        mylist = runchrome.viewlist()

        
        # return jsonify(games=data)

        if len(mylist) > 0:
            return jsonify(games=mylist)
        else:
            return "Problem with loading RESTAPI."

    app.run(host='0.0.0.0', port=2500)