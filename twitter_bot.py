import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from create_proxy import create_proxy_auth_extension
from dotenv import load_dotenv
import os


load_dotenv()

PROXYMESH_USERNAME = os.getenv("PROXYMESH_USERNAME")
PROXYMESH_PASSWORD = os.getenv("PROXYMESH_PASSWORD")
PROXYMESH_HOST = os.getenv("PROXYMESH_HOST")
PROXYMESH_PORT = os.getenv("PROXYMESH_PORT")
COMMAND_EXECUTOR = os.getenv("COMMAND_EXECUTOR", "http://127.0.0.1:4444/wd/hub")

IN_DEVELOPMENT = os.getenv("FLASK_ENV", "DEVELOPMENT") == "DEVELOPMENT"

TIME_OUT = 20
ACTIVATE_PROXY = False

if ACTIVATE_PROXY:
    create_proxy_auth_extension(
        proxy_host=PROXYMESH_HOST,
        proxy_port=PROXYMESH_PORT,
        proxy_username=PROXYMESH_USERNAME,
        proxy_password=PROXYMESH_PASSWORD
    )

proxy_url = f"http://{PROXYMESH_USERNAME}:{PROXYMESH_PASSWORD}@{PROXYMESH_HOST}:{PROXYMESH_PORT}"


class Twitterbot:

    def __init__(self, email, username, password):
        self.email = email
        self.password = password
        self.username = username
        # initializing chrome options
        chrome_options = Options()
        # Optional: Run Chrome in headless mode (no UI)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        if ACTIVATE_PROXY:
            chrome_options.add_extension("proxy_auth_plugin.zip")
        # chrome_options.add_argument(f'--proxy-server={proxy_url}')

        if not IN_DEVELOPMENT:
            chrome_options.add_argument("--no-sandbox")  # Required to run Chrome as root
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-setuid-sandbox")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.binary_location = "/usr/bin/google-chrome"
            chrome_options.add_argument('--ignore-ssl-errors=yes')
            chrome_options.add_argument('--ignore-certificate-errors')
            self.bot = webdriver.Remote(command_executor=COMMAND_EXECUTOR, options=chrome_options)
        else:
            self.bot = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def login(self):
        bot = self.bot
        # fetches the login page
        bot.get('https://x.com/i/flow/login')

        # Wait for the email input field to load (wait for it to be visible)
        WebDriverWait(bot, TIME_OUT).until(
            EC.visibility_of_element_located((By.NAME, "text"))
        )

        # Step 1: Enter email
        email = bot.find_element(By.NAME, "text")
        email.send_keys(self.email)
        email.send_keys(Keys.ENTER)

        # Wait for the next page to load (after submitting email)
        time.sleep(2)

        try:
            # Check if the username input field appears (if Twitter asks for username)
            WebDriverWait(bot, TIME_OUT).until(
                EC.visibility_of_element_located((By.NAME, "text"))
            )
            # If the username field appears, we enter the username
            username = bot.find_element(By.NAME, "text")
            username.send_keys(self.username)  # Or provide your username here
            username.send_keys(Keys.ENTER)
            print("Username asked, entered it.")
        except Exception as e:
            # If the username field does not appear, go to the password field
            print("Username not asked, proceeding with password.")
        finally:
            # Wait for the password input field to appear
            WebDriverWait(bot, TIME_OUT).until(
                EC.visibility_of_element_located((By.NAME, "password"))
            )

            # Step 2: Enter password
            password = bot.find_element(By.NAME, 'password')
            password.send_keys(self.password)
            password.send_keys(Keys.RETURN)
            print("Login successful")

        # Allow some time for the login process to complete
        time.sleep(3)

    def click_on_show_more_btn(self):
        try:
            # Wait for the "Show more" button to appear (it's located under the "What's Happening" section)
            show_more_button = WebDriverWait(self.bot, TIME_OUT).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/explore/tabs/for-you') and @role='link']"))
            )
            show_more_button.click()
            print("Clicked on the 'Show more' button.")
        except Exception as e:
            print("Failed to click 'Show more':", str(e))

        # Allow some time for the new content to load
        time.sleep(3)

    def get_top_trend_items(self):
        trend_li = []
        try:
            bot = self.bot
            # Locate all div elements with data-testid="trend" and role="link"
            trend_divs = bot.find_elements(
                By.XPATH,
                "//div[contains(@class, 'css-146c3p1') and contains(@class, 'r-bcqeeo') and contains(@class, 'r-1ttztb7') and contains(@class, 'r-qvutc0') and contains(@class, 'r-37j5jr') and contains(@class, 'r-a023e6') and contains(@class, 'r-rjixqe') and contains(@class, 'r-b88u0q') and contains(@class, 'r-1bymd8e')]")

            for div in trend_divs:
                # For each div, get the text of the span inside it
                span = div.find_element(By.XPATH, ".//span")
                trend_li.append(span.text)
        except Exception as e:
            print("Failed to extract trending text:", str(e))
        return trend_li

    def get_bot_ip(self):
        bot = self.bot
        bot.get("https://httpbin.org/ip")
        # Wait for the page to load
        time.sleep(2)
        # Extract the IP address from the page content
        ip_address = bot.find_element(By.TAG_NAME, "pre").text
        ip_dict = json.loads(ip_address)
        # Extract the IP address
        ip = ip_dict.get("origin")
        print(f"Current IP address used by Selenium: {ip}")
        return ip

    def close_bot(self):
        self.bot.close()

    def is_logged_in(self):
        try:
            # Wait for the element with `data-testid` attribute
            WebDriverWait(self.bot, TIME_OUT).until(
                EC.presence_of_element_located((By.XPATH, "//*[@data-testid='SideNav_AccountSwitcher_Button']"))
            )
            return True
        except:
            try:
                # Wait for the element with `aria-label` attribute
                WebDriverWait(self.bot, TIME_OUT).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Account menu']"))
                )
                return True
            except Exception as e:
                print(f"Login check failed: {e}")
                return False
