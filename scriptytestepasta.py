import json
import re

from enum import Enum
import subprocess

JSON_INFO = None

CONF_INFO = None

def exec_cache_existente():
    try:
        print_collor_green('-> Verificando tipo de equipamento                ')
        path_file = JSON_INFO['PATHS']['CONFIG_JARVISENV']
        with open(path_file, 'r') as arquivo:  
            if  'cat: /etc/cloudpark/config.yml"' in arquivo:
                print_collor_blue('     -> Equiapamento tipo CAIXA                  ')   
            else:
                print_collor_blue('     -> Equiapamento tipo PI                     ')   
                load_config_jarvis_env()
    except:
        print_collor_red('-> Erro ao carregar json de informações           ')   


def inicialize_config():
    print_collor_green('-> Inicializando criação de json informações.     ')
    try:
        global JSON_INFO
        global CONF_INFO
        
        config_path = {
            'PATHS': {
                'SYS_JARVIS_ENV': '/etc/cloudpark/jarvisenv/',
                'SYS_HARDWARE': '/opt/cloudpark/hardware',
                'SYS_SERVER': '/opt/cloudpark/cloudpark',
                'SYS_PAYMENT': '/opt/cloudpark/payment/',
                'SYS_LCD': '',
                'SYS_ALPR': '/opt/cloudpark/alpr/',
                'LOG_HARDWARE_ENTRANCE': '/var/log/cloudpark/entrance.log',
                'LOG_HARDWARE_EXIT': '/var/log/cloudpark/exit.log',
                'LOG_SERVER': '/var/log/cloudpark/logging.log',
                'LOG_JARVIS': '/var/log/cloudpark/jarvis.log',
                'LOG_LCD': '/var/log/cloudpark/lcd.log',
                'LOG_VALIDATOR': '/var/log/cloudpark/validator.log',
                'CONFIG_JARVISENV': '/etc/cloudpark/jarvis.env',
                'CONFIG_HARDWARE': '/etc/cloudpark/config.yml',
                'CONFIG_HARDWARE_OLD': '/etc/cloudpark/config.py',
                'CONFIG_PAYMENT': '/etc/cloudpark/payment.yml'
            },
            'HAS_JARVISTMP': False,                    
            'JARVIS_INSTALLED': False,
            'JARVIS_ENV': {
                'IS_SERVER': False, 
                'HAS_HARDWARE': False,
                'HAS_PAYMENT': False,
                'HAS_ALPR': False,
                "HAS_LCD": False,
                'HAS_ALPR': False,
            },
            'CONFIG':{
                'STAMP':False,
            },
            'MACHINE': {
                'HOSTNAME': '',
                'LOCAL_IP': '',
                'DNS':'',
                'IP_FIXO':False,
                'ROUTE':'',
                'EXIST_SQLITE3': False,
                'DATE': '',
                'USED_SWAP': False,
            }
        }
        JSON_INFO = config_path  
        
        config_comand = {
                'COMMAND':{
                    'TESTE_PING':'ping -c 2 -w 2 google.com',
                    'JARVIS_STATUS ':'sudo service cloudpark-jarvis status',
                    'DATE':'sudo date',
                    'LOG_JARVIS':'sudo tail -50 /var/log/cloudpark/jarvis.log',
                    'CLEAR_SWAP':'sudo swapoff -a ; sudo swapon -av',
                    'CHECK_SWAP':'free -h',
                    'LS':'ls',
                    'JARVIS_MACHINES':'sudo jarvis machines',
                    'JARVIS_IP':'sudo jarvis ip',
                    'VERSION_CASHIER':'sudo dpkg -s cloudpark-desktop',
                }
        }
        CONF_INFO = config_comand  
        
        print_collor_green('-> Finalizando criação de json informações.       ')
    except:
        print_collor_red('-> Erro ao criar json de informações              ')
        
       
