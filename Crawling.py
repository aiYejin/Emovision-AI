from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
import requests

# 디렉토리 생성 함수
def create_directory(directory):
    """
    주어진 디렉토리가 존재하지 않을 경우 디렉토리를 생성합니다.
    :param directory: 생성할 디렉토리 경로
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: 디렉토리 생성에 실패했습니다.")

# 이미지 다운로드 함수
def download_image(url, filepath):
    """
    주어진 URL에서 이미지를 다운로드하여 주어진 파일 경로에 저장합니다.
    :param url: 이미지의 URL
    :param filepath: 저장할 파일 경로
    """
    response = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(response.content)

# 이미지 크롤링 함수
def crawling_img(name):
    """
    인물의 이름을 입력받아 Google 이미지에서 해당 인물의 사진을 크롤링합니다.
    :param name: 인물의 이름
    """
    driver = webdriver.Chrome()
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        elem.send_keys(name)
        elem.send_keys(Keys.RETURN)

        SCROLL_PAUSE_TIME = 1
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    driver.find_element_by_css_selector(".mye4qd").click()
                except:
                    break
            last_height = new_height

        imgs = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
        dir = "./data/" + name
        create_directory(dir)
        count = 0
        for img in imgs:
            try:
                imgUrl = img.get_attribute("src")
                if imgUrl is None:
                    imgUrl = img.get_attribute("data-src")
                if imgUrl:
                    print("이미지 URL:", imgUrl)
                    path = "./data/" + name + "/"
                    create_directory(path)
                    file_path = path + str(count) + ".jpg"  # 저장할 파일 경로
                    print("파일 경로:", file_path)
                    download_image(imgUrl, file_path)
                    count += 1
                    if count >= 400: # 크롤링할 수가 끝나면 break
                        break
            except:
                pass

    finally:
        driver.close()


persons = []  # 원하는 인물 목록
for person in persons:
    crawling_img(person)
