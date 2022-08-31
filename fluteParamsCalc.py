import os
#import chromedriver_autoinstaller

import sys
from subprocess import check_call, call

og_directory = ""
params_calculated = False
valid_res = True
model_built = False


def install(package):
    check_call([sys.executable, "-m", "pip", "install", package])


def InitSelenium():
    try:
        import selenium
        import webdriver_manager
    except ImportError:
        install("selenium")
        install("webdriver-manager")
    finally:
        import selenium
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import Select
        from selenium.webdriver.common.by import By
        import webdriver_manager
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager
        global Select, By, Keys
        try:
            path = ChromeDriverManager().install()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--profile-directory=Default')
            driver = webdriver.Chrome(executable_path=path, options=chrome_options)
            return driver
        except:
            path = GeckoDriverManager().install()
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--profile-directory=Default')
            firefox_options.add_argument('--no-sandbox')
            firefox_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Firefox(executable_path=path, options=firefox_options)
            return driver



def CreateFile(Holes_diameter,From_end,Bore, Total_length, Tube_OD):
  resFile = open("results.txt","w")
  global valid_res
  valid_res = True
  for i in range(len(Holes_diameter)):
    if Holes_diameter[i] == "NaN":
        valid_res = False
    resFile.write(Holes_diameter[i])
    if (i != len(Holes_diameter) - 1):
        resFile.write(", ")
  resFile.write("\n")
  for i in range(len(From_end)):
    if From_end[i] == "NaN":
        valid_res = False
    resFile.write(From_end[i])
    if (i != len(From_end) - 1):
        resFile.write(", ")
  resFile.write("\n")
  resFile.write(Bore)
  if Bore == "NaN":
        valid_res = False      
  resFile.write("\n")
  resFile.write(Total_length)
  if Total_length == "NaN":
        valid_res = False         
  resFile.write("\n")
  resFile.write(Tube_OD)
  if Tube_OD == "NaN":
        valid_res = False 
  resFile.close()


def CalcParms(driver, KeyNote, od, wt, od_picked, wt_picked):
    SelectInstrument = Select(driver.find_element(By.NAME, "design"))
    SelectInstrument.select_by_visible_text("Whistle")

    SelectNote = Select(driver.find_element(By.NAME, "key"))
    SelectNote.select_by_visible_text(KeyNote + ' ')
    if wt_picked:
        Wall_thickness = driver.find_element(By.NAME, "wall")
        Wall_thickness.send_keys(Keys.CONTROL + "a")
        Wall_thickness.send_keys(Keys.DELETE)
        Wall_thickness.send_keys(wt)
        Wall_thickness.send_keys(Keys.ENTER)
      
    Tube_OD = driver.find_element(By.NAME, "OuterDiam")
    if od_picked:
        Tube_OD.send_keys(Keys.CONTROL + "a")
        Tube_OD.send_keys(Keys.DELETE)
        Tube_OD.send_keys(od)
        Tube_OD.send_keys(Keys.ENTER)
    else:
        od = driver.find_element(By.NAME, "OuterDiam").get_attribute("value")
        
    Holes_diameter = []
    for i in range(1,7+1):
      Hole_diam = driver.find_element(By.NAME, f"diam{i}").get_attribute("value")
      Holes_diameter.append(Hole_diam)

    From_end = []
    for i in range(1,7+1):
      from_end = driver.find_element(By.NAME, f"result{i}").get_attribute("value")
      From_end.append(from_end)

    Bore = driver.find_element(By.NAME, "bore2").get_attribute("value")
    Total_length = driver.find_element(By.NAME, "resultLength").get_attribute("value")
    return Holes_diameter, From_end, Bore, Total_length, od


def start_calculation(KeyNote, od, wt, od_picked, wt_picked):
  #chromedriver_autoinstaller.install()
  html_path = os.path.abspath("./flutePage/Bracker Whistles & Flutes - Whistle and Flute Hole Calculator.html")
  driver = InitSelenium()
  driver.get(f"file:///{html_path}")
  Holes_diameter,From_end, Bore, Total_length, Tube_OD = CalcParms(driver, KeyNote, od, wt, od_picked, wt_picked)#, WallThickness,OutDiameter)
  CreateFile(Holes_diameter, From_end, Bore, Total_length, Tube_OD)
  global params_calculated
  params_calculated = True
  return


def build_the_model(blender_dir, file_name):
  global og_directory
  og_directory = os.getcwd()
  blender_code_dir = og_directory + "\whistle_flute.py"
  os.chdir(blender_dir)
  call(['blender', '-b','-P', blender_code_dir, og_directory, file_name])
  global model_built
  model_built = True
  return




