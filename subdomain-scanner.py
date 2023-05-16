# -*- coding: utf-8 -*-
import os, sys
import dns.resolver
import socket
import platform
import time
from colorama import Fore, Back, init
init()

# Limpia todo el contenido de la pantalla
# ===============================================
def limpiar_pantalla():
    nombre_sistema = platform.system()
    if nombre_sistema == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Retorna la fecha del sistema
# ================================================
def fecha():
    return time.strftime('Fecha: %d/%m/%Y')

# Definir la lista de subdominios
# ================================================
def subdominios_lista():
    my_file = open('diccionario1.txt', 'r')
    data = my_file.read()
    subdomains = data.split('\n')
    return subdomains

limpiar_pantalla()
print(Back.RED + Fore.WHITE + '\n Subdomain-Scanner ' + Back.WHITE + Fore.BLUE + '\n\n' + fecha() + '\n')

# Definir el dominio principal
domain = sys.argv[1]

# Resolver el dominio principal para obtener su valor PTR
try:
    answers = dns.resolver.resolve(domain, 'PTR')
    ptr_values = [answer.to_text() for answer in answers]
    if ptr_values:
        print(Back.BLACK + Fore.YELLOW + f'Dominio principal: {domain}')
        print(f'Valor PTR: {", ".join(ptr_values)}')
        print('---')
except dns.resolver.NXDOMAIN:
    pass
except dns.resolver.NoAnswer:
    print(Back.BLACK + Fore.YELLOW + f'Dominio principal: {domain}')
    print('Valor PTR: No se encontró valor PTR')
    print('---')
except Exception as e:
    print(f'Error al resolver el dominio principal: {str(e)}')
    print('---')
    
subdomains = subdominios_lista()
# Recorrer la lista de subdominios
for subdomain in subdomains:
    # Componer el nombre completo del subdominio
    full_domain = subdomain + '.' + domain

    try:
        answers = dns.resolver.resolve(full_domain, 'A')

        found = False
        cname_values = []

        for answer in answers:
            if answer.rdtype == dns.rdatatype.A:
                found = True
                ip_address = answer.to_text()

                try:
                    ptr_values = socket.gethostbyaddr(ip_address)[0]
                    ptr_value = ', '.join(ptr_values)
                    ptr_value = ptr_value.replace(',', '').replace(' ', '') # Eliminar las comas y espacios
                except socket.herror:
                    ptr_value = 'No se encontró valor PTR'

                print(Back.BLACK + Fore.GREEN +f'Subdominio: {full_domain}')
                print(f'Encontrado: Sí')
                print(f'Valor PTR: {ptr_value}')
                print('Destino: ' + ip_address)
                print('---')
                listado = list(answers)

            elif answer.rdtype == dns.rdatatype.CNAME:
                cname_value = answer.target.to_text().strip('.')
                cname_values.append(cname_value)

        if cname_values:
            print(Back.BLACK + Fore.GREEN +f'Subdominio: {full_domain}')
            print(f'Encontrado: Sí')
            print(f'Valores CNAME: {", ".join(cname_values)}')
            print('Destino: ' + ip_address)
            print('---')
                
    except dns.resolver.NXDOMAIN:
        pass

    except Exception as e:
        print(f'Error al resolver {full_domain}: {str(e)}')
