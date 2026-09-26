from parse import MuztorgParser, GuitarClubParser, DBWorker, MIRMParser, SkifMusicParser
from time import sleep
from parse.main_parser import Parser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
from selenium import webdriver


opt = webdriver.ChromeOptions()
opt.add_argument("--headless=new")
opt.add_argument("--window-size=1920,1080")
opt.add_argument("--start-maximized")
driver = webdriver.Chrome(opt)
db =  DBWorker("data.db")
mp = MuztorgParser(driver, db)
gp = GuitarClubParser(driver, db)
mrp = MIRMParser(driver, db)
mzp = SkifMusicParser(driver, db)

for i in (mzp, ):
    res = i.run(["guitar"])
    print(res)
