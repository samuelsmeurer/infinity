import mysql.connector
import pymysql.cursors
import cv2
import webbrowser
import datetime
import time
from cryptography.fernet import Fernet
import PySimpleGUI as sg


#colors do front
cor_amarelo = '#ffc000'
cor_preto = '#161616'
cor_azul = '#1B1C3F'
cor_azul_claro = '#313273'
cor_laranja = '#F09800'
cor_branco = 'white'
sg.theme('Dark Blue 17')





#conexao db
file = open('chave.key', 'rb')
chave_lida = file.read()
file.close()

cifra = Fernet(chave_lida)

file = open('dados_bd.txt', 'rb')
arquivo = file.read()

texto = cifra.decrypt(arquivo)

arq = str(texto, 'utf-8')
file.close()

arq = arq.split('\n')

dados = []
for linha in range(len(arq)):
    dados.append(arq[linha].rstrip())

try:
    conexao = pymysql.connect(
        host = dados[0],
        port = int(dados[1]),
        user = dados[2],
        password = dados[3],
        database = dados[4],
    )
    conectado = True
    bd = dados[4]

except:
    sg.popup_error('Impossível se conectar ao Banco de Dados!', title='Erro de conexão',text_color=(cor_branco))
    exit()

ticketusado = list()
def callwebcan(x):

    with conexao.cursor() as cursor:
        conexao.commit()
        cursor.execute('select * from ticketusado')
        ticketusado = cursor.fetchall()
    cursor.close()
    x = x.upper()
    id = 1000
    try:    
        encontrado = 0
        for i in range(len(ticketusado)):
            id =id +1
            if ticketusado[i][1] == x:
                sg.popup_error('ACESSO NEGADO!!! O ticket {} já foi utilizado no dia {} '.format(x,ticketusado[i][2]), title='Erro de conexão',text_color=(cor_branco))
                #print('ACESSO NEGADO!!! O ticket {} já foi utilizado no dia {} '.format(x,ticketusado[i][2]))
                encontrado += 1
                time.sleep(1)
                
        if encontrado ==0:
            print("entrei aqui")
            with conexao.cursor() as cursor:
                print(a)
                cursor.execute('insert into ticketusado values( {}, "{}" , "{}")'.format(id,x,datetime.datetime.now()))
                conexao.commit()
            cursor.close()
            encontrado +=1  
            sg.popup('O seu ingresso "{}" acabou de ser utilizado!'.format(data), title='Erro de conexão',text_color=(cor_branco))
            #print('O seu ingresso "{}" acabou de ser utilizado!'.format(data))
            sg.popup_error
            time.sleep(1)     
    except:
        print("return")
        return 0

cap = cv2.VideoCapture(0)
# inicializa o cv2 detector de qrcode
detector = cv2.QRCodeDetector()
teste=0

while True:
    data = teste
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    if data != teste:    
        if data:
            a=data
            callwebcan(a)

    #termina programa com comando s
    cv2.imshow("QRCODEscanner", img)    
    if cv2.waitKey(1) == ord("s"):
        break

