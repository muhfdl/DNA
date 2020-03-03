import paramiko
import time

devices = [
    {
        'ip_address' : '192.168.22.10',
        'vendor' : 'cisco',
        'username' : 'fadil',
        'password' : 'F4dil'
    },
    {
        'ip_address' : '192.168.22.20',
        'vendor' : 'cisco',
        'username' : 'fadil',
        'password' : 'F4dil'
    },
    {
        'ip_address' : '192.168.22.30',
        'vendor' : 'cisco',
        'username' : 'fadil',
        'password' : 'F4dil'
    },
    {
        'ip_address' : '192.168.22.40',
        'vendor' : 'cisco',
        'username' : 'fadil',
        'password' : 'F4dil'
    }
]

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for device in devices:
    ssh_client.connect(hostname=device['ip_address'],username=device['username'], password=device['password'])
    print("\nResult on {}".format(device['ip_address']))

    if device['vendor'] == 'cisco':
        conn = ssh_client.invoke_shell()
        conn.send('terminal length 0\n')
        conn.send("show ip int br\n")
        time.sleep(5)
        
        output = conn.recv(65535)
        print(output.decode())
       
    ssh_client.close()