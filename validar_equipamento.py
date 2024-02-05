import os
import subprocess
import re



CURRENT_CORRECT_VERSION_CASHIER = '23.10.2'
COMMAND_JARVIS_ENV = 'cat /etc/cloudpark/jarvis.env'
COMMAND_VERSION_CASHIER = 'sudo dpkg -s cloudpark-desktop'
COMMAND_JARVIS_IP = 'sudo jarvis ip'
COMMAND_JARVIS_MACHINES = 'sudo jarvis machines'
COMMAND_LS = 'ls'
COMMAND_SWAP = 'free -h'
COMMAND_CLEAR_SWAP = 'sudo swapoff -a ; sudo swapon -av'
COMMAND_LOG_JARVIS = 'sudo tail -50 /var/log/cloudpark/jarvis.log'
COMMAND_DATE = 'sudo date'
COMMAND_JARVIS_STATUS = 'sudo service cloudpark-jarvis status'
COMMAND_TEST_PING = 'ping -c 2 -w 2 google.com'



LINK_UPPDATE_VERSION_CHASHIER= 'https://s3.sa-east-1.amazonaws.com/ferramentas.cloudpark.com.br/caixa/cloudpark-desktop_23.10.2_amd64.deb"'


script_content_pi = """ 
#!/bin/sh
resultado=$(wget https://s3-sa-east-1.amazonaws.com/ferramentas.cloudpark.com.br/app.zip);
if [ -e app.zip ]; then
echo "Baixamos o jarvis"
sudo mv app.zip /opt/jarvistmp
cd /opt/jarvistmp && sudo unzip app.zip
echo "Jarvis está pronto =)"
else
echo "Não consegui baixar o Jarvis =/"
fi
"""
script_content_caixa = """
#!/bin/sh
resultado=$(wget https://s3-sa-east-1.amazonaws.com/ferramentas.cloudpark.com.br/jarvis_x86/app.zip);
if [ -e app.zip ]; then
echo "Baixamos o jarvis"
sudo mv app.zip /opt/jarvistmp
cd /opt/jarvistmp && sudo unzip app.zip
echo "Jarvis está pronto =)"
else
echo "Não consegui baixar o Jarvis =/"
fi
"""


is_server:None
jarvis_dir:None
access_dir:None
ip:None
fixed_ip:True

variables_to_check_jarvis_env = [
    {'IS_SERVER': 'is_server'},
    {'HAS_HARDWARE': 'has_hardware'},
    {'HARDWARE_VERSION': 'hardware_version'},
    {'CLOUDPARK_VERSION': 'cloudpark_version'},
    {'HAS_PAYMENT': 'has_payment'},
    {'HAS_ALPR': 'has_alpr'},
    {'LCD_VERSION': 'lcd_version'},
    {'JARVIS_DIR':''},
    {'ACCESS_DIR':''}
]


results_list = []

def exec_cache_existence():
    print("\n-----------------------------------------------\n")
    print("\n----------------------PI-----------------------\n")
    try:
        result = subprocess.check_output(COMMAND_JARVIS_ENV, shell=True).decode('utf-8')
        if "cat: /etc/cloudpark/config.yml" in result:
            print("\n---------------------CAIXA---------------------\n")
            print("\n-----------------------------------------------\n")
            exec_validation_version_cashier(result)
        else:
            results_info_jarvis_env(result)

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def results_info_jarvis_env(result):
    try:
        print("\n-----------------------------------------------\n")
        print("\n----------------------PI-----------------------\n")

        for variable in variables_to_check_jarvis_env:
            get_value_from_file(result, variable)

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def get_value_from_file(result, variable):
    for key, value in variable.items():
        match = re.search(fr'{key}=(\S+)', result, re.IGNORECASE)
        if match:
            globals()[value] = match.group(1) == 'TRUE'
            print(f"{key}: {match.group(1)}")
        else:
            print(f'{key}: N/A')
            
def exec_validation_version_cashier():
    try:
        result = subprocess.check_output(COMMAND_VERSION_CASHIER, shell=True).decode('utf-8')
        match = re.search(r'"Version":\s*"(\d+\.\d+\.\d+)"', result)
        if match and match.group(1) != CURRENT_CORRECT_VERSION_CASHIER:
            print(match.group(1))
            """update_version_cashier()"""
        else:
            print("VERSION CAIXA=" + match)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def update_version_cashier():
    try:
        
        subprocess.check_output(['wget', LINK_UPPDATE_VERSION_CHASHIER]).decode('utf-8')
        subprocess.check_output(['sudo', 'dpkg', '--purge', 'cloudpark-desktop']).decode('utf-8')
        subprocess.check_output(['sudo', 'apt-get', 'update'])
        subprocess.check_output(['sudo', 'dpkg', '-i','cloudpark-desktop_'+CURRENT_CORRECT_VERSION_CASHIER+'_amd64.deb'])
        subprocess.check_output(['sudo', 'nano', '~/.config/autostart/cloudpark.desktop'])
        print("\n---------------CAIXA ATUALIZADO----------------\n")
        
    except Exception as e:
        print(f"Erro inesperado: {e}")

