from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Device, Log
import paramiko
from datetime import datetime
import time


def home(request):
    all_device = Device.objects.all()
    cisco_device = Device.objects.filter(vendor="cisco")
    last_event = Log.objects.all().order_by('-id')[:10]
    
    context = {
        'all_device': len(all_device),
        'cisco_device': len(cisco_device),
        'last_event': last_event
    }
    return render(request, 'home.html', context)

def devices(request):
    all_device = Device.objects.all()

    context = {
        'all_device': all_device
    }

    return render(request, 'devices.html', context)

def configure(request):
    if request.method == "POST":
        selected_device_id = request.POST.getlist('device')
        cisco_command = request.POST['cisco_command'].splitlines()
        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip_address,username=dev.username,password=dev.password)

                if dev.vendor.lower() == 'cisco':
                    conn = ssh_client.invoke_shell()
                    conn.send("conf t\n")
                    for cmd in cisco_command:
                        conn.send(cmd + "\n")
                        time.sleep(1)
                
                log = Log(target=dev.ip_address, action="Configure", status="Success", time=datetime.now(), messages="No Error")
                log.save()  

            except Exception as e:
                log = Log(target=dev.ip_address, action="Configure", status="Error", time=datetime.now(), messages=e)
                log.save()
        return redirect('home')

    else:
        devices = Device.objects.all()
        context = {
            'devices': devices,
            'mode': 'Configure'
        }
        return render(request, 'config.html', context)
       
def verify_config(request):
    if request.method == "POST":
        result = []
        selected_device_id = request.POST.getlist('device')
        cisco_command = request.POST['cisco_command'].splitlines()
        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip_address,username=dev.username,password=dev.password)

                if dev.vendor.lower() == 'cisco':
                    conn = ssh_client.invoke_shell()
                    conn.send('terminal length 0\n')
                    for cmd in cisco_command:
                        result.append("Result on {}".format(dev.ip_address))
                        conn.send(cmd + "\n")
                        time.sleep(5)
                        output = conn.recv(65535)
                        result.append(output.decode())
            
                log = Log(target=dev.ip_address, action="Verify Config", status="Success", time=datetime.now(), messages="No Error")
                log.save()  

            except Exception as e:
                log = Log(target=dev.ip_address, action="Verify Config", status="Error", time=datetime.now(), messages=e)
                log.save()

        result = '\n'.join(result)
        return render(request, 'verify-result.html', {'result':result})

    else:
        devices = Device.objects.all()
        context = {
            'devices': devices,
            'mode': 'Verify Config'
        }
        return render(request, 'config.html', context)

def upgrade_ios(request):
    if request.method == "POST":
        result = []
        selected_device_id = request.POST.getlist('device')
        cisco_command = request.POST['cisco_command'].splitlines()
        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip_address,username=dev.username,password=dev.password)

                if dev.vendor.lower() == 'cisco':
                    conn = ssh_client.invoke_shell()
                    for cmd in cisco_command:
                        result.append("Result on {}".format(dev.ip_address))
                        conn.send(cmd + "\n")
                        time.sleep(150)
                        output = conn.recv(65535)
                        result.append(output.decode())
                
                log = Log(target=dev.ip_address, action="Upgrade IOS", status="Success", time=datetime.now(), messages="No Error")
                log.save()  

            except Exception as e:
                log = Log(target=dev.ip_address, action="Upgrade IOS", status="Error", time=datetime.now(), messages=e)
                log.save()

        result = '\n'.join(result)
        return render(request, 'verify-result.html', {'result':result})

    else:
        devices = Device.objects.all()
        context = {
            'devices': devices,
            'mode': 'Verify IOS'
        }
        return render(request, 'upgrade-ios.html', context)

def log(request):
    logs = Log.objects.all()

    context = {
        'logs': logs
    }

    return render(request, 'log.html', context)