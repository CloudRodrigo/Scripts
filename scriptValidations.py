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
    global JSON_INFO
    global CONF_INFO
    global INCOMPATIBILIRIES
    
    try:   
        config_path = {
            'PATHS': {
                'SYS_JARVIS_ENV': '/opt/jarvisenv/',
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
                'CONFIG_HOSTNAME':'/etc/hostname',
                'CONFIG_RABBIT':'/etc/rabbitmq/rabbitmq.config',
                'CONFIG_MOSQUITTO':'/etc/mosquitto/mosquitto.conf',
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
                'STAMP': False,
            },
            'MACHINE': {
                'HOSTNAME': '',
                'LOCAL_IP': '',
                'DNS': '',
                'ROUTE': '',
                'DATE': '',
                'IP_FIXO': False,
                'EXIST_SQLITE3': False,
                'NO_USE_SWAP': False,
                'NO_EXIST_SHARE': False,
                'INTERNET': False,
                'DOWNLOAD':'',
                'UPLOAD':'',
                'RUNNING_JARVIS': False,
                'RUNNING_RABBIT': False,
                'RUNNING_MOSQUITTO': False,
                'LOG_JARVIS_OK': False,
            }
        }
        JSON_INFO = config_path  
        
        config_comand = {
                'COMMAND':{
                    'TESTE_PING':'ping -c 2 -w 2 google.com',
                    'JARVIS_STATUS':'sudo service cloudpark-jarvis status',
                    'DATE':'sudo date',
                    'LOG_JARVIS':'sudo tail -50 /var/log/cloudpark/jarvis.log',
                    'CLEAR_SWAP':'sudo swapoff -a ; sudo swapon -av',
                    'CHECK_SWAP':'free -h | grep Swap',
                    'LS':'ls',
                    'GET_IP_ROUTER':'ip route | grep default',
                    'JARVIS_MACHINES':'sudo jarvis machines',
                    'JARVIS_IP':'sudo jarvis ip',
                    'VERSION_CASHIER':'sudo dpkg -s cloudpark-desktop',
                    'DELETE_SHARE':'sudo rm -r ./share',
                    'FIND_SQLITE3':'which sqlite3',
                    'REMOVE_SQLITE3':'sudo apt remove sqlite3',
                    'INSTALL_SQLITE3':'sudo apt install sqlite3',
                    'UPDATE':'sudo apt update',
                    'AUTOREMOVER':'sudo apt autoremover',
                    'RESTART_RABBIT':'sudo service rabbitmq-server restart',
                    'RABBIT_STATUS':'sudo service rabbitmq-server  status',
                    'MOSQUITTO_STATUS':'sudo service mosquitto  status',
                    'REMOVE_MOSQUITTO':'sudo apt-get remove mosquitto -y',
                }
        }
        CONF_INFO = config_comand  
        
        no_compliant = {
            'UNCONFORMITIES': set()
        }
        INCOMPATIBILIRIES = no_compliant
        print_collor_green('-> Finalizando criação de json informações.       ')
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
    global JSON_INFO, CONF_INFO
    try:        
        print_collor_orange('-> Iniciando obtenção de ip machines              ')        
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
            INCOMPATIBILIRIES['UNCONFORMITIES'].add('É necessário fixar IP')
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
    print_collor_orange('-> Verificando data e hora da máquina             ')
    try:
        global JSON_INFO, CONF_INFO
        command = CONF_INFO['COMMAND']['DATE'] 
        output = subprocess.check_output(command, shell=True, universal_newlines=True).strip()
        JSON_INFO['MACHINE']['DATE'] = output
        print_collor_green('-> Finalizando data e hora da máquina')
    except:
        print_collor_red('-> Erro ao obter informações do IP do roteador padrão:')

