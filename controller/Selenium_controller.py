
from app import app
from model.DataBase_model import save_json
from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from flask import  jsonify
import os
import time
import tempfile

def switch_window(driver, index, context="Unknown", box_name=""):
        if len(driver.window_handles) > index:
            driver.switch_to.window(driver.window_handles[index])
            print(f"🔀 Switched to window {index} ({box_name})")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from werkzeug.utils import secure_filename

def get_element(driver, locator_type, locator_value, timeout=10):
    """
    General function to get a web element.
    
    Args:
        driver: Selenium WebDriver instance.
        locator_type: String ("id", "xpath", "css", "name", "class", "tag").
        locator_value: The value of the locator.
        timeout: Wait time in seconds (default 10).
    
    Returns:
        WebElement if found, else "" (empty string).
    """
    locator_dict = {
        "id": By.ID,
        "xpath": By.XPATH,
        "css": By.CSS_SELECTOR,
        "name": By.NAME,
        "class": By.CLASS_NAME,
        "tag": By.TAG_NAME,
        "link_text": By.LINK_TEXT,
        "partial_link_text": By.PARTIAL_LINK_TEXT
    }

    try:
        by_type = locator_dict.get(locator_type.lower())
        if not by_type:
            raise ValueError(f"Unsupported locator type: {locator_type}")

        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by_type, locator_value))
        )
        return element.text
    except (TimeoutException, NoSuchElementException):
        return ""  # Return empty string if not found




