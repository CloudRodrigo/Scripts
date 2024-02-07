import re
import subprocess




from enum import Enum

JSON_INFO = None
CONF_INFO = None
INCOMPATIBILIRIES = None
LOG_JARVIS= None

def exec_cache_existente():
    try:
        print_collor_orange('-> Verificando tipo de equipamento                ')
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
    print_collor_orange('-> Inicializando criação de json informações.     ')
    try:
        global JSON_INFO
        global CONF_INFO
        global INCOMPATIBILIRIES
        
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
                'CONFIG_PAYMENT': '/etc/cloudpark/payment.yml',
                'CONFIG_HOSTNAME':'/etc/hostname'
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
                'USE_SHARE': False
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
                'USE_SWAP':False,
                'EXIST_SHARE': False,
                'INTERNET': False,
                'RUNNING_JARVIS':False,
                'LOG_JARVIS_OK':False
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
                    'GET_IP_ROUTER':'ip route | grep default',
                    'JARVIS_MACHINES':'sudo jarvis machines',
                    'JARVIS_IP':'sudo jarvis ip',
                    'VERSION_CASHIER':'sudo dpkg -s cloudpark-desktop',
                    'DELETE_SHARE':'sudo rm -r ./share'
                }
        }
        CONF_INFO = config_comand  
        
        
        no_compliant = {
            'DIVERGENC': set()
        }
        INCOMPATIBILIRIES = no_compliant
        
        print_collor_orange('-> Finalizando criação de json informações.       ')
    except:
        print_collor_red('-> Erro ao criar json de informações              ')


       
def load_config_jarvis_env():
    print_collor_orange('-> Iniciando carregamento de json informações...  ')
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
            JSON_INFO['JARVIS_ENV']['USE_SHARE'] = 'share' in conteudo
        print_collor_green('-> Finalizando carregamento de json informações...')        
    except:        
      
        print_collor_red('-> Erro ao carregar json de informações           ')        
 
 
def get_ip_info():
    try:
        print_collor_orange('-> Iniciando obtenção de ip machines              ')
        global JSON_INFO, CONF_INFO
        print_collor_blue('    -> Obtendo dados do jarvis ip                ')
        command = CONF_INFO['COMMAND']['JARVIS_IP'] 
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        ip_match = re.search(r'IP:\s*([\d.]+)', output)
        dns_match = re.search(r'DNS:\s*([\d.]+)', output)
        if ip_match:
            JSON_INFO['MACHINE']['LOCAL_IP'] = ip_match.group(1)
        if dns_match: 
            JSON_INFO['MACHINE']['DNS'] = dns_match.group(1)
            get_router_default()
        JSON_INFO['MACHINE']['IP_FIXO'] = 'O IP está fixo' in output
        
        if not JSON_INFO['MACHINE']['IP_FIXO']:
            INCOMPATIBILIRIES['DIVERGENC'].add('TEM QUE FIXAR IP')
        
        print_collor_green('-> Finalizando obtenção de ip machines              ')
    except:
        print_collor_red('-> Erro ao obter informações referente a machines:')
 

def get_router_default():
    try:
        print_collor_blue('    -> Obtendo ip router                          ')
        global JSON_INFO, CONF_INFO
        command = CONF_INFO['COMMAND']['GET_IP_ROUTER'] 
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        lines = output.split('\n')
        for line in lines:
            if 'default via' in line:
                router_ip = line.split(' ')[2]
                JSON_INFO['MACHINE']['ROUTE'] = router_ip     
        print_collor_green('    -> Finalização obter ip router                ')
    except:
        print_collor_red('-> Erro ao obter informações do IP do route       ')

def get_machine_data():
    print_collor_orange('-> Verificando data e hora da maquina             ')
    try:
        global JSON_INFO, CONF_INFO
        command = CONF_INFO['COMMAND']['DATE'] 
        output = subprocess.check_output(command, shell=True, universal_newlines=True).strip()
        JSON_INFO['MACHINE']['DATE'] = output
        print_collor_green('-> Finalizando data e hora da maquina')
    except:
        print_collor_red('-> Erro ao obter informações do IP do roteador padrão:')

def get_hostname_machines():
    print_collor_orange('-> Obtendo hostname da maquina                    ')
    try:
        global JSON_INFO
        path_file = JSON_INFO['PATHS']['CONFIG_HOSTNAME']   
        with open(path_file, 'r') as arquivo:
            conteudo = arquivo.read().strip() 
        JSON_INFO['MACHINE']['HOSTNAME'] = conteudo
        print_collor_green('-> Finalizando obtenção do hostname               ')
    except:
        print_collor_red('-> Erro ao obter hostname                         ')
        
def get_if_has_share():
    global JSON_INFO, CONF_INFO
    print_collor_orange('-> Verificar existencia da pasta share            ')
    try:
        command = CONF_INFO['COMMAND']['LS']
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        JSON_INFO['MACHINE']['EXIST_SHARE'] = 'share' in output  # Verifica se 'share' está presente no output
        if JSON_INFO['MACHINE']['EXIST_SHARE']:
            print_collor_red('-> Pasta share foi encontrada')
            if not JSON_INFO['JARVIS_ENV']['USE_SHARE']:
                confirm = input('Você tem certeza que deseja excluir a pasta share? (Digite "sim" para confirmar): ')
                if confirm.lower() == 'sim':
                    delete_share_folder()
                    print_collor_orange("    -> Finalizando remoção da pasta share         ")
                else:
                    print_collor_blue('-> Exclusão da pasta share cancelada.')
            else:
                print_collor_red('      -> Pasta share está sendo usada             ')
        print_collor_green('-> Finalizando verificação se existe pasta share  ')
    except:
        print_collor_red('-> Erro ao verificar existencia da pasta share   ')

