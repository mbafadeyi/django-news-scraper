import datetime

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .models import NewsItem


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
    try:
        # find all the elements with this class -> crayons-story
        article_elements = browser.find_elements(By.CLASS_NAME, "crayons-story")

        for article in article_elements:
            # try get the anchor tag and href

            item_link = article.find_element(
                By.CLASS_NAME, "crayons-story__hidden-navigation-link"
            )
            news_item_link = item_link.get_attribute("href")

            # try get title
            title_result = article.find_element(By.TAG_NAME, "h3")
            news_item_title = title_result.text

            # try get timestamp

            # no articles older than 2 years
            two_years_ago = datetime.date.today() - relativedelta(years=2)

            timestamp_result = article.find_element(By.TAG_NAME, "time")
            news_item_time = timestamp_result.text

            # convert the news_item_time into python date object
            if "'" in news_item_time:
                # parse the year
                new_item_date = datetime.datetime.strptime(
                    news_item_time, "%b %d '%y"
                ).date()
            else:
                # the year is the current year
                new_item_date = datetime.datetime.strptime(news_item_time, "%b %d")
                today = datetime.date.today()
                new_item_date = new_item_date.replace(year=today.year).date()

            if new_item_date > two_years_ago:
                NewsItem.objects.get_or_create(
                    title=news_item_title,
                    link=news_item_link,
                    source="dev.to",
                    publish_date=new_item_date,
                )

    except:  # noqa
        pass
