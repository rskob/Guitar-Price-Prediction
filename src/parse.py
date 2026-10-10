from collect import (MuztorgParser, GuitarClubParser, DBWorker, MIRMParser, SkifMusicParser,
                    GuitarLavkaParser,  DominantaMusicParser,MusikRoomParser, MusicMarketParser, ShopAvallonParser,
                    LegatoParser, MirGuitarParser)
from selenium import webdriver
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent      # project/
DB_PATH = BASE_DIR / "data" / "raw" / "data.db"



opt = webdriver.ChromeOptions()
opt.add_argument("--headless=new")
opt.add_argument("--window-size=1920,1080")
opt.add_argument("--start-maximized")

driver = webdriver.Chrome(opt)
db =  DBWorker(DB_PATH)
mp = MuztorgParser(driver, db)
gp = GuitarClubParser(driver, db)
mrp = MIRMParser(driver, db)
mzp = SkifMusicParser(driver, db)
dp = DominantaMusicParser(driver, db)
mp = MusikRoomParser(driver, db)
mr = MusicMarketParser(driver, db)

parsers = [mp, gp, mrp, mzp, dp, mp, mr]

glp = GuitarLavkaParser(driver, db)
shp = ShopAvallonParser(driver, db)
mgp = MirGuitarParser(driver, db)
lgp = LegatoParser(driver, db)

try:
    for i in (lgp, ):
        res = i.run(["guitar"])
        print(res)
finally:
    driver.quit()
