from typing import List
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from flask import Flask
from flask import jsonify
from apscheduler.schedulers.background import BackgroundScheduler

import time

class RunChrome:
    def __init__(self) -> None:
        self.mylist = []
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        scheduler = BackgroundScheduler()
        scheduler.add_job(func=RunChrome.mylist, trigger="interval", seconds=60, args=[self])
        scheduler.start()

    def reload(self):
        print('Cleaning list')
        self.mylist.clear()

        print('Load website')
        self.driver.get("https://gg.deals/deals/best-deals/")

        
        
        gamename = self.driver.find_elements_by_xpath("//div[@data-game-name]//a[@class='ellipsis title']")
        gameprice = self.driver.find_elements_by_xpath("//div[@data-game-name]//span[@class='numeric']")
        
        n = 0;
        for el in gamename:
            a = gameprice[n].text
            a = a.replace("ł", "l")
            
            tables = [el.text, a]
            self.mylist.append(tables)
            
            n+=1

        print('Finish')

    def mylist(self):
        RunChrome.reload(self)
        print('Loaded data..')

    def viewlist(self) -> List:
        return self.mylist

if __name__ == "__main__":
    runchrome = RunChrome()

    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    @app.route("/")
    def hello_world():
        mylist = runchrome.viewlist()

        if len(mylist) > 0:
            return jsonify(games=mylist)
        else:
            return "Problem with loading RESTAPI."

    app.run()