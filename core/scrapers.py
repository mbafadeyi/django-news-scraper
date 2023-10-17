from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scrape(URL):
    options = webdriver.ChromeOptions()
    options.add_argument(" - incognito")
    options.add_argument("start-maximized")

    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--user-data-dir=~/.config/google-chrome")

    browser = webdriver.Chrome(options=options)

    browser.get(URL)

    timeout = 10

    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//article[@class='crayons-story']")
            )
        )
    except TimeoutException:
        print("Timed out waiting for page to load.")
        browser.quit()
    # find all the elements with this class -> crayons-story
    article_elements = browser.find_elements(By.CLASS_NAME, "crayons-story")

    for article in article_elements:
        # try get the anchor tag and href

        result = article.find_element(
            By.CLASS_NAME, "crayons-story__hidden-navigation-link"
        )
        print(result.get_attribute("href"))

        # try get title
        title_result = article.find_element(By.TAG_NAME, "h3")
        news_item_title = title_result.text
        print(news_item_title)

        # try get time
        timestamp_result = article.find_element(By.TAG_NAME, "time")
        news_item_time = timestamp_result.text
        print(news_item_time)
