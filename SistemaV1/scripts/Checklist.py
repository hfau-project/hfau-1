
from Corretude.Ventoinha import checklist_ventoinha
from Corretude.HCSRo4 import checklist_HCSR04
from Corretude.Internet import checklist_internet
from Corretude.LedMain import checklist_ledMain
from Corretude.LedsSecundarias import checklist_ledsSecundarias
from Corretude.Temperatura import checklist_temperatura
from Corretude.Definir_dist_max import definir_dis_max

# $ = falta mensagem pelo telegram

# * = função que será usada na rotina

def rodar_checklist() -> float:
    checklist_ventoinha()  # $
    checklist_HCSR04() # $
    checklist_temperatura()  # $*
    checklist_ledMain()  # $
    checklist_ledsSecundarias()  # $
    checklist_internet()  # $
    return definir_dis_max()  # $
