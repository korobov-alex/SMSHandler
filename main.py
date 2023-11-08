import kivy
import smtplib
from kivy.app import App
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from email.message import EmailMessage

kivy.require('2.2.1')

gmail_user = 'alexkorobov95@gmail.com'
gmail_password = 'sbno rjmb baxr atls'


def get_sms_data():
    store = JsonStore('sms.json')

    # Если ключ 'sms' существует, вернуть его значение
    if 'sms' in store:
        new_sms = store.get('sms')
    # Иначе вернуть пустой список
    else:
        new_sms = []

    return new_sms


class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()

    def start_program(self):
        self.label_text.text = "Program is started"
        # Запустить получение данных SMS
        Clock.schedule_interval(lambda dt: self.handle_new_sms(), 1)

    def handle_new_sms(self):
        sms_data = get_sms_data()
        if sms_data:
            sender_number = sms_data[0]['sender_number']
            message_content = sms_data[0]['message_content']
            timestamp = sms_data[0]['timestamp']
            email_content = (f"New SMS received:\n\nSender's number: {sender_number}\nMessage: {message_content}\n"
                             f"Timestamp: {timestamp}")
            self.send_saved_sms(email_content)

    def send_saved_sms(self, message):
        sent_from = gmail_user
        to = self.ids.email_text.text
        body = message
        subject = 'SMS Phone notification'
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sent_from
            msg['To'] = to
            msg.set_content(body)
            server.send_message(msg)
            server.close()
            print('Email sent!')
        except Exception as e:
            print(f'Something went wrong: {e}')

    def finish_program(self):
        self.label_text.text = "Program is stopped"
        # Остановить получение данных SMS
        Clock.unschedule(self.handle_new_sms)
        notCheckerApp.stop()


class NotCheckerApp(App):

    def build(self):
        return MyRoot()


if __name__ == '__main__':
    notCheckerApp = NotCheckerApp()
    notCheckerApp.run()
