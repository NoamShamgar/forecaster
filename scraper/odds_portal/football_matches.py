
import datetime
import time
from typing import List

from selenium.webdriver.remote.webdriver import By, WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.odds_portal.config import SITE_URL
from scraper.types.pronosoft import PronosoftGame
from scraper.utils.general import mark_element
from utils.logger import Logger

PATH = "matches/football"
URL = f"{SITE_URL}/{PATH}"

def get_all_odds_portal_games(driver:WebDriver,date:datetime) -> List[WebElement]:
    """scraping all the games from odds_portal in a specific date

    Args:
        driver (WebDriver)
        date: (datetime)
    """
    driver.get(URL)
    wait = WebDriverWait(driver, 10)  # Wait element that waits up to 10 seconds

    games_container_el = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/main/div[2]/div[3]/div[4]/div[1]'))) # getting games list container
    clickable_games_els = games_container_el.find_elements(By.XPATH,"./*/a") # getting all games, items in a list that are clickables
    
    games = []
    index = 0
    while (True): # looping through all items, looking for the right game
        print('starting while loop, index:', index, "list size:", len(clickable_games_els))
        team_names_el = clickable_games_els[index].find_elements(By.CLASS_NAME,"participant-name") # getting teams names
        team1 = team_names_el[0].text
        team2 = team_names_el[1].text
        url = clickable_games_els[index].get_attribute("href")
        games.append({"team1":team1,"team2":team2,"url":url})
        
        index = index + 1
        
        if (index == len(clickable_games_els)): # reached end of list, trying to scroll down and fetch more items
            clickable_games_els = load_more_items(driver, len(clickable_games_els))
            if (clickable_games_els is False):
                break
    return games


def load_more_items(driver,last_len):
    """scrolling down to make oddsportal matches page to load more games,
        if more games have added, returning the new list, false otherwise
        max time wait = 10

    Args:
        driver (WebDriver)
        last_len (Int): length of the list before the new items loaded

    Returns:
        _type_: new list or False 
    """
    start_time = datetime.datetime.now()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    answer = None
    while (answer is None):
        games_container_el = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/main/div[2]/div[3]/div[4]/div[1]')
        clickable_games_els = games_container_el.find_elements(By.XPATH,"./*/a")
        if (len(clickable_games_els) > last_len):
            answer = clickable_games_els
    
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        if elapsed_time >= 10:
            answer = False
    return answer
    
    


