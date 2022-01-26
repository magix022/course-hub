from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#FREEZE: pip list --format=freeze > requirements.txt  
#HELPERS

def delayed_send_keys(element, keys):
    for key in keys:
        element.send_keys(key)
        time.sleep(0.1)


def auth(username_txt, password_txt, email, passwd):
	count = 4
	trying = True
	while trying and count>0:
		try:
			username_txt.send_keys(email)
			password_txt.send_keys(passwd)
			trying = False
		except selenium.common.exceptions.UnexpectedAlertPresentException:
			count -= 1
			username_txt.clear()
			password_txt.clear()
			time.sleep(0.5)
	if trying: exit(-1)
	password_txt.send_keys(Keys.RETURN)

def get_dict(info, times):
	course = {}

	title = info.find_element(By.TAG_NAME, "caption").text
	title = title.split('-')
	course["title"] = title[0]
	course["subject"] = title[1]
	course["section"] = title[2]
	
	info = info.find_elements(By.TAG_NAME, 'td')
	course["term"] = info[0].text
	course["crn"] = info[1].text
	course["date"] = info[2].text
	course["instructor"] = info[3].text
	course["grading"] = info[4].text
	course["credits"] = info[5].text
	course["level"] = info[6].text
	course["campus"] = info[7].text

	info = times.find_elements(By.TAG_NAME, 'td')
	course["times"] = info[0].text
	course["day"] = info[1].text
	course["location"] = info[2].text
	course["dates"] = info[3].text
	course["type"] = info[4].text
	course["instructors"] = info[5].text

	unwanted = ".\n"
	for (key, value) in course.items():	
		for c in unwanted:
			value = value.replace(c,"")
		course[key] = value

	return course



# GET TO SCHEDULE
def find_weekly_schedule(driver):

	# BREACHED THE MAINFRAME
	time.sleep(1)
	Xpath = "/html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a"
	student_menu = driver.find_element(By.XPATH, Xpath)
	click(driver, student_menu)

	time.sleep(1)
	Xpath = "/html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a"
	registration_menu = driver.find_element(By.XPATH, Xpath)
	click(driver, registration_menu)

	time.sleep(1)
	Xpath = "/html/body/div[3]/table[1]/tbody/tr[5]/td[2]/a"
	weekly_schedule = driver.find_element(By.XPATH, Xpath)
	click(driver, weekly_schedule)

	time.sleep(1)
	Xpath = "/html/body/div[3]/form/input"
	submit_btn = driver.find_element(By.XPATH, Xpath)
	click(driver, submit_btn)


#JS click
def click(driver, elem):
	driver.execute_script("return arguments[0].click()",elem)


def get_schedule(email, passwd):
	#MAIN
	#driver = webdriver.Safari()
	# driver = webdriver.Chrome('../../assets/chromedriver')
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

	driver.get('https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin')
	time.sleep(4) #	wait for load
	Xpath = "//input[@id='mcg_un']"
	username_txt = driver.find_element(By.XPATH, Xpath)
	Xpath = "//input[@id='mcg_pw']"
	password_txt = driver.find_element(By.XPATH, Xpath)
	auth(username_txt, password_txt, email, passwd)
	find_weekly_schedule(driver)

	time.sleep(1)
	tables = driver.find_elements(By.CLASS_NAME, 'datadisplaytable')

	courses = []
	for i in range(0,len(tables),2):
		info = tables[i]
		times = tables[i+1]
		courses += [get_dict(info, times)]

	time.sleep(5)
	driver.close()
	return courses

