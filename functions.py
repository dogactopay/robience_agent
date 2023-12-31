import os
import pandas as pd
import requests as rq
from IPython import embed
import ansible_runner
import re
import json
import yaml
from selenium import webdriver
import chromedriver_autoinstaller
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import requests


#############Selenium Compenents (application)###################
def open_chrome_browser():
    try:
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome()
        print("Chrome tarayıcı açıldıı.")
        return driver
    except Exception as e:
        print(f"Hata oluştu: {e}")

def navigate_to_url(driver, url):
    try:
        driver.get(url)
        print(f"Belirtilen URL'ye gidildi: {url}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def close_browser(driver):
    try:
        driver.quit()
        print("Tarayıcı kapatıldı.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def find_element_by_xpath(driver, xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
        return element
    except NoSuchElementException:
        print(f"Element bulunamadı: {xpath}")
        return None

def find_elements_by_xpath(driver, xpath):
    try:
        elements = driver.find_elements(By.XPATH, xpath)
        return elements
    except NoSuchElementException:
        print(f"Elementler bulunamadı: {xpath}")
        return []

def give_time(sleep_time):
    try:
        print("sleeping...")
        time.sleep(int(sleep_time))
        print("sleep over.")
    except Exception as e:
        print(f"Hata oluştu: {e}")


def find_and_set_text(driver, xpath, text):
    try:
        element = find_element_by_xpath(driver, xpath)
        element.send_keys(text)
        print(f"'{text}' metni belirtilen alana yazıldı: {xpath}")
    except NoSuchElementException:
        print(f"Element bulunamadı: {xpath}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def find_and_click_element(driver, xpath):
    try:
        element = find_element_by_xpath(driver, xpath)
        element.click()
        print(f"Elemente tıklandı: {xpath}")
    except NoSuchElementException:
        print(f"Element bulunamadı: {xpath}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def find_and_get_text(driver,xpath):
    try:
        element = find_element_by_xpath(driver,xpath)
        text_element = element.text
        return text_element
        print(f"Element Text alındı: {xpath}")
    except NoSuchElementException:
        print(f"Element bulunamadı: {xpath}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def get_element_count(driver, xpath):
    element_count = None
    try:
        elements = find_elements_by_xpath(driver, xpath)
        element_count = len(elements)
        print(f"Element sayısı: {element_count}")
    except NoSuchElementException:
        print(f"Element bulunamadı: {xpath}")
    except Exception as e:
        print(f"Hata oluştu: {e}")
    
    return element_count





#############Selenium Compenents (application)###################

#######Dataset Compenents########

def write_dataset_to_excel(file_path,dataframe):
    dataframe.to_excel(file_path, index=False, engine='openpyxl')

def read_excel_to_dataset(file_path):
    return pd.read_excel(file_path, engine='openpyxl')

def create_empty_dataset():
    return pd.DataFrame()

def add_column(dataframe, column_name):
    dataframe[column_name] = None
    return dataframe

# def add_empty_rows(dataframe,row_number=1):
#     new_row = pd.Series([None] * len(dataframe.columns), index=dataframe.columns)
#     updated_dataframe = pd.concat([dataframe, new_row.to_frame().T], ignore_index=True)
#     return updated_dataframe

def add_empty_rows(dataframe,row_number=1):
    # Create an empty row with NaN values
    empty_row = pd.DataFrame({col: [pd.NA] for col in dataframe.columns})
    
    # Append the empty row to the DataFrame
    dataframe = dataframe._append(empty_row, ignore_index=True)
    
    return dataframe
    
def set_data(dataframe, row_number, col_number, data_value):
    dataframe.iat[int(row_number), int(col_number)] = data_value

    



#######Dataset Compenents########

#######alert  Compenents########
def create_alert(customer, alert_content,status):
    url = "http://185.185.82.233/alert/new/"  # API endpoint URL
    data = {
        "customer": customer,
        "alert_content": alert_content,
        "status": status 
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:  
            print("Alert başarıyla oluşturuldu.")
        else:
            print(f"Hata kodu: {response.status_code}")
            print(f"Hata mesajı: {response.text}")
    except Exception as e:
        print(f"Hata oluştu: {e}")
#######alert  Compenents########

def get_request(method, url, data, headers):
    return rq.request(method=method, url=url, data=data, headers=headers).json()


def yaz(text):
    return print(text)


def get_row(df, row):
    return df.iloc[row]

#######Ansible runner########
def run_ansible_playbook(script, os, host_ip, username, password):

    my_inventory = {"windows": {
        "web_server": {
            "hosts": {
                host_ip: {

                    "ansible_user": username,
                    "ansible_winrm_password": password,
                    "ansible_password": password,
                    "ansible_host": host_ip,
                    "ansible_winrm_server_cert_validation": "ignore",
                    "ansible_port": 5985,
                    "ansible_winrm_scheme": "http",
                    "ansible_connection": "remote",
                    "ansible_connection": "winrm",
                    "AllowUnencrypted": True,
                    "ansible_winrm_transport": "ntlm",
                },
            }
        },
    }, "Windows": {
        "web_server": {
            "hosts": {
                host_ip: {

                    "ansible_user": username,
                    "ansible_winrm_password": password,
                    "ansible_password": password,
                    "ansible_host": host_ip,
                    "ansible_winrm_server_cert_validation": "ignore",
                    "ansible_port": 5985,
                    "ansible_winrm_scheme": "http",
                    "ansible_connection": "remote",
                    "ansible_connection": "winrm",
                    "AllowUnencrypted": True,
                    "ansible_winrm_transport": "ntlm",
                },
            }
        },
    }, "linux": {
        "web_server": {
            "hosts": {
                host_ip: {
                    "ansible_connection": "ssh",
                    "ansible_user": username,
                    "ansible_sudo_pass": password,
                    "ansible_password": password,
                    "ansible_host": host_ip
                },
            }
        },
    }}

    playbook = json.loads(script.replace(
        "localhost", host_ip))

    r = ansible_runner.run(playbook=playbook, inventory=my_inventory[os], envvars={
                           "ANSIBLE_SHOW_CUSTOM_STATS": True, "ANSIBLE_STDOUT_CALLBACK": "json"})
    

    string_encode = r.stdout.read().encode("ascii", "ignore")
    string_decode = string_encode.decode()
    result = (string_decode.split(
        "TASK [Gathering Facts]")[-1].split("PLAY RECAP")[0].replace("*", "").replace("", ""))

    alph = re.sub(r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))', '', result)
    res = re.sub(r'\n', ' ', alph)

    try:

        output = r.stdout.read()
        #embed()
        if "error" not in output.lower():

            indexOfOutPut = output.find("{", 0)

            jsonOutput = json.loads(output[indexOfOutPut:])
            key0 = list(jsonOutput['stats'].keys())[0]

            if jsonOutput['stats'][key0]['failures'] > 0 or jsonOutput['stats'][key0]['unreachable'] > 0:
                msg = ",".join([",".join([k['hosts'][key0]['msg']for k in z['tasks']]) for z in json.loads(res)['plays']])
                raise Exception(msg)
            else:
                return "SUCCESS"
        else:
            raise Exception(output)
    except Exception as e:
        print(e)
        raise Exception(e)

#######Ansible runner########



# give_time(5)
# hotel_data=[]
# driver_test=open_chrome_browser()
# navigate_to_url(driver_test,"https://www.trivago.com.tr/tr/srl/otel-adana-t%C3%BCrkiye?search=200-15236;dr-20231106-20231107;pr-3525-2147483647")
# give_time(3)

# xpath_names= "//li[@data-testid='accommodation-list-element']//button[@data-testid='item-name']//span[@itemprop='name']"
# xpath_prices = "//li[@data-testid='accommodation-list-element']//p[@data-testid='recommended-price']"

# hotel_names_elements=find_elements_by_xpath(driver_test,xpath_names)
# hotel_prices_elements = find_elements_by_xpath(driver_test, xpath_prices)

# for name_element, price_element in zip(hotel_names_elements, hotel_prices_elements):
#     hotel_name = name_element.text
#     hotel_price = price_element.text
#     hotel_data.append([hotel_name, hotel_price])

# df = pd.DataFrame(hotel_data, columns=["Otel Adı", "Fiyat"])
# print(df)

# write_dataset_to_excel("/Users/alioktemediz/Desktop/robeniceAgent/hotel.xlsx",df)

#close_browser(driver_test)

#create_alert(1,"some problem",0)


# (//li[@data-testid='accommodation-list-element']//button[@data-testid='item-name']//span[@itemprop='name'])[{counter}]
# (//li[@data-testid='accommodation-list-element']//p[@data-testid='recommended-price'])[{counter}]

# //li[@data-testid='accommodation-list-element']//button[@data-testid='item-name']//span[@itemprop='name']
# //li[@data-testid='accommodation-list-element']//p[@data-testid='recommended-price']
#set_data(dataframe=updated_dataframe,row_number=counter,col_number=f'0',data_value=hotel_name)