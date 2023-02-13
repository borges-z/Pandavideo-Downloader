import requests
import re
import os
import shutil
from datetime import datetime
import time
from tqdm import tqdm

def main():
    os.system('cls || clear')
    start = time.time()
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

    #print('\n\n' + hash + '\n\n')
    n = re.compile(r'\d+')
    res = re.compile(r'[\d]+[x]+[\d]+')
    check = res.findall(str(pri.content))
    for i in check:
        if i == '1920x1080':
            resolution = i
            break
        elif i == '1280x720':
            resolution = i
            break
        elif i == '640x360':
            resolution = i
            break
        elif i == '842x480':
            resolution = i
            break
        else:
            print('[ERRO]- erro ao obter a resolução')

    new = link.rsplit("/", 2)[0].replace('b-', '').replace('.br', '').replace('.tv.', '.cdn1.') + '/'
    
    link3 = new + hash2 + '/' + resolution + '/' + 'video.m3u8'
    
    second = requests.get(link3, headers=headers2)
    

    lista =[]

    m = str(second.content)
    s = m.split('\\')
    for i in s:
        if len(i) <= 100:
            a = str(i).replace('n', '')
            if a[0] == 'v':
                lista.append(a)

    temp_folder = f"{os.getcwd()}/temp"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    videos = f"{os.getcwd()}/videos"
    if not os.path.exists(videos):
        os.makedirs(videos)

    for i, elem in enumerate(tqdm(lista)):
        tr = requests.get(new + hash2 + '/' + resolution + '/' + elem, headers=headers1)
        with open(f'{temp_folder}/input{i}.ts', 'wb') as file, open(f'{temp_folder}/temp.txt', 'a') as l:
            file.write(tr.content)
            l.write(f'file input{i}.ts' + '\n')

    os.system('ffmpeg -loglevel quiet -f concat -safe 0 -i "{}/temp.txt" -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 60 "videos/{}.mp4"'.format(temp_folder, saida))

    shutil.rmtree(temp_folder)

    end = time.time()
    lep = round(end - start)
    print(f'tempo: {lep} segundos para a finalização do download.')


main()