def get_ip_info():
    global fixed_ip,ip
    try:
        result = subprocess.check_output(COMMAND_JARVIS_IP, shell=True).decode('utf-8')
        ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', result)
        if ip_match:
            global_ip_address = ip_match.group(1)
            ip = global_ip_address
            print("\n----------------------IP-----------------------")
            print("IP:"+ ip)
            if "O IP está fixo" in result:
                print("IP Fixo: TRUE")
            else:
                print("IP Fixo: FALSE")
                fixed_ip = False
            print("-----------------------------------------------")                 
        else:
            print("Não foi possível encontrar o endereço IP no resultado.")
    
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def print_jarvis_machines():
    print("\n----------------JARVIS MACHINES-_--------------\n")
    result = subprocess.check_output(COMMAND_JARVIS_MACHINES, shell=True).decode('utf-8')
    print(result)


def print_date():
    result = subprocess.check_output(COMMAND_DATE, shell=True).decode('utf-8')
    print("DATA= " + result)


def print_has_share():
    result = subprocess.check_output(COMMAND_LS, shell=True).decode('utf-8')
    print("SHARE= EXISTE!! " if "share" in result else "SHARE= N/A")


def exec_validation_swap():
    result = subprocess.check_output(COMMAND_SWAP, shell=True).decode('utf-8')
    swap_line = [line for line in result.split('\n') if 'Swap' in line][0]
    used_swap = subprocess.check_output(['awk', '{print $3}', '/dev/stdin'], input=swap_line.encode('utf-8')).decode('utf-8').strip()
    if used_swap == '0B':
        print("SWAP= VAZIO")
    else:
        print("SWAP= EM USO")
        clean_swap()

def clean_swap():
    try:
        print("\n-----------------LIMPANDO SWAP-----------------\n")
        result = subprocess.check_output(COMMAND_CLEAR_SWAP, shell=True).decode('utf-8')
        print(result)
        print("-------------------TERMINOU--------------------\n")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def print_log_jarvis():
    try:
        print("\n-----------------LOG JARVIS OK?-----------------\n")
        result = subprocess.check_output(COMMAND_LOG_JARVIS, shell=True).decode('utf-8')
        print(result)
        print("-------------------TERMINOU--------------------")
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def exec_jarvis_status():
        result = subprocess.check_output(COMMAND_JARVIS_STATUS, shell=True).decode('utf-8')
        if"running" in result:
            print("JARVIS INSTALADO")
            print_log_jarvis()
        else :
            print("JARVIS N/A")
            
def print_test_internet_connection():
    result = subprocess.check_output(COMMAND_TEST_PING, shell=True).decode('utf-8')
    if "PING google.com" in result:
         print("INTERNETC= CONECTADO")
    else:
        print("INTERNETC= N/A") 

def jarvis_installed():
    try:
        result = subprocess.check_output(['sudo', 'service', 'cloudpark-jarvis', 'status']).decode('utf-8')
        if "running" in result:
            print("JARVIS INSTALADO")
            print_log_jarvis()
        else:
            print("JARVIS N/A")
        "installing_jarvis()"
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

         
def installing_jarvis():
    try:
        subprocess.check_output(['sudo', 'rm', '-r', '/opt/jarvistmp/']).decode('utf-8')
    except subprocess.CalledProcessError:
        pass

    subprocess.check_output(['sudo', 'mkdir', '-p', '/opt/jarvistmp/']).decode('utf-8')
    
    with open("get-jarvis.sh", "w") as arquivo:
        arquivo.write(script_content_pi)
    
    os.chmod("get-jarvis.sh", 0o755)


        
""" def print_exists_sqlite3():
    result = subprocess.check_output(['sqlite3']).decode('utf-8')
    if "SQLite version" in result:
         print("SQLite= TRUE")
    else:
        print("SQLite= FALSE") """

def main():
    get_ip_info()
    jarvis_installed()
    exec_cache_existence()
    print_date()
    print_has_share() 
    exec_validation_swap()
    print_test_internet_connection() 
    print_jarvis_machines()
    """for result in results_list:
        print(result) """
    
if __name__ == "__main__":
    main()

