from selenium.webdriver.remote.webdriver import By


def remove_pronosoft_cookies_window(driver):
    """removes the cookies window from pronosoft site

    Args:
        driver (WebDriver)
    """
    try:
        driver.find_element(By.XPATH, "//button[text()='Tout accepter']").click()
    except Exception:
        print("couldnt find cookies window")
        
        
        
def remove_oddsportal_cookies_window(driver):
    """removes the cookies window from oddsportal site

    Args:
        driver (WebDriver)
    """
    try:
        driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
    except Exception:
        print("couldnt find cookies window")