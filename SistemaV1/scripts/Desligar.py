GPIO_VENTOINHA = 5 #Segundo mensagem do joão no dia 21/10/2026
GPIO_LED_MAIN = 23 #Segundo mensagem do joão no dia 21/10/2026
GPIO_LEDS_SECUNDARIAS = [25, 24, 16] #Segundo mensagem do joão no dia 21/10/2026
GPIO_TRIGGER = 22 #Segundo mensagem do joão no dia 21/10/2026
GPIO_ECHO = 27 #Segundo mensagem do joão no dia 21/10/2026

def rodar_desligamento(ventoinha=None, sensor_hc=None, led_main=None, leds_secundarias=None):
    saidas = [ventoinha, led_main]

    if leds_secundarias is not None:
        saidas.extend(leds_secundarias)

    componentes = [*saidas, sensor_hc] # componentes = [["ventoinha", "led_main", "led_1"], "hc"]

    try:
        for saida in saidas:
            if saida is not None:
                saida.off()
    finally:
        for componente in componentes:
            if componente is not None:
                componente.close()

    raise SystemExit