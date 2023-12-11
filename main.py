import jnius
import kivy
import smtplib
import datetime
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from email.message import EmailMessage
from jnius import autoclass

String = jnius.autoclass("java.lang.String")
SmsManager = autoclass('android.telephony.SmsManager')


kivy.require('2.2.1')

gmail_user = 'alexkorobov95@gmail.com'
gmail_password = 'sbno rjmb baxr'


def get_sms():
    smsManager = SmsManager.getDefault()
    smsList = smsManager.getAllMessages()
    for sms in smsList:
        if sms.date > datetime.datetime.now() - datetime.timedelta(hours=1):
            smsText = sms.getMessageBody()
            return smsText
    return None


class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()

    def start_program(self):
        self.label_text.text = "Program is started"
        # Запустить получение данных SMS
        Clock.schedule_interval(lambda dt: self.handle_new_sms(), 1)

    def handle_new_sms(self):
        sms_data = get_sms()
        self.send_saved_sms(sms_data)

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
