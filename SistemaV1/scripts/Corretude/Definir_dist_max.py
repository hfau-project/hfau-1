ifrom gpiozero import DistanceSensor
from time import sleep

GPIO_TRIGGER = 22 #Segundo mensagem do joão no dia 21/10/2026
GPIO_ECHO = 27 #Segundo mensagem do joão no dia 21/10/2026
MAX_DIST_M = 4

def definir_dis_max():
    sensor = DistanceSensor(echo=GPIO_ECHO, trigger=GPIO_TRIGGER, max_distance=MAX_DIST_M)
    medidas = []

    for _ in range(5):
        medidas.append(sensor.distance * 100)	#cm
        sleep(0.2)

    sensor.close()

    distancia_maxima = sum(medidas) / len(medidas)
    print(f"Distância máxima definida: {distancia_maxima:.1f} cm")
    return distancia_maxima


# Há uma dúvida teórica aqui, se der 4 metros naquele dia, pode ser por fatores com fugindo do range máximo ou "no echo received".
# Sequer mensuramos a distância do corredor. Todavia, talvez seja menor do que 4 metros.
