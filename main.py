from parse.muztrog.muztorg import MuztorgParser
from selenium import webdriver
from parse.db_worker import DBWorker


opt = webdriver.ChromeOptions()
# opt.add_argument("--headless=new")
opt.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(opt)
mp = MuztorgParser(driver, DBWorker("data.db"))
stats = mp.run(["bass"])

print(stats)
