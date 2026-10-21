from scripts.Desligar import rodar_desligamento
from gpiozero import OutputDevice
from time import sleep
import requests

#TOKEN = "SEU_TOKEN"
#URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

#CHAT_IDS = [
#    0000000000,  # voce
#    0000000000,  # seu colega
#]

GPIO_ATIVADOR = 5 #Segundo mensagem do joão no dia 21/10/2026


def checklist_ventoinha():
    ventoinha = None

    #def enviar_telegram(mensagem):
    #    for chat_id in CHAT_IDS:
    #        try:
    #            resposta = requests.post(
    #                URL,
    #                json={"chat_id": chat_id, "text": mensagem},
    #                timeout=10
    #            )
    #            resposta.raise_for_status() # CASO ERROS DO TELEGRAM
    #        except requests.RequestException: # CASO ERROS DO TELEGRAM
    #            pass

    try:
        ventoinha = OutputDevice(GPIO_ATIVADOR)
        ventoinha.on()
        sleep(2)
        ventoinha.off()
        ventoinha.close()

        #enviar_telegram("Tudo okay com a ventoinha")

    except ValueError as erro:
        #enviar_telegram(f"GPIO inválido: {erro}")
        rodar_desligamento(ventoinha=ventoinha)

    except RuntimeError as erro:
        #enviar_telegram(f"Erro ao acessar/controlar GPIO: {erro}")
        rodar_desligamento(ventoinha=ventoinha)

    except Exception as erro:
        #enviar_telegram(f"Erro inesperado: {erro}")
        rodar_desligamento(ventoinha=ventoinha)