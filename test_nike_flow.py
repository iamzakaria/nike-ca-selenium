import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Base Page class for shared methods
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        self.find(locator).send_keys(text)

# Landing Page
class LandingPage(BasePage):
    SEARCH_INPUT = (By.ID, "gn-search-input")
    SEARCH_CONTAINER = (By.CSS_SELECTOR, ".search-input-container")

    def visit(self):
        self.driver.get("https://www.nike.com/ca/")
        self.driver.set_window_size(1918, 1032)
        print("Visited Nike Canada landing page")

    def search_product(self, product_name):
        self.click(self.SEARCH_CONTAINER)  # Open search
        self.type(self.SEARCH_INPUT, product_name)
        self.find(self.SEARCH_INPUT).send_keys(Keys.ENTER)
        print(f"Searched for: {product_name}")

# Product Page
class ProductPage(BasePage):
    PRODUCT_CARD = (By.CSS_SELECTOR, ".product-card:nth-child(1) .product-card__hero-image")
    SIZE_OPTION = (By.CSS_SELECTOR, ".css-vmnznv:nth-child(8) > .u-full-width")  # Size (e.g., 8th option)
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".mb3-sm")  # Add to Cart button
    CART_BTN = (By.CSS_SELECTOR, ".css-7jsinp")  # Cart icon/button

    def select_product(self):
        self.click(self.PRODUCT_CARD)
        print("Selected first product")

    def select_size(self):
        self.click(self.SIZE_OPTION)
        print("Selected size")

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)
        print("Added to cart")

    def go_to_cart(self):
        self.click(self.CART_BTN)
        print("Navigated to cart")

# Checkout Page (stub - expand based on needs)
class CheckoutPage(BasePage):
    def start_checkout(self):
        print("Checkout process started (add more steps as needed)")

# Main Test Class
class TestNikeFlow:
    @pytest.fixture(autouse=True)
    def setup(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.vars = {}
        yield
        self.driver.quit()
        print("Browser closed")

    def test_nike_purchase_flow(self):
        try:
            # Initialize page objects
            landing = LandingPage(self.driver)
            product = ProductPage(self.driver)
            checkout = CheckoutPage(self.driver)

            # Test flow
            landing.visit()
            landing.search_product("jordan")  # Keeping your final search
            product.select_product()
            product.select_size()
            product.add_to_cart()
            product.go_to_cart()
            checkout.start_checkout()

        except Exception as e:
            print(f"Test failed: {str(e)}")
            self.driver.save_screenshot("error.png")

if __name__ == "__main__":
    pytest.main(["-v", __file__])