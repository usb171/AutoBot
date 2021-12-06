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
        codDom = elipse.getDomainState()
        if codDom == 2: # Se estiver offline
            telegram.sendMessage(elipse.getDOM())
        elif codDom == 3: # Se estiver online
            telegram.sendMessage(elipse.getDOM())
            while elipse.getDomainState() == 3: # ENQUANTO ESTIVER ONLINE
                time.sleep(10) # ESPERE 10 SEGUNTOS ATÉ A PRÓXIMA VERIFICAÇÃO DO DOMÍNIO


def thread_telegram(telegram):
    telegram.runPooling() # LOOP DE EVENTOS DO BOT TELGRAM



def thread_sendEventsElipseTelegram(elipse, telegram):

    listEvent = elipse.getObjectEventListSink() # RETORNA A LISTA DE EVENTOS DO ELIPSE
    mutex = elipse.getObjectEventMutexSink() # RETORNA O MUTEX PARA CONTROLE DA LISTA DE EVENTOS DO ELIPSE

    while True:
        time.sleep(10)
        mutex.acquire()
        while len(listEvent):
            '''event = listEvent.pop().split(";")
            dataTime = event[0].split(' ')
            tag = event[1].split('.')
            value = event[2]

            data = dataTime[0]
            hora = dataTime[1]
            SE = tag[0]
            EQ = tag[2]
            MEA = tag[4]

            text = " SE: {}\n EQ: {}\n {}: {}\n Data: {}\n Hora: {}\n".format(SE, EQ, MEA, value, data, hora)'''
            #telegram.sendMessage(text)
            print("- ", listEvent.pop(), "  Buffer: ", len(listEvent))
        mutex.release()




if __name__ == "__main__":

    ''''template = {
                "Terminal1": {
                                "IA": "{SE}.{BAY}.[{EQ}].Terminal1.IA",
                                "IB": "{SE}.{BAY}.[{EQ}].Terminal1.IB",
                                "IC": "{SE}.{BAY}.[{EQ}].Terminal1.IC",
                                "VAB": "{SE}.{BAY}.[{EQ}].Terminal1.VAB",
                                "VBC": "{SE}.{BAY}.[{EQ}].Terminal1.VBC",
                                "VCA": "{SE}.{BAY}.[{EQ}].Terminal1.VCA"
                },
                "measurements": {
                                "Status": "{SE}.{BAY}.[{EQ}].Measurements.Status",
                                "MOLA": "{SE}.{BAY}.[{EQ}].Measurements.MOLA",
                                "BOBA": "{SE}.{BAY}.[{EQ}].Measurements.BOBA",
                                "BOBA2": "{SE}.{BAY}.[{EQ}].Measurements.BOBA2",
                                "BOBF": "{SE}.{BAY}.[{EQ}].Measurements.BOBF",
                                "LR": "{SE}.{BAY}.[{EQ}].Measurements.LR",
                                "79BLQ": "{SE}.{BAY}.[{EQ}].Measurements.79BLQ",
                                "NBLQ": "{SE}.{BAY}.[{EQ}].Measurements.NBLQ"
                },
                "protections":{
                                "50N": "{SE}.{BAY}.[{EQ}].Protections.50N",
                                "51F": "{SE}.{BAY}.[{EQ}].Protections.51F",
                                "51N": "{SE}.{BAY}.[{EQ}].Protections.51N",
                                "5051A": "{SE}.{BAY}.[{EQ}].Protections.5051A",
                                "5051B": "{SE}.{BAY}.[{EQ}].Protections.5051B",
                                "5051C": "{SE}.{BAY}.[{EQ}].Protections.5051C",
                                "5051N": "{SE}.{BAY}.[{EQ}].Protections.5051N",
                                "50FN1": "{SE}.{BAY}.[{EQ}].Protections.50FN1",
                                "50FN2": "{SE}.{BAY}.[{EQ}].Protections.50FN2",
                                "50FN3": "{SE}.{BAY}.[{EQ}].Protections.50FN3"
                              }
            }'''


    template = {
        "measurements": {
                    "Tag": "Dados.Tag",
                    "Tag3": "Dados.Tag3",
                    "Tag4": "Dados.Tag4",
                    "Tag5": "Dados.Tag5",
                    "Tag6": "Dados.Tag6",
                    "Tag7": "Dados.Tag7",
                    "Tag8": "Dados.Tag8",
                    "Tag9": "Dados.Tag9",
                    "Tag10": "Dados.Tag10",
                    "Tag11": "Dados.Tag11",
                    "Tag12": "Dados.Tag12",
                    "Tag13": "Dados.Tag13",
                    "Tag14": "Dados.Tag14",
                    "Tag15": "Dados.Tag15",
                    "Tag16": "Dados.Tag16",
                    "Tag17": "Dados.Tag17",
                    "Tag18": "Dados.Tag18",
                    }
    }



    elipse = Elipse(host=config("ELIPSE_HOST"), template=template)
    telegram = Telegram(token=config("TELEGRAM_TOKEN"),
                        chatID=config("TELEGRAM_CHATID"),
                        Elipse=elipse)


    if not elipse.error:

        listEvent = list() # LISTA USADA COMO BUFFER DE EVENTOS
        mutex = threading.Lock() # MUTEX PARA CORDENAR O USO DA LISTA DE EVENTOS

        elipse.setObjectEventListSink(listEvent) # PASSA O BUFFER PARA A CLASSE DE EVENTOS DO ELIPSE
        elipse.setObjectEventMutexSink(mutex) # PASSA O MUTEX PARA A CLASSE DE EVENTOS DO ELIPSE

        th1 = threading.Thread(target=thread_domainState, args=(elipse, telegram)) # THREAD PARA MONITORAR O ESTADO DO DOMÍNIO
        th2 = threading.Thread(target=thread_telegram, args=(telegram,)) # THREAD PARA INTERAÇÕES COM O BOT TELEGRAM
        th3 = threading.Thread(target=thread_sendEventsElipseTelegram, args=(elipse, telegram)) # THREAD PARA ENVIAR OS EVENTOS DO BUFFER PARA O BOT TELEGRAM

        th1.start()
        th2.start()
        th3.start()

        elipse.pumpEventsChanged() # LOOP DE EVENTOS DO ELIPSE


'''
Documents\PROJETOS\AutoBot\env\Scripts\activate
py Documents\PROJETOS\AutoBot\AutoBot\main.py

'''
