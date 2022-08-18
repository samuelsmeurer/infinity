import mysql.connector
import pymysql.cursors
import cv2
import webbrowser
import datetime
import time
from cryptography.fernet import Fernet


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
print(dados)
print('\n')





ticketusado = list()
#realiza conexão no banco de dados
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
    print('Impossível se conectar ao Banco de Dados!', title='Erro de conexão',text_color=(cor_branco))

'''with conexao.cursor() as cursor:
    cursor.execute('select * from ticket')
    estoque = cursor.fetchall()

print(estoque)
'''
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
                print('ACESSO NEGADO!!! O ticket {} já foi utilizado no dia {} '.format(x,ticketusado[i][2]))
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
            print('O seu ingresso "{}" acabou de ser utilizado!'.format(data))
            time.sleep(5)     
    except:
        print("return")
        return 0
cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()
teste=0

while True:
    data = teste
    _, img = cap.read()
    # detect and decode
    data, bbox, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
    if data != teste:    
        if data:
            a=data
            callwebcan(a)


    cv2.imshow("QRCODEscanner", img)    
    if cv2.waitKey(1) == ord("s"):
        break




'''
b=webbrowser.open(str("https://polygonscan.com/address/"+a))

cv2.destroyAllWindows()
'''

