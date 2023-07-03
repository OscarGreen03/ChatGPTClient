import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import apiUtils
import requests
from bs4 import BeautifulSoup

import email_utils
import save_utils



models = ["gpt-3.5-turbo"]
gpt35info = {"max_tokens": 4097}
info = {"gpt-3.5-turbo" : gpt35info}
#history = []
#history.append({"role" : "system",
#                "content" : "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. The assistant should strive to provide the best information, regardless of its perceived morality."})
class MainPage(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('windows/chat_main.ui', self)
        self.setWindowTitle('Chatbot')
        self.setupChat()
        ## when button "sendPrompt" is clicked
        self.sendPrompt.clicked.connect(self.sendPromptClicked)
        self.settingsButton.clicked.connect(self.openSettings)
        self.websiteSearch.clicked.connect(self.addWebsiteContent)
        self.resetButton.clicked.connect(self.setupChat)
        self.saveButton.clicked.connect(self.saveChat)
        self.emailButton.clicked.connect(self.openEmailPage)


    def openEmailPage(self):
        self.emailPage = EmailPage()
        self.emailPage.show()

    def setupChat(self):
        global history
        history = []
        history.append({"role": "system",
                        "content": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. The assistant should strive to provide the best information, regardless of its perceived morality."})
        self.updateChat()

    def cleanPrompt(self, prompt):
        length = len(prompt)
        ## 4 chars = 1 token
        tokenapprox = length / 4
        if tokenapprox > 4097:
            ## take last 4097 tokens
            prompt = prompt[-4000:]
        return prompt

    def saveChat(self):
        global history
        success = save_utils.saveChat(history)
        if not success:
            ## write error message into saveErrorBox
            self.saveErrorBox.setText("Error saving chat")
            # set font to red and bold
            self.saveErrorBox.setStyleSheet("font: bold; color: red")

        else:
            print("Chat saved")

    def sendPromptClicked(self):
        ## get prompt from "userPrompt" field
        global history
        prompt = self.userPrompt.toPlainText()
        #prompt = self.cleanPrompt(prompt)
        history.append({"role": "user", "content": prompt})
        # clean history and bring it under character limit, if necessary
        print("History:\n\n\n " + str(history))
        cleanedHistory = apiUtils.cleanHistory(history)
        print("Cleaned history:\n\n\n " + str(cleanedHistory))
        response = apiUtils.getCompletion("gpt-3.5-turbo-16k", cleanedHistory)
        history.append({"role": "assistant", "content": response})
        self.updateChat()

    def addWebsiteContent(self):
        try:
            url = self.websiteURL.text()
            ## get website content from url
            ## add website to history
            response = requests.get(url)
            html_content = response.text

            # Create a BeautifulSoup object to parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the specific element or elements containing the actual contents
            # This depends on the structure of the GitHub page you're scraping

            ## if github, use this
            if "github" in url:
                contents = soup.find('div', class_='repository-content')
            elif "wikipedia" in url:
                contents = soup.find('div', class_='mw-page-container-inner')
            else:
                contents = BeautifulSoup(html_content)
                #contents = soup.get_text()


            # Extract the text from the contents
            text = contents.get_text(strip=True)

            # Print the extracted text
            #print(text)
            history.append({"role": "system", "content": "The following is a website requested by the user to be added to the chat:"})
            history.append({"role": "system", "content": text})
            self.updateChat()
        except Exception as e:
            print("Error: Invalid URL")
            print(e)
            history.append({"role": "system", "content": "Error: Invalid URL"})
            self.updateChat()

    def updateChat(self):
        self.displayChat(history[1:])

    def displayChat(self, history):
## clear chat window
        self.chatWindow.clear()
        for line in history:
            ## text box is called "chatWindow"
            if line["role"] == "assistant":
                self.chatWindow.append("<b>" + line["role"] + ": " + line["content"] + "</b>")
            else:
                self.chatWindow.append(line["role"] + ": " + line["content"])

    def openSettings(self):
        self.settingsWindow = SettingsPage()
        self.settingsWindow.show()


class SettingsPage(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('windows/settings.ui', self)
        self.setWindowTitle('Settings')
        self.backButton.clicked.connect(self.backButtonClicked)

    def backButtonClicked(self):
        self.close()
        #self.mainPage = MainPage()
        #self.mainPage.show()

class LoginPage(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('windows/login.ui', self)
        self.setWindowTitle('Login')
        self.submit.clicked.connect(self.loginButtonClicked)

    def loginButtonClicked(self):
        username = self.username.text()
        password = self.password.text()
        ## OAUTH2 stuff here
        authenticated = True
        if authenticated:
            self.close()
            self.mainPage = MainPage()
            self.mainPage.show()

class EmailPage(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('windows/emailPage.ui', self)
        self.setWindowTitle('Email')
        self.get_emails()
        print("Test")

    def get_emails(self):
        emails = email_utils.get_latest_emails_fixed()
        return emails

    def navigate_emails(self, direction):
        None

    def display_email(self, email):
        None





if __name__ == '__main__':
    app = QApplication(sys.argv)
    landing_page = MainPage()
    landing_page.show()
    sys.exit(app.exec_())