def run_selenium(data):
    Main_data = {}
    temp_dir = tempfile.mkdtemp()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    chrome_options.add_argument("--remote-debugging-port=9222")  # Add this line

    driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # driver = webdriver.Chrome(service=service, options=chrome_options)

        print("test 1")
        driver.get("https://api-sabor.connectmls.com/sso/login")  # replace with your real URL
        time.sleep(2)
        print("test 2")
        # Fill the input box
        # input_box = driver.find_element(By.XPATH, "/html[1]/body[1]/section[1]/section[1]/div[1]/div[1]/form[1]/input[2]")
        input_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @name='username']"))
        )
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
        time.sleep(20)


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

        time.sleep(15)
        print("test 12")


        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "input-0"))
        )
        # Click the element
        element.click()

        print("test 12.1")

        input_box = driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[6]/div[1]/form[1]/md-autocomplete[1]/md-autocomplete-wrap[1]/input[1]")

        # Enter text into the input box
        # input_box.send_keys("1208 Creek Knoll")
        print("this is the address = = " , data["address"])
        input_box.send_keys(data["address"])

        time.sleep(10)
        print("test 12.22")

        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/md-virtual-repeat-container[1]/div[1]/div[2]/ul[1]/li[3]/md-autocomplete-parent-scope[1]/div[1]/div[2]/div[1]/div[1]"))
        )
        # Click the element
        element.click()
        print("test 12.2.1")
        time.sleep(10)

        # contry = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[4]/div[1]/div[1]/table[1]/tbody[1]/tr[7]/td[1]/span[1]"))
        # ) 
        contry = get_element(driver, "xpath", "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[4]/div[1]/div[1]/table[1]/tbody[1]/tr[7]/td[1]/span[1]")

        print("test 12.3")
        # Lot = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[4]/div[1]/div[1]/table[1]/tbody[1]/tr[5]/td[1]/span[1]"))
        # )
        Lot = get_element(driver, "xpath", "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[4]/div[1]/div[1]/table[1]/tbody[1]/tr[5]/td[1]/span[1]")

        print("test 12.4")
        # Block = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[4]/div[1]/div[1]/table[1]/tbody[1]/tr[4]/td[1]/span[1]"))
        # )
        Block = get_element(driver, "xpath", "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[4]/div[1]/div[1]/table[1]/tbody[1]/tr[4]/td[1]/span[1]")
        print("test 12.5")  
        # Subdivision_Legal_Name = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[4]/div[1]/div[1]/table[1]/tbody[1]/tr[9]/td[1]/span[1]"))
        # )
        Subdivision_Legal_Name = get_element(driver, "xpath", "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[4]/div[1]/div[1]/table[1]/tbody[1]/tr[9]/td[1]/span[1]")

        print("test 12.6")
        # address = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span[1]"))
        # )
        address = get_element(driver, "xpath", "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span[1]")
        print("test 12.7")  
        # Preferred_Title_Company = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[5]/div[1]/div[2]/table[1]/tbody[1]/tr[16]/td[1]/span[1]/report-field[1]/span[1]/a[1]"))
        # )
        Preferred_Title_Company = get_element(driver, "xpath", "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[5]/div[1]/div[2]/table[1]/tbody[1]/tr[16]/td[1]/span[1]/report-field[1]/span[1]/a[1]")

        print("test 12.8")
        # Listing_Associate_Email_Address = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[5]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/span[1]/report-field[4]/span[1]/a[1]"))
        # )
        Listing_Associate_Email_Address = get_element(driver, "xpath", "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[5]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/span[1]/report-field[4]/span[1]/a[1]")
        print("test 12.8.1")


        # Store current window handles before clicking
        current_windows = driver.window_handles
        print(f"Current windows: {len(current_windows)}")

        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/div[5]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div[4]/div[3]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/span[1]/report-field[1]/span[1]/a[1]"))
        )
        element.click()

        # Wait for new window to open
        WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > len(current_windows))
        print(f"New windows: {len(driver.window_handles)}")

        # Get the new window handle
        new_windows = [window for window in driver.window_handles if window not in current_windows]
        if new_windows:
            driver.switch_to.window(new_windows[0])
            print("Switched to new window")
        else:
            print("No new window found, trying to switch to last window")
            driver.switch_to.window(driver.window_handles[-1])

        print("test 12.9.1")  
        time.sleep(5)
        current_url = driver.current_url
        print("Current URL:", current_url)

        # Check if we need to switch to a frame
        try:
            # First try to find iframe by index 0
            driver.switch_to.frame(0)
            print("Switched to iframe by index")
        except:
            try:
                # If that fails, try to find iframe by tag name
                iframe = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "iframe"))
                )
                driver.switch_to.frame(iframe)
                print("Switched to iframe by tag name")
            except:
                print("No iframe found, continuing with main content")

        print("test 12.10")






        # Switch back to default content first
        driver.switch_to.default_content()
        print("Switched back to default content")

        # Now find and switch to the workspace iframe
        try:
            workspace_iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "workspace"))
            )
            driver.switch_to.frame(workspace_iframe)
            print("Switched to workspace iframe")
            
            # Wait for content to load
            time.sleep(3)
            
            # Extract all the broker information
            broker_info = {}
            
            # Office Information
            try:
                broker_info['office_name'] = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), 'Office Name:')]/following-sibling::td[1]"))
                ).text
            except:
                broker_info['office_name'] = "Not found"
            
            try:
                broker_info['office_type'] = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), 'Office Type:')]/following-sibling::td[1]"))
                ).text
            except:
                broker_info['office_type'] = "Not found"
            
            try:
                broker_info['office_id'] = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), 'Office ID:')]/following-sibling::td[1]"))
                ).text
            except:
                broker_info['office_id'] = "Not found"
            
            try:
                broker_info['email'] = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), 'Email Address:')]/following-sibling::td[1]"))
                ).text
            except:
                broker_info['email'] = "Not found"
            
            try:
                broker_info['website'] = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), 'Web Page:')]/following-sibling::td[1]"))
                ).text
            except:
                broker_info['website'] = "Not found"
            
            # Organization Address
            try:
                broker_info['street_address'] = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Organization Address')]/following-sibling::table//td[contains(text(), 'Street Address:')]/following-sibling::td[1]"))
                ).text
            except:
                broker_info['street_address'] = "Not found"
            
            try:
                broker_info['city_state_zip'] = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Organization Address')]/following-sibling::table//td[contains(text(), 'City, State, Zip:')]/following-sibling::td[1]"))
                ).text
            except:
                broker_info['city_state_zip'] = "Not found"
            
            # Phone
            try:
                broker_info['phone'] = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Phone')]/following-sibling::table//td[contains(text(), 'Phone:')]/following-sibling::td[1]"))
                ).text
            except:
                broker_info['phone'] = "Not found"
            
            # Print all extracted information
            print("Extracted Broker Information:")
            for key, value in broker_info.items():
                print(f"{key}: {value}")
            
            # Return the extracted data
            # return broker_info



            
        except Exception as e:
            # Return error information
            return {"status": "error", "message": str(e)}



            # "Listing_Broker_Firmname": broker_info

        print("test 13")
        print("Extracted contry:", contry)
        print("Extracted Text of Lot:", Lot)
        print("Extracted Text of Block:", Block)
        print("Extracted Text of Subdivision_Legal_Name:", Subdivision_Legal_Name)
        print("Extracted Text of address:", address)
        print("Extracted Text of Preferred_Title_Company:", Preferred_Title_Company)

        Main_data = {
            "contry": contry,
            "Lot": Lot,
            "Block": Block,
            "Subdivision_Legal_Name": Subdivision_Legal_Name,
            "address": address,
            "Preferred_Title_Company": Preferred_Title_Company,
            "Listing_Associate_Email_Address": Listing_Associate_Email_Address,
            "broker_info": broker_info,
            "csvFilepath":data['FilePath']
            }
        
        print( "This is the data", Main_data)
        doc_id = save_json(Main_data, "properties")
        print("Inserted ID:", doc_id)
        # print("Extracted Text of Listing_Associate_Email_Address:", Listing_Associate_Email_Address.text)
        # print("Extracted Text of Listing_Broker_Firmname:", broker_info)
        # # print("Extracted Text of Listing_Associate_Name:", Listing_Associate_Name.text)
        # # print("Extracted Text of Team_name:",Team_name.text)
        # # print("Extracted Text of Listing_Associate_Phone_Number:", Listing_Associate_Phone_Number.text)
        # # print("Extracted Text of Listing_Broker_Office_Addrress:", Listing_Broker_Office_Addrress.text)
        # # print("Extracted Text of Listing_Broke_Phone_Number:", Listing_Broke_Phone_Number.text)


        if driver is not None:
            driver.quit()
        # print("test 14")
        # time.sleep(5)
        # extracted_text = element.text
        # print("Extracted Text:", extracted_text)
        # return {"status": "success", "text": extracted_text}
        return {"status": "success", "message": str(e) , "data": Main_data}
    except Exception as e:
        return {"status": "error", "message": str(e) , "data": Main_data}

    finally:
        if driver is not None:
            driver.quit()
        # Clean up temporary directory
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)




