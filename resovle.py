import re
import socket


def get_ip_address(domain):
    try:
        domain_encoded = domain.encode('idna').decode()  # Encode domain name using 'idna'
        server_ip = socket.gethostbyname(domain_encoded)
        return server_ip
    except socket.gaierror:
        return None

domain = 'https://aspb2.cdn.asset.aparat.com/aparat-video/0bdd921b6dbbf60ec4b2b6ec0828e4258360240-144p.apt/s-1-v1-a1.ts?wmsAuthSign=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IjYxNWQ1YzAzMWRmNDFjZTA3ZTdmYWY0MGQ4OTA1NDMwIiwiZXhwIjoxNjg1MTY4NjkyLCJpc3MiOiJTYWJhIElkZWEgR1NJRyJ9.nQl0FzTi50jJCXq_XdbOoUKtalNCTBtnBpyUMNLzsnA'
domain = domain.split("/")[1].split("aparat.com")[0] + "aparat.com"
ip_address = get_ip_address(domain)
if ip_address is not None:
    print(f"The IP address of {domain} is {ip_address}")
else:
    print(f"Failed to resolve IP address for {domain}")