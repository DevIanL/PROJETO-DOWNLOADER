import time
import random

def pausa_randomica(min_segundos=5.5, max_segundos=12.4):
    """
    Simula o tempo de um humano assistindo e rolando o feed do TikTok.
    Janela segura para 30 links: entre 5.5 e 12.4 segundos.
    """
    tempo_espera = random.uniform(min_segundos, max_segundos)
    print(f"[!] Pausa de segurança: Aguardando {tempo_espera:.2f} segundos...")
    time.sleep(tempo_espera)