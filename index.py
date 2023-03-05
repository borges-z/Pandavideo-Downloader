import requests
import re
import os
import shutil
import time
from tqdm import tqdm
import re

def main():
    if os.path.exists("temp"):
        shutil.rmtree("temp")

    os.system('cls || clear')
    azul = '\033[34m'
    vermelho = '\033[31m'
    verde = '\033[32m'
    term = '\033[m'
    start = time.time()
    one = False
    link = input('link do video. Ex: playlist.m3u8: ')
    saida = input('nome final do video: ')
    plataforma = input('link da plataforma do video. Ex: https://portalhashtag.com/: ')


    os.system('cls || clear')
    
    hash = 'https://' + link.rsplit("/", 3)[1].replace('b-vz-', 'player-vz-')
    hash2 = link.rsplit("/", 3)[2]

    headers1 = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': f'{plataforma}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'Cache-Control': 'max-age=0',
        'Te': 'trailers'
    }

    headers2 = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Origin': f'{hash}',
        'Referer': f'{hash}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Te': 'trailers'
    }

    pri = requests.get(link, headers=headers1)

    res = re.compile(r'[\d]+[x]+[\d]+')
    check = set(res.findall(str(pri.content)))
    fullhd = ''
    hd = ''
    low = ''
    very_low = ''

    for i in check:
        if i in '1920x1080':
            fullhd = i
        elif i in '1280x720':
            hd = i
        elif i in '640x360':
            low = i
        elif i in '842x480':
            very_low = i
        else:
            print(f'{vermelho}[ERRO] - Falha a obter a resolução{term}')
            exit()
    
    resolution = input(f"Escreva qual resolução deseja, exemplos: {fullhd}, {hd}, {low}, {very_low}: ")
    os.system('cls || clear')

    new = link.rsplit("/", 2)[0].replace('//b-', '//').replace('.br', '').replace('.tv.', '.cdn1.') + '/'
    
    linka = 'https://' + link.rsplit("/", 2)[0].replace('https://b-', '').replace('.br', '').replace('.tv.pandavideo.com', '.b-cdn.net/')

    link3 = new + hash2 + '/' + resolution + '/' + 'video.m3u8'
    linknew = linka + hash2 + '/' + resolution + '/' + 'video.m3u8'
    
    try:
        second = requests.get(link3, headers=headers2)
        one = True
    except:
        second = requests.get(linknew, headers=headers2)

    lista =[]

    m = str(second.content)
    s = m.split('\\')
    for i in s:
        if len(i) <= 14:
            if i in "'b'#EXTM3U'" or i in "#EXT-X-ENDLIST":
                pass
            else:
                a = str(i).replace('n', '')
                if a[0] == 'v':
                    lista.append(a)

    temp_folder = f"{os.getcwd()}/temp"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    videos = f"{os.getcwd()}/videos"
    if not os.path.exists(videos):
        os.makedirs(videos)

    if one == True:
        for i, elem in enumerate(tqdm(lista)):
            nn = new + hash2 + '/' + resolution + '/' + elem
            tr = requests.get(new + hash2 + '/' + resolution + '/' + elem, headers=headers1)
            with open(f'{temp_folder}/input{i}.ts', 'wb') as file, open(f'{temp_folder}/temp.txt', 'a') as l:
                file.write(tr.content)
                l.write(f'file input{i}.ts' + '\n')
    else: 
        for i, elem in enumerate(tqdm(lista)):
            nn = linka + hash2 + '/' + resolution + '/' + elem
            tr = requests.get(nn, headers=headers1)
            with open(f'{temp_folder}/input{i}.ts', 'wb') as file, open(f'{temp_folder}/temp.txt', 'a') as l:
                file.write(tr.content)
                l.write(f'file input{i}.ts' + '\n')
    try:
        print("Juntando...")
        os.chdir('bin')
        os.system('ffmpeg -loglevel quiet -f concat -safe 0 -i "{}/temp.txt" -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 60 "../videos/{}.mp4"'.format(temp_folder, saida))
    
    except:
        print("[ERRO] -> Problema ao juntar arquivos. Reporte!")

    resmeta = input("Deseja remover os metadados? [y/n] ")
    if resmeta in ['yes', 'Y', 'y', 'ye', 'Yes', 'yEs', 'yeS']:
        print(f'{azul}[INFO] - Apagando os metadados{term}')
        os.system(f"exiftool -q -all= -overwrite_original ../videos/{saida}.mp4")
    resmod = input("Deseja modificar os dados de criação/modificação? [y/n] ")
    if resmod in ['yes', 'Y', 'y', 'ye', 'Yes', 'yEs', 'yeS']:
        print(f'{azul}[INFO] - Modificando dados{term}')
        os.system("""exiftool -q -FileModifyDate="1969:10:29 00:00:00" -FileCreateDate="1969:10:29 00:00:00" -overwrite_original ../videos/{}.mp4""".format(saida))
    
    shutil.rmtree(temp_folder)

    end = time.time()
    lep = round(end - start)
    print(f'{azul}[INFO] - tempo: {lep} segundos para a finalização do download.{term}')
    print(f'{verde}[RES] - Download terminado com sucesso!{term}')


main()