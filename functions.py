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


#  def click_element(element):
#     if element:
#         try:
#             element.click()
#             print("Elemente tıklandı.")
#         except Exception as e:
#             print(f"Hata oluştu: {e}")
#     else:
#         print("Element bulunamadı.")

# def set_text(element, text):
#     if element:
#         try:
#             element.send_keys(text)
#             print(f"'{text}' metni belirtilen alana yazıldı.")
#         except Exception as e:
#             print(f"Hata oluştu: {e}")
#     else:
#         print("Element bulunamadı.")

#############Selenium Compenents (application)###################



def get_request(method, url, data, headers):
    return rq.request(method=method, url=url, data=data, headers=headers).json()


def yaz(text):
    return print(text)


def read_excel(excel_path):
    return pd.read_excel(excel_path, engine='openpyxl')


def get_row(df, row):
    return df.iloc[row]


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


driver_test=open_chrome_browser()
navigate_to_url(driver_test,"https://www.youtube.com")
give_time(5)


xpath = "//input[@id='search']"  # Belirli bir giriş alanını tanımlayın (örneğin, ID'si ile)
second_xpath ="//button[@id='search-icon-legacy']"

text_to_set = "RPA"  # Girmek istediğiniz metni belirleyin
find_and_set_text(driver_test,xpath,text_to_set)
find_and_click_element(driver_test,second_xpath)



#close_browser(driver_test)
