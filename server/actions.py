from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sys
import time
import requests
sys.path.insert(0, 'c:/Users/shane/Documents/Uni Work/CyberLab AI')
from ai.personas import createEventInfo, createChatInfo

driver = webdriver.Firefox()

def wait_for_http(url, timeout=60, interval=1):
    """
    Waits until the given URL is reachable via HTTP (returns a 2xx or 3xx status).
    """
    print(f"Waiting for {url} to become available...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code < 400:
                print(f"Ok {url} is up!")
                return True
        except requests.RequestException:
            pass  # just keep trying

        time.sleep(interval)

    print(f"Timeout: {url} didn't become available in {timeout} seconds.")
    return False

def openContainer():
    if wait_for_http("http://localhost:8080"):
        driver.get("http://localhost:8080")
    else:
        print("Exiting: web server inside container didn't start in time.")


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
        openContainer()
        print("Logging in...")
        # Wait until the form elements are available
        username_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'user'))
        )
        password_input = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        # Enter the credentials and submit the form
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        openTalk()
        startNewChat()

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

    DateTimeInputs = driver.find_elements(By.ID, 'date-time-picker-input')
  

    LocationInput = driver.find_element(By.TAG_NAME, "textarea")

    DescriptionInput = driver.find_element(By.CLASS_NAME, "textarea--description")

    # Insert inputs for new event information
    eventInfos = createEventInfo()

    EventTitleInput.send_keys(eventInfos[0])
    for i in range(4):
        DateTimeInputs[i].send_keys(eventInfos[1+i])
        sleep(1)

    LocationInput.send_keys(eventInfos[5])
    DescriptionInput.send_keys(eventInfos[6])

    # Save Event Info
    save_button = driver.find_element(By.XPATH, '//button[contains(., "Save")]')
    save_button.click()

    print("Event Created Successfully")


# Chat Actions
def openTalk():
    for link in getHeaderLinks():
        if link.get_attribute("title") == "Talk":
            try:
                link.click()
            except Exception as e:
                print(f"Error during going into Talk: {e}")
            break

def startNewChat():
    createChatBtn = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'chat-plus-icon'))
    )
    createChatBtn.click()

    createNewConv = driver.find_element(By.XPATH, '//button[contains(., "Create a new conversation")]')
    createNewConv.click()

    # Chat Info Inputs
    chatName = driver.find_element(By.XPATH, '//input[@placeholder="Enter a name for this conversation"]')
    chatDescription = driver.find_element(By.XPATH,'//textarea[@placeholder="Enter a description for this conversation"]')

    chatInfos = createChatInfo()

    chatName.send_keys(chatInfos[0])
    chatDescription.send_keys(chatInfos[1])

    createConvBtn = driver.find_element(By.XPATH, '//button[contains(., "Create conversation")]')
    createConvBtn.click()

# Send Message to a chat

def sendMsg():
    msgForm = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'new-message-form'))
    )
    msgForm.send_keys()

def getDetailsofChat():
    

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