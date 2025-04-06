from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sys
sys.path.insert(0, 'c:/Users/shane/Documents/Uni Work/CyberLab AI')
from ai.personas import createEventInfo

driver = webdriver.Firefox()

def openContainer():
    driver.get('http://localhost:8080')

    # Wait for the page to load and for an element to be present
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'adminlogin')))
    except Exception as e:
        print(f"Error while loading page: {e}")
        driver.quit()

def signupAdmin(username, password):
    try:
        # Wait until the form elements are available
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'adminlogin'))
        )
        password_input = driver.find_element(By.ID, 'adminpass')
        signup_button = driver.find_element(By.CLASS_NAME, 'primary')

        # Enter the credentials and submit the form
        username_input.send_keys(username)
        password_input.send_keys(password)
        signup_button.click()

    except Exception as e:
        print(f"Error during signup: {e}")

def Login(username, password):
    try:
        # Wait until the form elements are available
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'user'))
        )
        password_input = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.TAG_NAME, 'button')

        # Enter the credentials and submit the form
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

    except Exception as e:
        print(f"Error during login: {e}")


def startupNewAcc(username, password):
    openContainer()
    signupAdmin(username, password)

    sleep(5)
    install_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.TAG_NAME, 'button'))
    )
    install_button.click()

    closeBtn = WebDriverWait(driver, 9999).until(
        EC.element_to_be_clickable((By.CLASS_NAME, '_button_close_1pqur_36'))
    )
    closeBtn.click()
    openCalendar()
    CreateEvent()
        


#Getting the quick links on header
def getHeaderLinks():
    elements = driver.find_elements(By.CLASS_NAME, "app-menu-entry__link")
    return elements

# Calendar Actions

#Open the calendar
def openCalendar():
    for link in getHeaderLinks():
        if link.get_attribute("title") == "Calendar":
            try:
                link.click()
            except Exception as e:
                print(f"Error during going into Calendar: {e}")
            break

def CreateEvent():
    # Click new event button
    new_event = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'new-event'))
    )
    new_event.click()

    # Find input areas for new event information
    EventTitleInput = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Event title"]'))
    )

    LocationInput = driver.find_element(By.TAG_NAME, "textarea")

    DescriptionInput = driver.find_element(By.CLASS_NAME, "textarea--description")

    # Insert inputs for new event information
    eventInfos = createEventInfo()

    EventTitleInput.send_keys(eventInfos[0])
    LocationInput.send_keys(eventInfos[1])
    DescriptionInput.send_keys(eventInfos[2])

    # Save Event Info
    save_button = driver.find_element(By.XPATH, '//button[contains(., "Save")]')
    save_button.click()




# Mail Actions

#File Actions
def openFiles():
    for link in getHeaderLinks():
        if link.get_attribute("title") == "Files":
            try:
                link.click()
            except Exception as e:
                print(f"Error during going into Files: {e}")
            break

def deleteFile():

    files = driver.find_elements(By.CLASS_NAME, "files-list__row")

    for link in files:
        if link.get_attribute("title") == "Files":
            try:
                link.click()
            except Exception as e:
                print(f"Error during going into Files: {e}")
            break