def get_hostname_machines():
    print_collor_orange('-> Obtendo hostname da máquina                    ')
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
        JSON_INFO['MACHINE']['NO_EXIST_SHARE'] = 'share' in  output  # Verifica se 'share' está presente no output
        if JSON_INFO['MACHINE']['NO_EXIST_SHARE']:
            print_collor_red('-> Pasta share foi encontrada')
            if not JSON_INFO['JARVIS_ENV']['USE_SHARE']:
                confirm = input('Você tem certeza que deseja excluir a pasta share? (Digite "sim" para confirmar): ')
                if confirm.lower() == 'sim':
                    delete_share_folder()
                    print_collor_orange("    -> Finalizando remoção da pasta share         ")
                    JSON_INFO['MACHINE']['NO_EXIST_SHARE'] = True
                else:
                    print_collor_blue('-> Exclusão da pasta share cancelada.')
            else:
                print_collor_red('      -> Pasta share está sendo usada             ')
        JSON_INFO['MACHINE']['NO_EXIST_SHARE'] = True
        print_collor_green('-> Finalizando verificação se existe pasta share  ')
    except:
        print_collor_red('-> Erro ao verificar existencia da pasta share   ')

def delete_share_folder():
    global CONF_INFO, INCOMPATIBILIRIES
    print_collor_blue('     -> Removendo pasta share                    ')
    try:
        command = CONF_INFO['COMMAND']['DELETE_SHARE']
        subprocess.check_output(command, shell=True, universal_newlines=True)
        INCOMPATIBILIRIES['UNCONFORMITIES'].add('PASTA SHARE REMOVIDA')
    except:
        print_collor_red("-> Erro ao deletar pasta share")
        
def exec_validation_swap():
    global JSON_INFO, CONF_INFO
    print_collor_orange('-> Verificar uso do swap                          ')
    try:
        command = CONF_INFO['COMMAND']['CHECK_SWAP']
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        swap_line = [line for line in output.split('\n') if 'Swap' in line][0]
        JSON_INFO['MACHINE']['NO_USE_SWAP'] = '0B' in swap_line
        if not JSON_INFO['MACHINE']['NO_USE_SWAP']:
            clear_swap()
        JSON_INFO['MACHINE']['NO_USE_SWAP'] = True
        print_collor_green('-> Finalizando verificar uso do swap                          ')
    except:
        print_collor_red('-> Erro ao verificar uso do swap                  ')
   
