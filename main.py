from parse.muztrog.muztorg import MuztorgParser
from selenium import webdriver
from parse.muztrog.guitar import GuitarParser


driver = webdriver.Chrome()
mp = MuztorgParser(driver, {"guitar": GuitarParser(driver)})
mp.run(["guitar"])
