# facebook scraper
from matplotlib.cbook import index_of
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import wget

# the dictionary with variations a word can occur
# can further be extended with more request_word per your needs
request_words = {"food dataset 1": ["Badajari Sangamaya", "Sri Lankan Food"]}
links = {"food dataset 1": set()}

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
# specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome(options=chrome_options)
# open the webpage
driver.get("http://www.facebook.com")

# target username
username = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']"))
)
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']"))
)

# enter username and password
username.clear()
username.send_keys("supungamlath@outlook.com")
password.clear()
password.send_keys("Sandali@2005")

# target the login button and click it
button = (
    WebDriverWait(driver, 2)
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    .click()
)

time.sleep(5)


def download(dish):

    print(dish + ": " + str(len(links[dish])) + "\n")
    # Enter the absolute path to the folder where this file is located
    os.chdir(r"E:\Projects\PythonProjects\facebook_image_dataset_scraper\images")
    path = os.getcwd()
    path = os.path.join(path, dish)
    # create the directory
    os.mkdir(path)
    counter = 0
    for image in links[dish]:
        save_as = os.path.join(path, str(counter) + ".jpg")
        wget.download(image, save_as)
        counter += 1

    # Enter the absolute path to the folder where this file is located
    os.chdir(r"E:\Projects\PythonProjects\facebook_image_dataset_scraper\images")


def scrape_posts(subrequests):
    """
    Scraping Posts

    """
    driver.get("https://www.facebook.com/search/posts?q=" + el)
    time.sleep(3)

    # scroll down
    # increase the range to sroll more
    # example: range(0,10) scrolls down more images
    for j in range(0, 5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    # target all the link elements on the page
    try:
        img = driver.find_elements(By.TAG_NAME, "img")

        for h in img:
            link = h.get_attribute("src")
            if str(link).startswith("https://scontent") or str(link).startswith(
                "https://external"
            ):
                links[subrequests].add(link)
    except Exception as e:
        print(e)


def scrape_photos(subrequests, el):
    """
    Scraping Photos

    """
    driver.get("https://www.facebook.com/search/photos?q=" + el)
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "See all").click()

    for k in range(0, 4):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    a_tags = driver.find_elements(By.TAG_NAME, "a")
    img_links = []
    for tag in a_tags:
        href = tag.get_attribute("href")
        if "photo" in href:
            img_links.append(href)

    for img_link in img_links:
        driver.get(img_link)
        time.sleep(1)

        imgs = driver.find_elements(By.TAG_NAME, "img")
        for img in imgs:
            identifier = img.get_attribute("data-visualcompletion")
            if identifier and identifier == "media-vc-image":
                links[subrequests].add(img.get_attribute("src"))


if __name__ == "__main__":
    for subrequests in request_words:
        for el in request_words[subrequests]:
            # scrape_posts(subrequests)
            scrape_photos(subrequests, el)

        download(subrequests)
print("\nDone!")
