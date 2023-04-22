#!/usr/bin/python
# -*- coding: utf-8 -*-
import ftplib, optparse


def paginasPadrao(ftp):
    try:
        lista_diretorios = ftp.nlst()
    except:
        lista_diretorios = []
        print '[-] Não foi possível listar o conteúdo.'
        return

    lista_arquivos = []
    for fileName in lista_diretorios:
        fn = fileName.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn:
            print '[+] Encontrado a página padrão: ' + fileName
            lista_arquivos.append(fileName)
    return lista_arquivos


def inicio():
    analisador = optparse.OptionParser('use paginas_padrao_ftp '+\
      '-H <host alvo> -p <porta(s) alvo>')
    analisador.add_option('-H', dest='host', type='string',\
      help='especifique o host alvo')
    analisador.add_option('-u', dest='usuario', type='string',\
      help='especifique o usuario alvo')
    analisador.add_option('-s', dest='senha', type='string',\
      help='especifique a senha do usuario alvo')

    (opcoes, args) = analisador.parse_args()

    host = opcoes.host
    usuario = opcoes.usuario
    senha = opcoes.senha

    if (host == None) | (usuario == None) | (senha == None):
        print analisador.usage
        exit(0)

    ftp = ftplib.FTP(host)
    ftp.login(usuario, senha)
    paginasPadrao(ftp)

if __name__ == '__main__':
    inicio()