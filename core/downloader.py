import yt_dlp
import requests
import os

def gerar_nome_unico(base_nome, extensao="mp4"):
    """
    Verifica se o arquivo já existe e adiciona um sufixo numérico para evitar sobrescrita.
    Ex: usuario.mp4 -> usuario_1.mp4 -> usuario_2.mp4
    """
    contador = 1
    nome_final = f"downloads/{base_nome}.{extensao}"
    
    while os.path.exists(nome_final):
        nome_final = f"downloads/{base_nome}_{contador}.{extensao}"
        contador += 1
        
    return nome_final

def baixar_via_api_tikwm(url):
    """
    PLANO B: Usa a API TikWM para extrair o vídeo sem marca d'água.
    """
    print("[!] yt-dlp falhou. Acionando Fallback via API TikWM...")
    api_url = "https://www.tikwm.com/api/"
    
    try:
        # Faz a requisição para a API passando o link do vídeo
        resposta = requests.get(api_url, params={"url": url})
        dados = resposta.json()
        
        if dados.get("code") == 0:
            # Extrai os dados do JSON que a API devolve
            nome_criador = dados["data"]["author"]["unique_id"]
            link_video = dados["data"]["play"] # Link direto do .mp4 sem marca
            
            nome_arquivo = gerar_nome_unico(nome_criador)
            
            # Baixa o arquivo mp4 diretamente
            print(f"[*] Baixando arquivo direto da API para: {nome_criador}...")
            video_bytes = requests.get(link_video).content
            
            with open(nome_arquivo, 'wb') as f:
                f.write(video_bytes)
                
            print(f"[+] Sucesso via API! Salvo em: {nome_arquivo}\n")
            return True
        else:
            print("[-] Erro: A API não conseguiu processar este link.\n")
            return False
            
    except Exception as e:
        print(f"[-] Falha catastrófica no Fallback: {e}\n")
        return False

def baixar_video(url):
    """
    PLANO A: Tenta usar o yt-dlp primeiro.
    Se falhar, aciona a função baixar_via_api_tikwm automaticamente.
    """
    # Corta a string no ponto de interrogação e pega só a primeira parte (o link puro)
    url_limpa = url.split('?')[0]

    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url_limpa, download=False)
        usuario = info.get('uploader', 'usuario_desconhecido')

    caminho_final = gerar_nome_unico(usuario)

    opcoes_yt_dlp = {
        'outtmpl': caminho_final,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': False,
        'no_warnings': False, 
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        },
        
        # --- A BLINDAGEM PARA O TWITTER (X) ---
        'postprocessors': [{
            # Garante que o arquivo passe pelo FFmpeg no final
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'postprocessor_args': {
            # Injeta as regras exatas que o algoritmo do Twitter exige
            'default': [
                '-c:v', 'libx264',     # Força o vídeo para H.264
                '-pix_fmt', 'yuv420p', # Formato de pixel universal (O Twitter barra se não tiver isso)
                '-c:a', 'aac'          # Força o áudio para AAC
            ]
        }
    }

    try:
        print(f"[*] Tentando yt-dlp para: {url}")
        with yt_dlp.YoutubeDL(opcoes_yt_dlp) as ydl:
            ydl.download([url_limpa])
        print("[+] Sucesso via yt-dlp!\n")
        return True
    
    except Exception as e:
        print(f"\n[!] DIAGNÓSTICO DE ERRO DO YT-DLP:")
        # O repr(e) força o Python a mostrar o erro em formato bruto
        print(f"Motivo da falha: {repr(e)}\n")
        
        return baixar_via_api_tikwm(url)
    
def baixar_video_instagram(url):
    """
    Motor dedicado para o Instagram. Usa os cookies para burlar o bloqueio de login.
    """
    print(f"\n[*] Detectado link do Instagram. Injetando cookies para: {url}")
    
    # Limpeza da URL para evitar rastreadores do Instagram
    url_limpa = url.split('?')[0]

    # Extrair nome do usuário passando o cookie (o Instagram bloqueia até isso sem login)
    opcoes_extracao = {
        'quiet': True, 
        'cookiefile': 'cookies/instagram_cookie.txt'
    }
    
    with yt_dlp.YoutubeDL(opcoes_extracao) as ydl:
        try:
            info = ydl.extract_info(url_limpa, download=False)
            usuario = info.get('uploader', 'insta_user')
        except Exception:
            # Se falhar ao ler o nome, usa um padrão seguro
            usuario = 'insta_user'

    caminho_final = gerar_nome_unico(usuario)

    opcoes_yt_dlp = {
        'outtmpl': caminho_final,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': False,
        'no_warnings': False,
        'cookiefile': 'cookies/instagram_cookie.txt', 
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        },
        
        # --- A BLINDAGEM PARA O TWITTER (X) ---
        'postprocessors': [{
            # Garante que o arquivo passe pelo FFmpeg no final
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'postprocessor_args': {
            # Injeta as regras exatas que o algoritmo do Twitter exige
            'default': [
                '-c:v', 'libx264',     # Força o vídeo para H.264
                '-pix_fmt', 'yuv420p', # Formato de pixel universal (O Twitter barra se não tiver isso)
                '-c:a', 'aac'          # Força o áudio para AAC
            ]
        }
    }

    try:
        print(f"[*] Iniciando download seguro via yt-dlp (Instagram)...")
        with yt_dlp.YoutubeDL(opcoes_yt_dlp) as ydl:
            ydl.download([url_limpa])
        print(f"[+] Sucesso! Vídeo do Instagram salvo em: {caminho_final}\n")
        return True
    
    except Exception as e:
        print(f"\n[!] FALHA NO INSTAGRAM:")
        print(f"Motivo: {repr(e)}")
        print("[DICA] Verifique se o instagram_cookie.txt está válido ou se a conta foi deslogada.\n")
        return False