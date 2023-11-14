import re
from typing import List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import By, WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.pronosoft.config import SITE_URL
from scraper.types.pronosoft import PronosoftEvent, PronosoftGame
from scraper.utils.cookies import remove_pronosoft_cookies_window

PATH = "lotofoot/resultats-et-rapports.php"
URL = f"{SITE_URL}/{PATH}"
WANTED_FORM_TYPES = [7,8,15]

def scrape_result_page(driver: WebDriver) -> List[PronosoftEvent]:
    """scraping the event result page from pronosoft

    Args:
        driver (WebDriver)

    Returns:
        List[PronosoftEvent]: Array of the scraped data
    """
    driver.get(URL)
    remove_pronosoft_cookies_window(driver)
    wait = WebDriverWait(driver, 10)  # Wait element that waits up to 10 seconds
    container_el = driver.find_element(By.CLASS_NAME, 'box-live')  # container that holds all titles and tables

    event_collapse_container_el = container_el.find_elements(By.XPATH, './div') # the divs that react to clicks
    event_collapse_container_el.pop()  # removing the last div, doesnt contain data
    data: List[PronosoftEvent] = []

    for event_container_el in event_collapse_container_el:
        try:
            event_data_el = event_container_el.find_element(By.CLASS_NAME, "live-match")  # the container of event table and title
            event_title = event_data_el.find_element(By.CSS_SELECTOR, "h2").text
            form_types: List[str] = get_form_types(event_title)  # getting all form types of the event
            needed_form_types = list(set(WANTED_FORM_TYPES) & set(form_types)) # getting form types that appear in the event and wanted
            if (len(needed_form_types) is not 0):
                games_els = event_data_el.find_elements(By.CSS_SELECTOR, "tr")  # a row of a game in the event
                date = get_event_date(games_els[0], wait) # getting the date of the first game, which is the date of the event
                
                games_data: List[PronosoftGame] = [] # making a list that will get all the games data
                for game_el in games_els[:max(needed_form_types)]: # looping through the games, only till the max form type which we will not need more rows than this
                    games_data.append(scrape_game_row_data(game_el))
                
                for form_type in needed_form_types:
                    cycle = get_cycle(event_title, form_type) # getting the cycle of the event
                    event = PronosoftEvent(cycle, date,form_type, games_data[:form_type]) # making an event object, getting only the sum of items that the form type demand
                    data.append(event)

        except Exception as err:
            print(err)

    return data


def get_event_date(game_row: WebElement, wait):
    """returns the event date

    Args:
        game_row (WebElement): a game row
        wait (WebDriverWait): wait object

    Returns:
        string: _description_
    """
    game_row.find_element(By.CLASS_NAME, 'score').click()
    try:
        date_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-date-utc]')))
        return date_span.get_attribute('data-date-utc')


    except TimeoutException:
        print("Element not found within 10 seconds.")


def get_cycle(game_title: str, form_type: str):
    """
    Args:
        game_title (string): title of the event, contains the cycle
        form_type (string): type of the form, e.g [Loto Foot 7]

    Returns:
        string: cycle of the game
    """
    escaped_string = re.escape(f"Loto Foot {form_type}")
    pattern = rf'{escaped_string} n°(\d+)'
    match = re.search(pattern, game_title)
    cycle = int(match.group(1))
    return cycle


def get_form_types(game_title: str):
    """get the form types of the event"""
    pattern = r'Loto Foot (\d+)'
    matches = re.finditer(pattern, game_title)
    form_types = []
    for match in matches:
        extracted_number = int(match.group(1))
        form_types.append(extracted_number)

    return form_types


def scrape_game_row_data(game: WebElement) -> PronosoftGame:
    """getting a game and returning the data needed for the game"""

    game_index = game.find_element(By.CLASS_NAME, "nr-m").text
    team1 = game.find_element(By.CLASS_NAME, "equipe1").text
    team2 = game.find_element(By.CLASS_NAME, "equipe2").text
    score = game.find_element(By.CLASS_NAME, "score-ft").text
    team1_score, team2_score = score.split('-')
    result = game.find_element(By.CLASS_NAME, "score-final").text
    game_data = PronosoftGame(game_index, team1, team2, team1_score, team2_score, result)
    return game_data