def load_config_jarvis_env():
    print_collor_green('-> Iniciando carregamento de json informações...  ')
    try:
        global JSON_INFO
        path_file = JSON_INFO['PATHS']['CONFIG_JARVISENV']   
        with open(path_file, 'r') as arquivo:
            conteudo = arquivo.read()
            JSON_INFO['JARVIS_ENV']['IS_SERVER'] = 'IS_SERVER=True' in conteudo
            JSON_INFO['JARVIS_ENV']['HAS_HARDWARE'] = 'HAS_HARDWARE=True' in conteudo
            JSON_INFO['JARVIS_ENV']['HAS_PAYMENT'] = 'HAS_PAYMENT=True' in conteudo
            JSON_INFO['JARVIS_ENV']['HAS_LCD'] = 'HAS_LCD=True' in conteudo
            JSON_INFO['JARVIS_ENV']['JARVIS_DIR'] = 'HAS_ALPR=/opt/cloudpark/jarvis/' in conteudo
            JSON_INFO['JARVIS_ENV']['HARDWARE_DIR'] = 'HAS_ALPR=/opt/cloudpark' in conteudo
            JSON_INFO['JARVIS_ENV']['PAYMENT_TOTEM_DIR'] = 'PAYMENT_TOTEM_DIR=/opt/cloudpark/payment_totem/' in conteudo
        print_collor_green('-> Finalizando carregamento de json informações...')        
    except:        
      
        print_collor_red('-> Erro ao carregar json de informações           ')        
 
 
def get_ip_info():
    print_collor_green('-> Obtendo informações referente a machines...    ')
    try:
        global JSON_INFO, CONF_INFO
        command = CONF_INFO['COMMAND']['JARVIS_IP'] 
        print(command)
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        ip_match = re.search(r'IP:\s*([\d.]+)', output)
        dns_match = re.search(r'DNS:\s*([\d.]+)', output)
        if ip_match:
            JSON_INFO['MACHINE']['LOCAL_IP'] = ip_match.group(1)
        if dns_match: 
            JSON_INFO['MACHINE']['DNS'] = dns_match.group(1)
        JSON_INFO['MACHINE']['IP_FIXO'] = 'O IP está fixo' in output
         
        
        # Reescreve o JSOpath_fileN no arquivo
        with open(command, 'w') as arquivo:
            json.dump(JSON_INFO, arquivo, indent=4)
    except Exception as e:
        print_collor_red('-> Erro ao obter informações referente a machines:', e)
 
def get_router_default():
    
    
# CONFIG FOR PRINT

class ColorPrint(Enum):
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    WHITE = '\033[0m'
    BLUE = '\033[34m'

def print_dict_with_format(data, title):
    if data:
        print("-" * 8)
        print(title.upper() + ":")
        print("-" * 15)
        for key, value in data.items():
            if isinstance(value, bool):
                value_str = "\033[92mTrue\033[0m" if value else "\033[91mFalse\033[0m"
            else:
                value_str = "\033[91mN/A\033[0m" if value == "N/A" else value
            print(f"{key} -> {value_str}")
        print("-" * 8)
    else:
        print(f"No data found for {title.upper()}.")

def print_result():    
    global JSON_INFO    
    global CONF_INFO
    print_dict_with_format(JSON_INFO.get('JARVIS_ENV'), 'JARVIS_ENV')
    print_dict_with_format(JSON_INFO.get('MACHINE'), 'MACHINE')  

def print_collor_yellow(text):
     print(f'{ColorPrint.YELLOW.value}{text}{ColorPrint.WHITE.value}')    

def print_collor_green(text):
     print(f'{ColorPrint.GREEN.value}{text}{ColorPrint.WHITE.value}') 
        
def print_collor_red(text):
    print(f'{ColorPrint.RED.value}{text}{ColorPrint.WHITE.value}')   
    
def print_collor_blue(text):
    print(f'{ColorPrint.BLUE.value}{text}{ColorPrint.WHITE.value}')
    
# MAIN 

def main():
    print_collor_yellow("-" * 50)
    print_collor_yellow('     Validador de integridade de equipamento      ')
    print_collor_yellow("-" * 50)
    

    inicialize_config()
    exec_cache_existente()
    get_ip_info()
    # load_config_jarvis_env()    
    

    print_collor_yellow("-" * 50)

    print_result() 

    print_collor_yellow("-" * 50)

if __name__ == "__main__":
    main()
