from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

app = Flask(__name__)

def run_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    # Set the correct paths for Chromium and ChromeDriver
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    service = Service("/usr/bin/chromedriver")
    # driver = webdriver.Chrome(options=chrome_options)
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print("test 1")
        driver.get("https://api-sabor.connectmls.com/sso/login")  # replace with your real URL
        time.sleep(2)
        print("test 2")
        # Fill the input box
        input_box = driver.find_element(By.XPATH, "/html[1]/body[1]/section[1]/section[1]/div[1]/div[1]/form[1]/input[2]")
        input_box.send_keys("817205")


        time.sleep(5)
        print("test 3")

        input_box = driver.find_element(By.XPATH, "/html[1]/body[1]/section[1]/section[1]/div[1]/div[1]/form[1]/input[3]")

        # Enter text into the input box
        input_box.send_keys("TitoBabi$123")

        print("test 4")
        # Click the button
        button = driver.find_element(By.XPATH, "/html[1]/body[1]/section[1]/section[1]/div[1]/div[1]/form[1]/button[1]")
        button.click()

        time.sleep(15)

        print("test 5")

        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[2]/md-card[1]/md-card-actions[1]/a[2]/span[1]/span[1]"))
        )
        # Click the element
        element.click()


        print("test 6")
        time.sleep(5)

        print("test 7")
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))  # wait until 2 tabs exist
        driver.switch_to.window(driver.window_handles[-1])  # move to the newest tab
        print("Switched to new tab:", driver.title)


        current_url = driver.current_url
        print("Current URL:", current_url)

        print("test 8")
        time.sleep(15)


        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[2]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]"))
        )
        # Click the element
        element.click()
        time.sleep(2)


        print("test 9")

        input_box = driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[2]/div[1]/div[1]/div[1]/input[1]")

        # Enter text into the input box
        input_box.send_keys("jev@trustwcrealty.com")

        print("test 10")

        time.sleep(5)
        # Wait to see the result


        input_box = driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[3]/div[1]/div[1]/div[1]/input[1]")

        # Enter text into the input box
        input_box.send_keys("WholeSaleRE$987")

        print("test 11")

        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[2]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[2]/button[1]"))
        )
        # Click the element
        element.click()

        time.sleep(10)
        print("test 12")



        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[1]/div[2]"))
        )

        print("test 13")
        # Get the text content
        text_value = element.text
        print("Extracted Text:", text_value)

        print("test 14")
        time.sleep(5)
        extracted_text = element.text
        print("Extracted Text:", extracted_text)
        return {"status": "success", "text": extracted_text}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        driver.quit()


@app.route("/run", methods=["GET"])
def run():
    result = run_selenium()
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
