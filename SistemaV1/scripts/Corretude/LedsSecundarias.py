from gpiozero import LED
from time import sleep

GPIO_LEDS_SECUNDARIAS = [25, 24, 16] #Segundo mensagem do joão no dia 21/10/2026



def checklist_ledsSecundarias():
    for pino in GPIO_LEDS_SECUNDARIAS:
        try:
            led = LED(pino)
            led.on()
            sleep(1)
            led.off()
            led.close()
            print(f"LED secundaria no GPIO {pino} okay.")

        except ValueError as erro:
            print(f"GPIO inválido na LED secundaria {pino}: {erro}")

        except RuntimeError as erro:
            print(f"Erro na LED secundaria GPIO {pino}: {erro}")

        except Exception as erro:
            print(f"Erro inesperado na LED secundaria GPIO {pino}: {erro}")
