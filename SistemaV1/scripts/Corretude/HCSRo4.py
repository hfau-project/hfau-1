from Desligar import rodar_desligamento
from gpiozero import DistanceSensor
from time import sleep

GPIO_TRIGGER = 22 #Segundo mensagem do joão no dia 21/10/2026

GPIO_ECHO = 27 #Segundo mensagem do joão no dia 21/10/2026


MINIMO_LEITURAS_VALIDAS_HC = 3 #MUTÁVEL
DISTANCIA_MAXIMA_METROS = 4
TENTATIVAS_HC = 5 #MUTÁVEL


def checklist_HCSR04():
    sensor_hc = None

    try:
        sensor_hc = DistanceSensor(
            echo=GPIO_ECHO,
            trigger=GPIO_TRIGGER,
            max_distance=DISTANCIA_MAXIMA_METROS
        )

        sleep(0.5)

        leituras_validas = []

        for _ in range(TENTATIVAS_HC):
            distancia_cm = sensor_hc.distance * 100

            if 0 < distancia_cm <= DISTANCIA_MAXIMA_METROS * 100:
                leituras_validas.append(distancia_cm)

            sleep(0.2)

        if len(leituras_validas) < MINIMO_LEITURAS_VALIDAS_HC:
            print("HC-SR04 não retornou leituras válidas suficientes")
            rodar_desligamento(sensor_hc=sensor_hc)

        print("Tudo okay com o HC-SR04")

    except ValueError as erro:
        print(f"GPIO inválido no HC-SR04: {erro}")
        rodar_desligamento(sensor_hc=sensor_hc)

    except RuntimeError as erro:
        print(f"Erro ao acessar/controlar HC-SR04: {erro}")
        rodar_desligamento(sensor_hc=sensor_hc)

    except Exception as erro:
        print(f"Erro inesperado no HC-SR04: {erro}")
        rodar_desligamento(sensor_hc=sensor_hc)

    finally:
        if sensor_hc is not None:
            sensor_hc.close()