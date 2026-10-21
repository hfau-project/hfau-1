from gpiozero import OutputDevice, LED, DistanceSensor
from Corretude.Temperatura import checklist_temperatura
from Desligar import rodar_desligamento

from datetime import datetime #EMBUTIDO PYTHON
from time import sleep #EMBUTIDO PYTHON
import socket #EMBUTIDO PYTHON
from pathlib import Path #EMBUTIDO PYTHON
import csv #EMBUTIDO PYTHON
import math #EMBUTIDO PYTHON

GPIO_VENTOINHA = 5 #Segundo mensagem do joão no dia 21/10/2026
GPIO_LED_MAIN = 23 #Segundo mensagem do joão no dia 21/10/2026
GPIO_LEDS_SECUNDARIAS = [25, 24, 16] #Segundo mensagem do joão no dia 21/10/2026
GPIO_TRIGGER = 22 #Segundo mensagem do joão no dia 21/10/2026
GPIO_ECHO = 27 #Segundo mensagem do joão no dia 21/10/2026

TIMEOUT_INTERNET = 1
HORARIO_DESLIGAMENTO = "23:00"  # formato HH:MM

INTERVALO_COLETA = 10 #ISSO É EQUIVALENTE A 6 CSVs POR MINUTO
PASTA_CSVS = Path(__file__).resolve().parent / "CSVs_treinamento"


def rodar_rotina(distancia_maxima: float):
    ventoinha = OutputDevice(GPIO_VENTOINHA)
    led_main = LED(GPIO_LED_MAIN) # SEM FUNÇÃO FIXA
    leds_secundarias = [LED(pino) for pino in GPIO_LEDS_SECUNDARIAS] # SEM FUNÇÃO FIXA
    sensor_hc = DistanceSensor(echo=GPIO_ECHO, trigger=GPIO_TRIGGER)

    def coleta_armazenamento(sensor_hc):

        while True:
            agora = datetime.now()

            # CRIA A PASTA E DEFINE O ARQUIVO DO DIA
            pasta_dia = PASTA_CSVS / agora.strftime("%d_%m")
            pasta_dia.mkdir(parents=True, exist_ok=True)
            nome_arquivo = agora.strftime("%d_%m") + ".csv"
            caminho_csv = pasta_dia / nome_arquivo

        # 5 LEITURAS EM 1 SEGUNDO
            leituras = []
            for _ in range(5):
                leituras.append(sensor_hc.distance * 100)
                sleep(0.2)

        # DIA DA SEMANA E HORÁRIO
            weekend = 1 if agora.weekday() in [5, 6] else 0
            minuto_do_dia = agora.hour * 60 + agora.minute
            hora_sin = math.sin(2 * math.pi * minuto_do_dia / 1440)
            hora_cos = math.cos(2 * math.pi * minuto_do_dia / 1440)

        # ESCREVE NO CSV
            escrever_cabecalho = not caminho_csv.exists()
            with open(caminho_csv, "a", newline="", encoding="utf-8") as arquivo:
                escritor = csv.writer(arquivo)

                if escrever_cabecalho:
                    escritor.writerow([
                        "data_hora",
                        "weekend",
                        "hora_sin",
                        "hora_cos",
                        "distancia_cm",
                        "distancia_maxima_cm",
                        "delta_cm",
                    ])

                for leitura in leituras:
                    escritor.writerow([
                        agora.strftime("%Y-%m-%d %H:%M:%S"),
                        weekend,
                        hora_sin,
                        hora_cos,
                        leitura,
                        distancia_maxima,
                        distancia_maxima - leitura,
                    ])

            verificar_desligamento()
            verificar_conexao_internet()
            iniciar_ventoinha()

    def verificar_desligamento():
        if datetime.now().strftime("%H:%M") > HORARIO_DESLIGAMENTO:
            rodar_desligamento(
                ventoinha=ventoinha,
                sensor_hc=sensor_hc,
                led_main=led_main,
                leds_secundarias=leds_secundarias
            )

    def iniciar_ventoinha():
        temperatura = checklist_temperatura()
    
        if temperatura is None:
            return  # or log a warning

        if temperatura >= 45.0:
            ventoinha.on()
        elif temperatura <= 40.0:
            ventoinha.off()

    def verificar_conexao_internet():
        try:
            with socket.create_connection(("8.8.8.8", 53), timeout=TIMEOUT_INTERNET):
                return True
        
        except OSError:
            return False
          
    def manter_led_main_ligada():
        led_main.on()

    manter_led_main_ligada()
    coleta_armazenamento(sensor_hc)

# def iniciar_ventoinha():
#     temperatura = ler_temperatura_cpu()
#
#     if temperatura is None:
#         print("Não foi possível ler a temperatura.")
#         return
#
#     if temperatura >= 45.0:
#         print("Ventoinha em rotação intermediária.")
#
#         while temperatura >= 45.0:
#             ventoinha.on()
#             sleep(0.5)
#             ventoinha.off()
#             sleep(0.5)
#             temperatura = ler_temperatura_cpu()

