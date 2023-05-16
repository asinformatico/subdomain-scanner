# -*- coding: utf-8 -*-
import sys
import dns.resolver
import socket

# Definir la lista de subdominios
my_file = open('diccionario1.txt', 'r')
data = my_file.read()
subdomains = data.split('\n')

# Definir el dominio principal
domain = sys.argv[1]

# Resolver el dominio principal para obtener su valor PTR
try:
    answers = dns.resolver.resolve(domain, 'PTR')
    ptr_values = [answer.to_text() for answer in answers]
    if ptr_values:
        print(f'Dominio principal: {domain}')
        print(f'Valor PTR: {", ".join(ptr_values)}')
        print('---')
except dns.resolver.NXDOMAIN:
    pass
except dns.resolver.NoAnswer:
    print(f'Dominio principal: {domain}')
    print('Valor PTR: No se encontró valor PTR')
    print('---')
except Exception as e:
    print(f'Error al resolver el dominio principal: {str(e)}')
    print('---')

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

                print(f'Subdominio: {full_domain}')
                print(f'Encontrado: Sí')
                print(f'Valor PTR: {ptr_value}')
                print('---')

            elif answer.rdtype == dns.rdatatype.CNAME:
                cname_value = answer.target.to_text().strip('.')
                cname_values.append(cname_value)

        if cname_values:
            print(f'Subdominio: {full_domain}')
            print(f'Encontrado: Sí')
            print(f'Valores CNAME: {", ".join(cname_values)}')
            print('---')

    except dns.resolver.NXDOMAIN:
        pass

    except Exception as e:
        print(f'Error al resolver {full_domain}: {str(e)}')
