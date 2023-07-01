import schedule
from main.services import send_email_to_clients


def my_scheduled_sending():
    schedule.every(60).seconds.do(send_email_to_clients)