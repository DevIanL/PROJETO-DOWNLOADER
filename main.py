import os
from core.downloader import baixar_video, baixar_video_instagram
from utils.helpers import pausa_randomica

def ler_links(caminho_arquivo='links.txt'):
    """Lê o arquivo de texto e retorna uma lista de links limpos."""
    if not os.path.exists(caminho_arquivo):
        print(f"[-] Erro Crítico: O arquivo '{caminho_arquivo}' não foi encontrado na raiz do projeto.")
        # Cria um arquivo vazio para facilitar a vida na próxima execução
        with open(caminho_arquivo, 'w') as f:
            pass
        print(f"[*] Arquivo '{caminho_arquivo}' criado automaticamente. Cole seus links lá e rode novamente.")
        return []
    
    with open(caminho_arquivo, 'r') as arquivo:
        # Pega as linhas, remove espaços em branco, \n, e ignora linhas vazias
        links = [linha.strip() for linha in arquivo.readlines() if linha.strip()]
    return links

def main():
    print("===================================================")
    print("    Iniciando Motor Node Bahia (Foco: TikTok)      ")
    print("===================================================\n")
    
    # Passo 1: Garante que a pasta de destino existe
    os.makedirs('downloads', exist_ok=True)
    
    # Passo 2: Carrega a fila de trabalho
    links = ler_links()
    
    if not links:
        print("[!] A fila está vazia. Processo encerrado.")
        return

    total_links = len(links)
    print(f"[*] Fila carregada: {total_links} links encontrados.\n")

    # Passo 3: Executa o loop principal
    for index, url in enumerate(links, start=1):
        print(f"--- Processando vídeo {index} de {total_links} ---")
        
        # Chama a nossa função robusta (Plano A e Plano B integrados)
        # Roteador Inteligente Node Bahia
        if "tiktok.com" in url:
            baixar_video(url)
        elif "instagram.com" in url:
            baixar_video_instagram(url)
        else:
            print(f"[-] Plataforma ignorada ou não suportada: {url}")
        
        # Passo 4: O Jitter (Pausa de Segurança)
        # Só aplicamos a pausa se NÃO for o último vídeo da lista
        if index < total_links:
            pausa_randomica()
            print("-" * 50) # Linha separadora para organizar o terminal

    print("\n===================================================")
    print(" [+] Todos os vídeos foram processados com sucesso!  ")
    print("     Verifique a pasta 'downloads/'.               ")
    print("===================================================")

if __name__ == "__main__":
    main()