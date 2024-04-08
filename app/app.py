from utils import get_revenda_condicoes
from flet import dropdown
import pyautogui
from time import sleep

running = True
pause = False

def carregar_arquivo(caminho):
    with open(caminho, encoding='iso-8859-1') as arquivo:
        data = arquivo.readlines()
    return data

# data = carregar_aquivo(caminho_arquivo)
data = ''

def separar_mapas(data):
    indice_mapas = []
    mapas = []
    for i, linha in enumerate(data):
        if 'Mapa' in linha:
            index_mapa = linha.index('Mapa')+6
            mapa = linha[index_mapa:index_mapa+7].replace('.', '')
            mapas.append(mapa)
            indice_mapas.append(i)
    indice_mapas = adicionar_mapa_indices(indice_mapas, mapas)
    return indice_mapas, list(set(mapas))

def get_mapas():
    none, mapas = separar_mapas(data)
    return mapas

def adicionar_mapa_indices(indices, mapas):
    indice_mapa = []
    for i in range(1, len(indices)):
        indice_mapa.append((indices[i-1], indices[i], mapas[i-1]))
    return indice_mapa
    
def separar_notas(condicao):
    indices, mapas = separar_mapas(data)
    notas = {}
    linhas = []
    for i in range(len(indices)):
        for lin in data[indices[i][0]:indices[i][1]]:
            if condicao in lin:  
                mapa = indices[i][2]
                if mapa not in notas:
                    notas[mapa] = []
                nota_formatada = (lin[lin.index(condicao)-21:lin.index(condicao)-14]).replace('.', '')
                notas[mapa].append(nota_formatada)
                linhas.append(lin)
    
    if notas:
        return notas, linhas
    return None, False

def separar_condicoes_encontradas(revenda):
    condicoes_revenda = get_revenda_condicoes(revenda)
    condicoes_existentes = []
    condicoes_encontradas = []
    indice_mapas, mapas = separar_mapas(data)
    
    for cond in condicoes_revenda:
        condicoes_existentes.append(cond['DESCRICAO'])
        notas, flag = separar_notas(cond['DESCRICAO'])
        if(flag):
            condicoes_encontradas.append(cond['DESCRICAO'])
    
    
    return condicoes_encontradas, condicoes_existentes
    

def get_condicoes(revenda):
    condicoes_encontradas, condicoes_existentes = separar_condicoes_encontradas(revenda)
    return condicoes_encontradas, condicoes_existentes

def get_condicoes_options(revenda):
    condicoes_encontradas, condicoes_existentes = get_condicoes(revenda)
    condicoes_encontradas_options = []
    condicoes_existentes_options = []
    
    for cond_e in condicoes_encontradas:
        condicoes_encontradas_options.append(dropdown.Option(cond_e))
    for cond_e in condicoes_existentes:
        condicoes_existentes_options.append(dropdown.Option(cond_e))
    
    return condicoes_encontradas_options, condicoes_existentes_options


def get_mapas_options():
    lista, mapas = separar_mapas(data)
    mapas.insert(0, 'TODOS')
    lista = []
    if mapas:
        for i in mapas:
            lista.append(dropdown.Option(i)) 
        return lista
    return None


def iniciar_alteracoes():
    pass

def get_condicao_codigo(condicao, revenda):
    codigos = get_revenda_condicoes(revenda)
    for cod in codigos:
        if cod['DESCRICAO'] == condicao:
            return cod['CODIGO']
    return None


def press_and_wait(key, wait_time):
    pyautogui.press(key)
    sleep(wait_time)

def executar_codigo(codigos, porcentagem_text):
        try:
            total = len(codigos)
            feito = 0

            sleep(2)  # Apenas para simular um processo de execu  o
            for mapa in codigos:
                if not running:
                    break
                
                pyautogui.hotkey('alt', 'c')
                if not running:
                    break
                
                pyautogui.write(str(mapa[0]))
                press_and_wait('tab', 0.1)
                
                pyautogui.write(str(mapa[1]))
                press_and_wait('tab', 0.1)
                press_and_wait('tab', 0.1)
                
                if not running:
                    break
                
                pyautogui.write('5')
                press_and_wait('tab', 0.3)
                
                if not running:
                    break
                
                pyautogui.press('enter')
                press_and_wait('enter', 0.2)
                press_and_wait('enter', 0.2)
                press_and_wait('enter', 0.2)
                press_and_wait('enter', 0.2)
                
                if not running:
                    break
                pyautogui.hotkey('alt', 'c')
                if not running:
                    break
                feito += 1
                
                porcentagem_text.value = 'Progresso: ' + str(f"{((feito/total)*100):.2f}")
                porcentagem_text.update()
                sleep(1)
            porcentagem_text.value = 'Processo concluído! Selecione outro arquivo caso tenha mais alterações.'

        except Exception as e:
            print("Erro", f"Ocorreu um erro durante a execu  o:\n{str(e)}")

        # self.running = False
        # self.progress_label.config(text="Clique em 'Iniciar' para come ar as altera  es.")
        # self.start_button.config(state=tk.NORMAL)
        # self.cancel_button.config(state=tk.DISABLED)