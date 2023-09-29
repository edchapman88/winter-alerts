from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def handler(event=None, context=None):
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(options=options, service=service)
    driver.implicitly_wait(10)
    driver.get("https://www.ukclimbing.com/logbook/crags/ben_nevis-16877/#ascents")

    WebDriverWait(driver, 10, poll_frequency=2).until(EC.visibility_of(driver.find_element(By.XPATH, '//*[@id="ascents"]/div[2]/table/tbody')))
    table = driver.find_element(By.XPATH, '//*[@id="ascents"]/div[2]/table/tbody')
    data = []
    for row in table.find_elements(By.TAG_NAME, 'tr'):
        row_data = {}
        for (id,cell) in zip(['route','grade','style','climber','date'],row.find_elements(By.TAG_NAME, 'td')):
            row_data[id] = cell.text.replace("\n"," ")
        data.append(row_data)

    return {"scrape":data}
