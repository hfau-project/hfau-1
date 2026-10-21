from gpiozero import LED
from time import sleep

GPIO_LED_MAIN = 23 #Segundo mensagem do joão no dia 21/10/2026


def checklist_ledMain():
    try:
        led_main = LED(GPIO_LED_MAIN)
        led_main.on()
        sleep(1)
        led_main.off()
        led_main.close()
        print("LED principal okay.")

    except ValueError as erro:
        print(f"GPIO inválido: {erro}")

    except RuntimeError as erro:
        print(f"Erro ao controlar LED principal: {erro}")

    except Exception as erro:
        print(f"Erro inesperado no LED principal: {erro}")