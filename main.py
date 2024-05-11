from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.config import Config
import string
from random import choice, shuffle, randint
from os.path import exists
import json
from sys import exit

Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '350')
Config.set('graphics', 'resizeable', 'False')


class View(BoxLayout):
    website_input = ObjectProperty(None)
    emailorusername_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    new_data = None
    file = None
    file_exists = None
    path = "log.json"
    input_color = 1, 1, 1, 0.1
    white = 1, 1, 1, 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate_pw(self):
        letters = string.ascii_uppercase + string.ascii_lowercase
        numbers = string.digits
        symbols = string.punctuation
        # print(letters)
        pw_letters = [choice(letters) for _in in range(randint(8, 10))]
        pw_numbers = [choice(numbers) for _in in range(randint(1, 2))]
        pw_symbols = [choice(symbols) for _in in range(randint(1, 2))]

        password_list = pw_letters + pw_numbers + pw_symbols
        shuffle(password_list)
        self.password_input.text = "".join(password_list)

    def save_profile(self):
        website_text = self.website_input.text
        emailorusername_text = self.emailorusername_input.text
        password_text = self.password_input.text
        print(website_text, emailorusername_text)
        if emailorusername_text != '' and website_text != '' and password_text != '':
            self.new_data = {
                website_text: {
                    'email': emailorusername_text,
                    'password': password_text
                }
            }
            # print(self.new_data)
            self.save_to_file()

    def save_to_file(self):
        self.load_file()
        self.file = open(self.path, "r")
        try:
            data = json.load(self.file)
        except json.decoder.JSONDecodeError:
            self.file = open(self.path, "w+")
            json.dump(self.new_data, self.file, indent=4)
        else:
            self.file = open(self.path, mode='w')
            data.update(self.new_data)
            json.dump(data, self.file, indent=4)
        finally:
            self.file.close()

    def create_file(self):
        self.file = open("log.json", "x")

    def load_file(self):
        self.file_exists = exists(self.path)
        if not self.file_exists:
            self.create_file()

    def load_profile(self):
        self.load_file()
        keyword = self.website_input.text
        if keyword != '':
            self.file = open(self.path, mode='r')
            try:
                data = json.load(self.file)
            except json.decoder.JSONDecodeError:
                exit()
            else:
                if keyword in data:
                    self.emailorusername_input.text = data[keyword]['email']
                    self.password_input.text = data[keyword]['password']
                else:
                    print("Keyword Not Found!")


class PasswordManager(App):
    def build(self):
        self.icon = "logo.ico"
        return View()


PasswordManager().run()
