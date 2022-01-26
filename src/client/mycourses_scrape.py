from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datefinder
from nltk import tokenize
import nltk

nltk.download("punkt")

def click(elem):
	driver.execute_script("return arguments[0].click()",elem)

def getShadowRoot(host):
    shadowRoot = driver.execute_script("return arguments[0].shadowRoot", host)
    return shadowRoot

def mycourses_auth(email, passwd):
	Xpath = '//*[@id="link1"]'
	mcgill_btn = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	click(mcgill_btn)

	Xpath = '//*[@id="i0116"]'
	email_txt = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	email_txt.send_keys(email)

	Xpath = '//*[@id="idSIButton9"]'
	next_btn = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	click(next_btn)

	Xpath = '//*[@id="passwordInput"]'
	passwd_txt = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	passwd_txt.send_keys(passwd)

	Xpath = '//*[@id="submitButton"]'
	submit_btn = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	click(submit_btn)

	#AUTHENTIFICATOR!!!!
	Xpath = '//*[@id="idDiv_SAOTCAS_Title"]'
	authentificator = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	print("AUTHENTIFICATOR")
	Xpath = '//*[@id="idChkBx_SAOTCAS_TD"]'
	chkbx = driver.find_element(By.XPATH, Xpath)
	click(chkbx)
	Xpath = '//*[@id="lightbox"]/div[3]/div/div[2]/div/div[1]'
	element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	print("HERE!")
	Xpath = '//*[@id="idBtn_Back"]'
	no_btn = driver.find_element(By.XPATH, Xpath)
	click(no_btn)

def get_to_course(subject):
	time.sleep(7)
	Xpath = '/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/d2l-expand-collapse-content/div/d2l-my-courses'
	root = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath))).shadow_root
	root = root.find_element(By.CSS_SELECTOR, 'd2l-my-courses-container').shadow_root #CHROME DRIVER SHADOWROOTS ONLY WORK WITH CSS
	root = root.find_element(By.CSS_SELECTOR, 'd2l-tabs') 
	root = root.find_element(By.CSS_SELECTOR, 'd2l-tab-panel')
	root = root.find_element(By.CSS_SELECTOR, 'd2l-my-courses-content').shadow_root 
	root = root.find_element(By.CSS_SELECTOR, 'd2l-my-courses-card-grid').shadow_root 
	tabs = root.find_elements(By.CSS_SELECTOR, 'd2l-enrollment-card')

	cards = [tab.shadow_root.find_element(By.CSS_SELECTOR, 'd2l-card') for tab in tabs]
	card = (card for card in cards if subject in card.get_attribute('text')).__next__()
	
	click(card.shadow_root.find_element(By.CSS_SELECTOR, 'div > a'))

def get_to_content():
	Xpath = '/html/body/header/nav/d2l-navigation/d2l-navigation-main-footer/div/div/div[1]/a'
	root = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	click(root)

def get_announcements(subject):
	get_to_course(subject)
	#CLICK ALL ANNOUCEMENTS
	Xpath = '/html/body/div[2]/div[2]/div/div/div[1]/div/d2l-expand-collapse-content/div/div[1]/div/a'
	root = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	click(root)

	Xpath = '/html/body/div[2]/div/div[3]/div/div/div[2]/form/div/div/d2l-table-wrapper/table'
	table = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	elems = table.find_elements(By.CSS_SELECTOR, 'tr')

	announcements = []
	#FIRST IS TITLE -- SKIP
	for i in range(1,len(elems),2):
		announcement = {}
		announcement["subject"] = subject
		head = elems[i]
		title = head.find_element(By.CSS_SELECTOR, 'a').text
		date = head.find_element(By.CSS_SELECTOR, 'label').text
		body = elems[i+1]
		body_elems = body.find_elements(By.CSS_SELECTOR,"*")
		text = ""
		for e in body_elems:
			try: 
				text += e.text
			except:
				pass
		announcement['title'] = title
		announcement['date'] = date
		announcement['text'] = text

		announcements += [announcement]

	return announcements

def parse_events(announcements):

	keywords = ["quiz","exam","midterm","final","test","assignment","paper","project","homework","pset","problem set","hw","ass","webwork","lab","workshop"]

	events = []

	for anc in announcements:
		text = anc["text"]
		text = tokenize.sent_tokenize(text) #SPlITS INTO SENTENCES USING NLP
		for sent in text:
			sent = sent.lower()
			words = tokenize.word_tokenize(sent)
			union = list(set(keywords) & set(words))
			if union:
				event = {}
				event['subject'] = anc['subject']
				typ = ""
				[typ := typ + " " + key for key in union]
				typ = typ[1:]
				dates = datefinder.find_dates(sent)
				dates = [date for date in dates]
				if dates:
					date = dates[0]
				else:
					date = None
				#TREAT OTHER CASES
				event['type'] = typ
				event['deadline'] = date
				event['length'] = 0
				event['title'] = anc['title']
				event['date'] = datefinder.find_dates(anc['date'])
				#event['text'] = anc['text']

				events += [event]

	return events


def get_events(subjects, email, passwd):
	try: 
		start_mycourses(email,passwd)
	except:
		print("LOGIN FAILED")
		return None

	events = []
	for subject in subjects:
		announcements = get_announcements(subject)
		events += parse_events(announcements)
		back_to_home()

	mycourses_close()
	return events
	


def start_mycourses(email, passwd):
	global driver
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	driver.get('https://mycourses2.mcgill.ca/d2l/loginh/?target=%2fd2l%2fhome')
	try:
		mycourses_auth(email,passwd)
	except selenium.common.exceptions.TimeoutException:
		print("Authentification failed")

def back_to_home():
	driver.get('https://mycourses2.mcgill.ca/d2l/home')


def mycourses_close():
	driver.close()

