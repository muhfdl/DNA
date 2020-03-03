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
    print("\nSuccess login to {}".format(device['ip_address']))

    if device['vendor'] == 'cisco':
        conn = ssh_client.invoke_shell()
        conn.send("conf t\n")
        conn.send("int lo1\n")
        conn.send("ip add 10.10.10.10 255.255.255.255\n")
        time.sleep(1)
        
        output = conn.recv(65535)
        print(output.decode())
       
    ssh_client.close()