def clear_swap():
    global CONF_INFO, INCOMPATIBILIRIES
    print_collor_blue('     -> Iniciando limpeza do SWAP             ')
    try:
        command = CONF_INFO['COMMAND']['CLEAR_SWAP']
        subprocess.run(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        INCOMPATIBILIRIES['UNCONFORMITIES'].add('LIMPEZA SWAP')
        print_collor_green('     -> Finalizando limpeza do SWAP             ')   
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
            INCOMPATIBILIRIES['UNCONFORMITIES'].add('SEM CONEXAO A INTERNET')
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
            INCOMPATIBILIRIES['UNCONFORMITIES'].add('JARVIS DEAD')        
    except:
        print_collor_red('-> Erro ao verificar funcionamento jarviz         ')

def get_log_jarvis():
    global JSON_INFO, LOG_JARVIS
    print_collor_orange("-> Verificação do log do jarvis...                ")
    try:
        path_file = JSON_INFO['PATHS']['LOG_JARVIS']   
        with open(path_file, 'r') as arquivo:
            linhas = arquivo.readlines()
            ultimas_20_linhas = linhas[-20:]
            for linha in ultimas_20_linhas:
                if ("ERRO" or "CRITICAL" )in linha:
                    LOG_JARVIS = ultimas_20_linhas
                    INCOMPATIBILIRIES['UNCONFORMITIES'].add('LOG JARVIS COM ERRO')
                    print_collor_red("-> Erro encontrado no log do jarvis")
                    break
        if LOG_JARVIS is  None:  
            JSON_INFO['MACHINE']['LOG_JARVIS_OK'] = True
            print_collor_green("-> Log verificado com sucesso                       ")
    except:
        print_collor_red("-> Erro ao verificar log do jarvis                ")

def install_sqlite3():
    global CONF_INFO
    install_command = CONF_INFO['COMMAND']['INSTALL_SQLITE3']
    subprocess.run(install_command, shell=True, universal_newlines=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def remove_sqlite3():
    global CONF_INFO
    remove_command = CONF_INFO['COMMAND']['REMOVE_SQLITE3']
    autoremove_command = CONF_INFO['COMMAND']['AUTOREMOVER']
    subprocess.run("echo 'Y' | " + remove_command, shell=True, universal_newlines=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(autoremove_command, shell=True, universal_newlines=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_sqlite3_check():
    global JSON_INFO, CONF_INFO, INCOMPATIBILIRIES
    print_collor_orange("-> Verificando instalação SQLITE3                 ")
    is_server = JSON_INFO['JARVIS_ENV']['IS_SERVER']
    command = CONF_INFO['COMMAND']['FIND_SQLITE3']
    try:
        find_sqlite3 = subprocess.run(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        find_sqlite3_stdout = find_sqlite3.stdout.strip()
    except subprocess.CalledProcessError:
        find_sqlite3_stdout = None
    try:        
        if is_server:
            if not find_sqlite3_stdout:
                print_collor_blue('     -> Instalando SQLITE3                        ')
                INCOMPATIBILIRIES['UNCONFORMITIES'].add('INSTALANDO SQLITE')
                install_sqlite3()
                JSON_INFO['MACHINE']['EXIST_SQLITE3'] = True
        elif not is_server:
            if find_sqlite3_stdout:
                print_collor_blue('     -> Removendo SQLITE3                         ')
                INCOMPATIBILIRIES['UNCONFORMITIES'].add('REMOVENDO SQLITE')
                remove_sqlite3()
        print_collor_green('-> Finalizando verificação SQLITE3')
        JSON_INFO['MACHINE']['EXIST_SQLITE3'] = True
    except:
        print_collor_red('-> Erro ao verificar instalação SQLITE3')

def get_check_rabbit():
    global JSON_INFO, CONF_INFO, INCOMPATIBILIRIES
    print_collor_orange('-> Iniciando verificação do Rebbit                ')
    is_serve = JSON_INFO['JARVIS_ENV']['IS_SERVER']
    
    try:
        status_rabbit()
        if is_serve and JSON_INFO['MACHINE']['RUNNING_RABBIT']:
            installing_rabbit() 
            restart_rabbit()
            status_rabbit()
            if JSON_INFO['MACHINE']['RUNNING_RABBIT']:
                print('     -> Instalando com sucesso                    ')
            else:
                print('     -> Erro ao instalar rabbbit                ')
        if is_serve and not JSON_INFO['MACHINE']['RUNNING_RABBIT']:
            installing_rabbit() 
            restart_rabbit()
            status_rabbit()
            if JSON_INFO['MACHINE']['RUNNING_RABBIT']:
                print('     -> Instalando com sucesso                    ')
                INCOMPATIBILIRIES['UNCONFORMITIES'].add('Rabbit instalado')
            else:
                print('     -> Erro ao instalar mosquitto                ')
        elif is_serve and JSON_INFO['MACHINE']['RUNNING_RABBIT']:
            remover_rabbit()
        print_collor_green('-> Finalizando verificação do Rebbit              ')
    except:
        print_collor_red('-> Erro ao executar verificação do Rebbbit ')

def status_rabbit():
    global CONF_INFO
    command = CONF_INFO['COMMAND']['RABBIT_STATUS']
    try:
        print_collor_blue('     -> Verificando status rabbit                 ')
        result = subprocess.check_output(command, shell=True, universal_newlines=True)
        JSON_INFO['MACHINE']['RUNNING_RABBIT'] = 'running' in result 
    except subprocess.CalledProcessError:
        print_collor_orange('     -> Rabbit nao encontrado                 ')
        pass
        
def remover_rabbit():
    print_collor_blue('     -> Removendo Rabbit                   ')
    global CONF_INFO, INCOMPATIBILIRIES
    try:
        remover_rabbit_simple = 'sudo apt-get remove rabbitmq-server -y'
        remover_rabbit_auto_remove = 'sudo apt-get remove --auto-remove rabbitmq-server -y'
        purge_rabbit_auto_remove = 'sudo apt-get purge --auto-remove rabbitmq-server -y'
        update_command = CONF_INFO['COMMAND']['UPDATE']
        subprocess.run(remover_rabbit_simple, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(remover_rabbit_auto_remove, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(purge_rabbit_auto_remove, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(update_command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        INCOMPATIBILIRIES['UNCONFORMITIES'].add('Rabbit removido')
        print_collor_green('     -> Finalizando remoção do Rabbit                  ')
    except:
        print_collor_red('     -> Erro ao remover o Rabbit')

def restart_rabbit():
    global CONF_INFO
    restart_command = CONF_INFO['COMMAND']['RESTART_RABBIT']
    try:
        print_collor_blue('     -> Reiniciando Rabbit                       ')
        subprocess.run(restart_command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_collor_green('     -> Rabbit reiniciado                        ')
    except:
        print_collor_red('      -> Erro ao reiniciar Rabbit                 ')

def installing_rabbit():
    global JSON_INFO
    conteudo ="[{rabbit, [{loopback_users, []}]}]."
    path_file = JSON_INFO['PATHS']['CONFIG_RABBIT']
    print(path_file)
    try:
        print_collor_blue('     -> Alterando arquivo Rabbit                  ')
        with open(path_file, 'w') as arquivo:  
            arquivo.write(conteudo)
        print_collor_green('     -> Arquivo alterado Rabbit                   ')
    except:
        print_collor_red('     -> Erro ao alterar arquivo Rabbit: ')

def get_mosquitto_check():
    global JSON_INFO, CONF_INFO, INCOMPATIBILIRIES
    print_collor_orange('-> Iniciando verificação do Mosquitto                ')
    is_serve = JSON_INFO['JARVIS_ENV']['IS_SERVER']
    try:
        status_mosquitto()
        if is_serve and JSON_INFO['MACHINE']['RUNNING_MOSQUITTO']:
            installing_mosquitto()
            status_mosquitto()
            if JSON_INFO['MACHINE']['RUNNING_MOSQUITTO']:
                print_collor_green('     -> Instalando com sucesso                    ')
            else:
                print_collor_red('     -> Erro ao instalar mosquitto                ')
        if is_serve and not JSON_INFO['MACHINE']['RUNNING_MOSQUITTO']:
            installing_mosquitto()
            status_mosquitto()
            if JSON_INFO['MACHINE']['RUNNING_MOSQUITTO']:
                print_collor_green('     -> Instalando com sucesso                    ')
                INCOMPATIBILIRIES['UNCONFORMITIES'].add('Mosquito instalado')
            else:
                print_collor_red('     -> Erro ao instalar mosquitto                ')
        elif not is_serve and JSON_INFO['MACHINE']['RUNNING_MOSQUITTO']:
            remover_mosquitto()
        print_collor_green('-> Finalizando verificação do Mosquitto           ')
    except:
        print_collor_red('-> Erro ao executar verificação do Mosquitto      ')

def status_mosquitto():
    global CONF_INFO
    command = CONF_INFO['COMMAND']['MOSQUITTO_STATUS']
    try:
        print_collor_blue('     -> Verificando status mosquitto')
        result = subprocess.check_output(command, shell=True, universal_newlines=True)
        JSON_INFO['MACHINE']['RUNNING_MOSQUITTO'] = 'running' in result 
        print_collor_blue('     -> Mosquitto nao encontrado')
    except subprocess.CalledProcessError:
        print_collor_orange('     -> Mosquitto nao encontrado                  ')
        pass
        
def installing_mosquitto():
    global JSON_INFO, INCOMPATIBILIRIES
    conteudo ="""listener 9001\nprotocol websockets\nlistener 1883\nprotocol mqtt\nallow_anonymous true"""
    path_file = JSON_INFO['PATHS']['CONFIG_MOSQUITTO']
    try:
        print_collor_blue('     -> Alterando arquivo Mosquitto               ')
        with open(path_file, 'w') as arquivo:  
            arquivo.write(conteudo)
        print_collor_green('     -> Arquivo alterado Mosquitto                ')
    except:
        print_collor_red('     -> Erro ao alterar arquivo Mosquitto         ')

def remover_mosquitto():
   try:
    print_collor_blue('      -> Inicinado remoção do mosquitto                      ')
    command = JSON_INFO['COMMAND']['REMOVE_MOSQUITTO']
    subprocess.run(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    INCOMPATIBILIRIES['UNCONFORMITIES'].add('Mosquitto removido')
    print_collor_green('      -> Removendo mosquitto                      ')
   except:
       print_collor_red('     -> Erro ao remover mosquito                  ')  
    
def print_log_jarvis():
    print("LOG_JARVIS:")
    if LOG_JARVIS is not None:
        for linha in LOG_JARVIS:          
            print(linha.strip())    

def fixing_ip():
    global JSON_INFO
    local_ip = JSON_INFO['MACHINE']['LOCAL_IP']
    route = JSON_INFO['MACHINE']['ROUTE']
    dns = JSON_INFO['MACHINE']['DNS']
    command = f'sudo jarvis ip --static {local_ip} --mask 24 --gateway {route} --dns {dns}'
    if not JSON_INFO['MACHINE']['IP_FIXO']:
        head('                    FIXANDO IP                    ')  
        subprocess.run(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
     
# INICIALIZAR MACHINES
def process_machines():
    print_collor_orange('-> Obtendo informações referente a machines...    ')
    get_ip_info()
    get_machine_data()
    get_hostname_machines() 
    get_if_has_share()
    exec_validation_swap()
    get_test_internet_connection()
    exec_jarvis_status()
    get_log_jarvis()
    get_sqlite3_check()
    get_check_rabbit()
    get_mosquitto_check()

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
        print_collor_orange('\n' + title.upper())
        print_collor_orange('-' * 50)
        for key, value in data.items():
            if value:
                print_collor_green(f'{key}:{value}')
            else:
                 print_collor_red(f'{key}:{value}')
    else:
        print_collor_orange(f"No data found for {title.upper()}.")

def print_result():    
    global JSON_INFO,CONF_INFO, INCOMPATIBILIRIES   
    print_dict_with_format(JSON_INFO.get('JARVIS_ENV'), 'JARVIS_ENV')
    print_dict_with_format(JSON_INFO.get('MACHINE'), 'MACHINE')  
    print_collor_blue('-'*50)
    print_collor_blue(INCOMPATIBILIRIES)
    print_collor_blue('-'*50)

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
    
def head(text):
    print_collor_yellow("-" * 50)
    print_collor_yellow(f'{text}')
    print_collor_yellow("-" * 50)

# MAIN 

def main():
    global JSON_INFO
    head('     VALIDADOR DE INTEGRIDADE DE EQUIPAMENTO      ')
    inicialize_config()
    exec_cache_existente()
    process_machines()
    head('                    RESULTADOS                    ')
    print_result()
    if  not JSON_INFO['MACHINE']['LOG_JARVIS_OK']:
        head('                    LOG JARVIS                    ')
        print_log_jarvis()
    fixing_ip()
    
if __name__ == "__main__":
    main()
