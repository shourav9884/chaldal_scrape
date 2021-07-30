import json

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,3600")

driver = webdriver.Chrome(options=options, executable_path=r"/Users/nati/Downloads/chromedriver")
url = "https://chaldal.com"
driver.get(url)

def has_child(xpath):
	elements = driver.find_elements(By.XPATH, xpath)
	if len(elements) == 0:
		return False
	return True

def get_child(parent_xpath):
	# elements = driver.find_elements(By.XPATH, xpath)
	print(parent_xpath)
	clickable_xpath = parent_xpath + "/div/a"
	clickable_element = driver.find_element(By.XPATH, clickable_xpath)
	# driver.execute_cdp_cmd("arguments[0].scrollIntoView(true);", clickable_element)
	clickable_element.click()
	time.sleep(1)
	elements = driver.find_elements(By.XPATH, parent_xpath+"/ul/li")
	cats = []
	i=1
	for element in elements:
		cat_dict = {
			"name": element.text,
			"id": element.get_attribute('data-cid')
		}
		a_element = driver.find_element(By.XPATH, parent_xpath + "/ul/li[{}]/div/a".format(i))
		cat_dict['slug'] = a_element.get_attribute('href').strip('/')
		if has_child(parent_xpath+"/ul/li[{}]/div/span".format(i)):
			cat_dict['has_child'] = True
			cat_dict['children'] = get_child(parent_xpath+"/ul/li[{}]".format(i))

		cats.append(cat_dict)
		i += 1
	return cats





time.sleep(3)
# elements(By.XPATH
cats = []
high_level_cats = driver.find_elements(By.XPATH, "//ul[@class='level-0']/li")
i=1
for cat in high_level_cats:
	cat_dict = {
		"name": cat.text,
		"id": cat.get_attribute('data-cid')
	}
	xpath = "//ul[contains(@class, 'level-0')]/li[{}]/div/span".format(i)
	if has_child(xpath):
		cat_dict['has_child'] = True
		cat_dict['children'] = get_child("//ul[contains(@class, 'level-0')]/li[{}]".format(i))

	a_element = driver.find_element(By.XPATH, "//ul[contains(@class, 'level-0')]/li[{}]/div/a".format(i))
	cat_dict['slug'] = a_element.get_attribute('href').strip('/')
	cats.append(cat_dict)
	i+=1


with open('jsons/categories.json', 'w+') as file:
	json.dump(cats, file, indent=4)
driver.close()


# //*[@id="page"]/div/div[3]/div/div[2]/div/div/div[2]/ul[2]/li[3]/div/a