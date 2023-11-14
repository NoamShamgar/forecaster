import time

from selenium import webdriver

from scraper.odds_portal.football_matches import get_all_odds_portal_games
from scraper.pronosoft.results_page import scrape_result_page
from scraper.types.pronosoft import PronosoftGame
from scraper.utils.cookies import remove_oddsportal_cookies_window
from scraper.utils.general import mark_element, scroll_to_element

driver = webdriver.Chrome()


def start_scraping():
    events = scrape_result_page(driver)
    game_el = get_all_odds_portal_games(driver,'')
    time.sleep(100)