def delete_share_folder():
    global CONF_INFO, INCOMPATIBILIRIES
    print_collor_blue('     -> Removendo pasta share                    ')
    try:
        command = CONF_INFO['COMMAND']['DELETE_SHARE']
        subprocess.check_output(command, shell=True, universal_newlines=True)
        INCOMPATIBILIRIES['DIVERGENC'].add('PASTA SHARE REMOVIDA')
    except:
        print_collor_red("-> Erro ao deletar pasta share")
        
def exec_validation_swap():
    global JSON_INFO, CONF_INFO
    print_collor_orange('-> Verificar uso do swap                          ')
    try:
        command = CONF_INFO['COMMAND']['CHECK_SWAP']
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        swap_line = [line for line in output.split('\n') if 'Swap' in line][0]
        used_swap = subprocess.check_output(['awk', '{print $3}', '/dev/stdin'], input=swap_line.encode('utf-8')).decode('utf-8').strip()
        JSON_INFO['JARVIS_ENV']['IS_SERVER'] = '0B' not in used_swap
        if JSON_INFO['JARVIS_ENV']['IS_SERVER']:
            clear_swap()
        print_collor_green('-> Finalizando verificar uso do swap                          ')
    except:
         print_collor_red('-> Erro ao verificar uso do swap                  ')
   
def clear_swap():
    global CONF_INFO, INCOMPATIBILIRIES
    print_collor_blue('         -> Iniciando limpeza do SWAP             ')
    try:
        command = CONF_INFO['COMMAND']['CLEAR_SWAP']
        subprocess.check_output(command, shell=True, universal_newlines=True)
        INCOMPATIBILIRIES['DIVERGENC'].add('LIMPEZA SWAP')
        print_collor_green('         -> Finalizando limpeza do SWAP             ')   
    except:
        print_collor_red("-> Erro ao executar limpeza de swap               ")

def get_test_internet_connection():
    global CONF_INFO, INCOMPATIBILIRIES
    print_collor_orange("-> Verificação de internet...                     ")
    try:
        command = CONF_INFO['COMMAND']['TESTE_PING']
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        JSON_INFO['MACHINE']['INTERNET'] ='PING google.com' in output;
        if not JSON_INFO['MACHINE']['INTERNET']:
            INCOMPATIBILIRIES['DIVERGENC'].add('SEM CONEXAO A INTERNET')
            print_collor_red("      -> Sem conexão com a internet               ")
        print_collor_green("-> Finalizando verificação internet               ")
    except:
        print_collor_red('-> Erro ao tentar verificar conexão com a internet')    

def exec_jarvis_status():
    global CONF_INFO, INCOMPATIBILIRIES
    print_collor_orange("-> Verificando funcionamento jarvis               ")
    try:
        command = CONF_INFO['COMMAND']['JARVIS_STATUS']
        result = subprocess.check_output(command, shell=True, universal_newlines=True)
        JSON_INFO['MACHINE']['RUNNING_JARVIS'] = 'running' in result
        if not JSON_INFO['MACHINE']['RUNNING_JARVIS']:
            print_collor_red('      -> Jarvis nao esta funciondo')
            INCOMPATIBILIRIES['DIVERGENC'].add('JARVIS DEAD')
    except:
        print_collor_red('-> Erro ao verificar funcionamento jarviz         ')

def get_log_jarvis():
    global JSON_INFO, LOG_JARVIS
    path_file = JSON_INFO['PATHS']['LOG_JARVIS']   
    with open(path_file, 'r') as arquivo:
        linhas = arquivo.readlines()
        ultimas_20_linhas = linhas[-20:]
        for linha in ultimas_20_linhas:
            if ("ERRO" or "CRITICAL" )in linha:
                LOG_JARVIS = ultimas_20_linhas
                break
    if LOG_JARVIS is  None:  
        JSON_INFO['MACHINE']['LOG_JARVIS_OK'] = True

def print_log_jarvis():
    print("LOG_JARVIS:")
    if LOG_JARVIS is not None:
        for linha in LOG_JARVIS:          
            print(linha.strip())    



# INICIALIZAR MACHINES
def inicialize_machines():
    print_collor_orange('-> Obtendo informações referente a machines...    ')
    # get_ip_info()
    # get_machine_data()
    # get_hostname_machines() 
    # get_if_has_share()
    # exec_validation_swap()
    # get_test_internet_connection()
    # exec_jarvis_status()
    get_log_jarvis()

# CONFIG FOR PRINT
class ColorPrint(Enum):
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    WHITE = '\033[0m'
    BLUE = '\033[34m'
    ORANGE = '\033[33m' 

def print_dict_with_format(data, title):
    if data:
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
    global JSON_INFO,CONF_INFO, INCOMPATIBILIRIES   
    print_dict_with_format(JSON_INFO.get('JARVIS_ENV'), 'JARVIS_ENV')
    print_dict_with_format(JSON_INFO.get('MACHINE'), 'MACHINE')  
    print(INCOMPATIBILIRIES)

def print_collor_yellow(text):
     print(f'{ColorPrint.YELLOW.value}{text}{ColorPrint.WHITE.value}')    

def print_collor_green(text):
     print(f'{ColorPrint.GREEN.value}{text}{ColorPrint.WHITE.value}') 

def print_collor_orange(text):
    print(f'{ColorPrint.ORANGE.value}{text}{ColorPrint.WHITE.value}')    

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
    inicialize_machines()
   
    

    print_collor_yellow("-" * 50)

    print_result() 
    print_collor_yellow("-" * 50)

    print_log_jarvis()

if __name__ == "__main__":
    main()
