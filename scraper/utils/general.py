def mark_element(driver,element,color='red'):
    """make element border red and bold"""
    driver.execute_script(f"arguments[0].style.border = '20px solid {color}';", element)
    
def scroll_to_element(driver,element):
    """scroll to an element"""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    