# @app.route("/run", methods=["GET"])
# def run():
#     result = run_selenium()
#     return jsonify(result)


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# import time
# from flask import jsonify

# @app.route("/run", methods=["GET", "POST"])
# def run():

#     print("its working")
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return redirect(request.url)
        
#         file = request.files['file']
#         if file.filename == '':
#             return redirect(request.url)
        
#         if file and allowed_file(file.filename):
#             # Ensure CSVstore folder exists
#             folder = "CSVstore"
#             os.makedirs(folder, exist_ok=True)
            
#             # Secure the filename
#             original_name = secure_filename(file.filename)
#             name, ext = os.path.splitext(original_name)
            
#             # Add unique timestamp to filename
#             timestamp = time.strftime("%Y%m%d-%H%M%S")
#             unique_filename = f"{name}_{timestamp}{ext}"
            
#             # Save into CSVstore folder
#             filepath = os.path.join(folder, unique_filename)
#             file.save(filepath)
            
#             print(f"File saved as {filepath}")

#     start_time = time.time()  # record start
#     result = run_selenium()
#     end_time = time.time()    # record end
    
#     elapsed_time = end_time - start_time  # seconds
#     print(f"{elapsed_time:.2f} seconds")
#     print("This is the result:", result )
#     # attach elapsed time to your result
#     # if isinstance(result, dict):
#     #     result["elapsed_time"] = f"{elapsed_time:.2f} seconds"
    
#     return jsonify(result)




import os
import time
import csv
from flask import request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename

@app.route("/run", methods=['GET', 'POST'])
def run():
    print("its working")
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Ensure CSVstore folder exists
            folder = "CSVstore"
            os.makedirs(folder, exist_ok=True)
            
            # Secure and make unique filename
            original_name = secure_filename(file.filename)
            name, ext = os.path.splitext(original_name)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            unique_filename = f"{name}_{timestamp}{ext}"
            filepath = os.path.join(folder, unique_filename)
            
            # Save file
            file.save(filepath)
            print(f"✅ File saved as {filepath}")
            
            results = []
            
            # Read file row by row
            with open(filepath, newline='', encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    # Build JSON object with nested broker_info
                    data = {
                        "address": row.get("address", ""),
                        "FilePath":filepath
                        }
                    

                    print("this is the data = = =" , data)
                    
                    # Call run_selenium for each row
                    selenium_result = run_selenium(data)
                    
                    results.append({
                        "input": data,
                        "output": selenium_result
                    })
            
            return jsonify(results)
    
    return render_template('index.html')
