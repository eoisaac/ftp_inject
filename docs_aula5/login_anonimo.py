#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib, optparse

def loginAnonimo(host_alvo):
    try:
        ftp = ftplib.FTP(host_alvo, timeout=5)
        ftp.login('anonymous', 'anonymous')
        print '[*] ' + host_alvo + ' FTP Login Anonimo Sucesso.'
        ftp.quit()
        return True
    except Exception, e:
        print '[-] ' + host_alvo + ' FTP Login Anonimo Falhou.'
    return False

def inicio():
    analisador = optparse.OptionParser('use login_anonimo '+\
      '-H <host alvo>')
    analisador.add_option('-H', dest='host', type='string',\
      help='especifique o host alvo')

    (opcoes, args) = analisador.parse_args()

    host = opcoes.host

    if (host == None):
        print analisador.usage
        exit(0)

    loginAnonimo(host)


if __name__ == '__main__':
    inicio()