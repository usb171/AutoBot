import os
import time
from Elipse import *
from Telegram import *
import threading
from decouple import config
from datetime import datetime



def thread_domainState(elipse, telegram):
    while True:
        time.sleep(15)
        elipse.setObjectEventSink(datetime.now().time())

        codDom = elipse.getDomainState()
        if codDom == 2: # Se estiver offline
            telegram.sendMessage(elipse.getDOM())
        elif codDom == 3: # Se estiver online
            telegram.sendMessage(elipse.getDOM())
            while elipse.getDomainState() == 3:
                time.sleep(10)


def thread_telegram(telegram):
    telegram.runPooling()


if __name__ == "__main__":

    template = {"status": "{SE}.{BAY}.[{EQ}].Measurements.Status",
                "IA": "{SE}.{BAY}.[{EQ}].Terminal1.IA",
                "IB": "{SE}.{BAY}.[{EQ}].Terminal1.IB",
                "IC": "{SE}.{BAY}.[{EQ}].Terminal1.IC",
                "VAB": "{SE}.{BAY}.[{EQ}].Terminal1.VAB",
                "VBC": "{SE}.{BAY}.[{EQ}].Terminal1.VBC",
                "VCA": "{SE}.{BAY}.[{EQ}].Terminal1.VCA",
                "79BLQ":"",
                "NBLQ":"",
                "51F":"",
                "51N":"",
                "50F":"",
                "50N":"",
                "50FN1":"",
                "50FN2":"",
                "50FN3":""}

    elipse = Elipse(host=config("ELIPSE_HOST"), template=template)
    telegram = Telegram(token=config("TELEGRAM_TOKEN"),
                        chatID=config("TELEGRAM_CHATID"),
                        Elipse=elipse)


    if not elipse.error:

        th1 = threading.Thread(target=thread_domainState, args=(elipse, telegram))
        th2 = threading.Thread(target=thread_telegram, args=(telegram,))

        th1.start()
        th2.start()

        elipse.pumpEventsChanged()


'''
Documents\PROJETOS\AutoBot\env\Scripts\activate
py Documents\PROJETOS\AutoBot\AutoBot\main.py

'''
