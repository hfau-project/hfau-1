from gpiozero import LED
from time import sleep
import socket

GPIO_LED_AMARELO = 24 # mudável
INTERVALO_TESTE = 5 # mudável

def checklist_internet():
    led_amarelo = LED(GPIO_LED_AMARELO)

    def tem_internet() -> bool:
        try:
            conexao = socket.create_connection(("8.8.8.8", 53), timeout=3)
            conexao.close()
            return True

        except OSError:
            return False


    def aguardar_internet() -> None:
        while not tem_internet():
            led_amarelo.on()
            print("Sem internet. LED amarelo aceso.")
            sleep(INTERVALO_TESTE)

        led_amarelo.off()
        led_amarelo.close()
        print("Internet voltou. LED amarelo apagado.")


    aguardar_internet()
