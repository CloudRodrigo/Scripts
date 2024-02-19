import os
import re
import subprocess
from enum import Enum

JSON_INFO = None
CONF_INFO = None
INCOMPATIBILIRIES = None
LOG_JARVIS= None

def inicialize_config():
    print_color_orange('-> Inicializando criação de json informações.     ')
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
                'CREATE_RABBITMQ_CONFIG':'/etc/rabbitmq/rabbitmq.config',
                'CONFIG_MOSQUITTO':'/etc/mosquitto/mosquitto.conf',
                'AUTOSTART_CLOUDPARK':'/home/pi/.config/autostart/cloudpark.desktop'
            },
            'HAS_JARVISTMP': False,                    
            'JARVIS_INSTALLED': False,
            'JARVIS_ENV': {
                'IS_SERVER': False, 
                'HAS_HARDWARE': False,
                'HAS_PAYMENT': False,
                'HAS_ALPR': False,
                'HAS_CASHIER': False,
                "HAS_LCD": False,
                'HAS_ALPR': False,
                'USE_SHARE': False,
                'HAS_STAMP': False,
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
                'CURRENT_VERSION_CASHIER': False,
                'VERSION_CASHIER':'',
                'INTERNET': False,
                'DOWNLOAD':'',
                'UPLOAD':'',
                'RUNNING_JARVIS': False,
                'RUNNING_RABBIT': False,
                'RUNNING_MOSQUITTO': False,
                'LOG_JARVIS_OK': False,
            },
            'OTHERS':{
                'VERSION_CASHIER':'23.10.2',
                'LINK_UPPDATE_VERSION_CHASHIER':'https://s3.sa-east-1.amazonaws.com/ferramentas.cloudpark.com.br/caixa/cloudpark-desktop_23.10.2_amd64.deb"'


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
                    'RABBIT_STATUS':'sudo service rabbitmq-server status',
                    'MOSQUITTO_STATUS':'sudo service mosquitto status',
                    'REMOVE_MOSQUITTO':'sudo apt-get -y remove mosquitto',
                    'INSTALLING_RABBIT':'sudo apt-get install rabbitmq-server',
                    'INSTALLING_MOSQUITTO':'sudo apt-get install mosquitto -y',
                }
        }
        CONF_INFO = config_comand  
        
        no_compliant = {
            'UNCONFORMITIES': set()
        }
        INCOMPATIBILIRIES = no_compliant
        print_color_green('-> Finalizando criação de json informações.       ')
    except:
        print_color_red('-> Erro ao criar json de informações              ')

def exec_cache_existente():
    path = JSON_INFO['PATHS']['CONFIG_HARDWARE']
    try:
        print_color_orange('-> Verificando tipo de equipamento                ')
        if not os.path.exists(path):
            is_cache()
            load_config_jarvis_env()
        else:
            print_color_blue('     -> Equipamento tipo PI                     ')
            load_config_jarvis_env()
            has_swap()
    except Exception as e:
        print_color_red('-> Erro ao carregar json de informações: ' + e)

def is_cache():
    global JSON_INFO
    path_file = JSON_INFO['PATHS']['AUTOSTART_CLOUDPARK']
    try:
        print_color_orange('-> Verificando AutoStart')
        with open(path_file, 'r') as arquivo:
            conteudo = arquivo.read()
            if 'CloudPark' in conteudo:
                print_color_blue('     -> Equipamento tipo CAIXA                   ')
                JSON_INFO['JARVIS_ENV']['HAS_CASHIER'] = True
                exec_validation_version_cashier()
            else:
                print_color_blue('     -> Equipamento NÃO é um CAIXA                   ')
        print_color_green('-> Finalizando verificação AutoStart')
    except Exception as e:
        print_color_red('-> Erro ao tentar verificar AutoStart: ' + str(e))


def exec_validation_version_cashier():
    global CONF_INFO, INCOMPATIBILIRIES, JSON_INFO
    command_version_cashier = CONF_INFO['COMMAND']['VERSION_CASHIER']
    version_cashier = JSON_INFO['OTHERS']['VERSION_CASHIER']
    try:
        result = subprocess.check_output(command_version_cashier, shell=True, universal_newlines=True)
        match = re.search(r'Version: (\d+\.\d+\.\d+)', result)
        JSON_INFO['MACHINE']['VERSION_CASHIER'] = match.group(1)
        JSON_INFO['MACHINE']['CURRENT_VERSION_CASHIER'] = 'Version: {}'.format(version_cashier) in result
        if not JSON_INFO['MACHINE']['CURRENT_VERSION_CASHIER']:
            INCOMPATIBILIRIES['UNCONFORMITIES'].add('Caixa atualizado')
            # update_version_cashier()
    except subprocess.CalledProcessError as e:
        print_color_red('Erro ao executar o comando: {}'.format(e))
    except Exception as e:
        print_color_red('Erro inesperado: {}'.format(e))


""" def update_version_cashier():
    global CONF_INFO, INCOMPATIBILIRIES, JSON_INFO
    version_cashier = JSON_INFO['OTHERS']['VERSION_CASHIER']
    link_update_version_cashier = JSON_INFO['OTHERS']['LINK_UPDATE_VERSION_CASHIER']
    try:
        print_color_orange('     -> Iniciando Atualização caixa')
        subprocess.check_output(['wget', link_update_version_cashier]).decode('utf-8')
        subprocess.check_output(['sudo', 'dpkg', '--purge', 'cloudpark-desktop']).decode('utf-8')
        subprocess.check_output(['sudo', 'apt-get', 'update'])
        subprocess.check_output(['sudo', 'dpkg', '-i', 'cloudpark-desktop_'+version_cashier+'_amd64.deb'])
        # subprocess.check_output(['sudo', 'nano', '/home/pi/.config/autostart/cloudpark.desktop'])
        print_color_green('     -> Caixa atualizado com sucesso')
    except Exception as e:
        print_color_red('      -> Erro ao tentear atualizar o caixa ', e) """

def load_config_jarvis_env():
    print_color_orange('-> Iniciando carregamento de json informações...  ')
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
        print_color_green('-> Finalizando carregamento de json informações...')        
    except Exception as e:
        print_color_red('-> Erro ao carregar json de informações:', str(e))

def has_swap():
    global JSON_INFO
    path_file = JSON_INFO['PATHS']['CONFIG_HARDWARE']
    try:
        print_color_blue('     -> Verificando se é STAMP')
        with open(path_file, 'r') as arquivo:
            conteudo = arquivo.read()
            JSON_INFO['JARVIS_ENV']['HAS_STAMP'] = 'STAMP: true' in conteudo
        print_color_green('    -> Finalizando verificação STAMP')
    except Exception as e:
        print_color_red('     -> Erro ao executar verificação STAMP:', e)


def have_ip_info():
    global JSON_INFO, CONF_INFO, INCOMPATIBILIRIES
    try:
        print_color_orange('-> Iniciando obtenção de ip machines              ')
        print_color_blue('    -> Obtendo dados do jarvis ip                ')
        command = CONF_INFO['COMMAND']['JARVIS_IP'] 
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        ip_match = re.search(r'IP:\s*([\d.]+)', output)
        dns_match = re.search(r'DNS:\s*([\d.]+)', output)
        if ip_match:
            JSON_INFO['MACHINE']['LOCAL_IP'] = ip_match.group(1)
        if dns_match: 
            JSON_INFO['MACHINE']['DNS'] = dns_match.group(1)
            have_router_default()
        JSON_INFO['MACHINE']['IP_FIXO'] = 'O IP está fixo' in output
        if not JSON_INFO['MACHINE']['IP_FIXO']:
            INCOMPATIBILIRIES['UNCONFORMITIES'].add('É necessário fixar IP')
        print_color_green('-> Finalizando obtenção de ip machines              ')
    except Exception as e:
        print_color_red('-> Erro ao obter informações referente a machines:', e)

def have_router_default():
    try:
        print_color_blue('    -> Obtendo ip router                          ')
        global JSON_INFO, CONF_INFO
        command = CONF_INFO['COMMAND']['GET_IP_ROUTER'] 
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        lines = output.split('\n')
        for line in lines:
            if 'default via' in line:
                router_ip = line.split(' ')[2]
                JSON_INFO['MACHINE']['ROUTE'] = router_ip     
        print_color_green('    -> Finalização obter ip router                ')
    except Exception as e:
        print_color_red('-> Erro ao obter informações do IP do route:', e)


def have_machine_data():
    print_color_orange('-> Verificando data e hora da máquina             ')
    try:
        global JSON_INFO, CONF_INFO
        command = CONF_INFO['COMMAND']['DATE'] 
        output = subprocess.check_output(command, shell=True).decode('utf-8').strip()
        JSON_INFO['MACHINE']['DATE'] = output
        print_color_green('-> Finalizando data e hora da máquina')
    except Exception as e:
        print_color_red('-> Erro ao obter informações do IP do roteador padrão:', e)

def have_hostname_machines():
    print_color_orange('-> Obtendo hostname da máquina                    ')
    try:
        global JSON_INFO
        path_file = JSON_INFO['PATHS']['CONFIG_HOSTNAME']   
        with open(path_file, 'r') as arquivo:
            conteudo = arquivo.read().strip() 
        JSON_INFO['MACHINE']['HOSTNAME'] = conteudo
        print_color_green('-> Finalizando obtenção do hostname               ')
    except Exception as e:
        print_color_red('-> Erro ao obter hostname:', e)
        
def have_if_has_share():
    global JSON_INFO, CONF_INFO
    print_color_orange('-> Verificar existência da pasta share')
    try:
        command = CONF_INFO['COMMAND']['LS']
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        JSON_INFO['MACHINE']['NO_EXIST_SHARE'] = 'share' not in output
        if not JSON_INFO['MACHINE']['NO_EXIST_SHARE']:
            print_color_red('-> Pasta share foi encontrada')
            if not JSON_INFO['JARVIS_ENV']['USE_SHARE']:
                try:
                    confirm = input('Você tem certeza que deseja excluir a pasta share? (Digite "sim" para confirmar): ')
                    if confirm.lower() == 'sim':
                        delete_share_folder()
                        print_color_orange('-> Finalizando remoção da pasta share')
                        JSON_INFO['MACHINE']['NO_EXIST_SHARE'] = True
                    else:
                        print_color_blue('-> Exclusão da pasta share cancelada.')
                except EOFError:
                    print_color_red('-> Entrada interrompida. Exclusão da pasta share cancelada.')
            else:
                print_color_red('-> Pasta share está sendo usada')
        else:
            print_color_green('-> Pasta share não encontrada')
        print_color_green('-> Finalizando verificação se existe pasta share')
    except subprocess.CalledProcessError as e:
        print_color_red('-> Erro ao verificar existência da pasta share:', e)

def delete_share_folder():
    global CONF_INFO, INCOMPATIBILIRIES
    print_color_blue('     -> Removendo pasta share                    ')
    try:
        command = CONF_INFO['COMMAND']['DELETE_SHARE']
        subprocess.check_output(command, shell=True)
        INCOMPATIBILIRIES['UNCONFORMITIES'].add('PASTA SHARE REMOVIDA')
    except Exception as e:
        print_color_red('-> Erro ao deletar pasta share:', e)
        
def exec_validation_swap():
    global JSON_INFO, CONF_INFO
    print_color_orange('-> Verificar uso do swap                          ')
    try:
        command = CONF_INFO['COMMAND']['CHECK_SWAP']
        output = subprocess.check_output(command, shell=True)
        output = output.decode('utf-8')  
        swap_line = [line for line in output.split('\n') if 'Swap' in line][0]
        JSON_INFO['MACHINE']['NO_USE_SWAP'] = '0B' in swap_line
        if not JSON_INFO['MACHINE']['NO_USE_SWAP']:
            clear_swap()
        JSON_INFO['MACHINE']['NO_USE_SWAP'] = True
        print_color_green('-> Finalizando verificar uso do swap                          ')
    except Exception as e:
        print_color_red('-> Erro ao verificar uso do swap:', e)

   
def clear_swap():
    global CONF_INFO, INCOMPATIBILIRIES
    print_color_blue('     -> Iniciando limpeza do SWAP             ')
    try:
        command = CONF_INFO['COMMAND']['CLEAR_SWAP']
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        INCOMPATIBILIRIES['UNCONFORMITIES'].add('LIMPEZA SWAP')
        print_color_green('     -> Finalizando limpeza do SWAP             ')   
    except Exception as e:
        print_color_red('-> Erro ao executar limpeza de swap:', e)

def have_test_internet_connection():
    global CONF_INFO, INCOMPATIBILIRIES, JSON_INFO
    print_color_orange('-> Verificação de internet...                     ')
    try:
        command = CONF_INFO['COMMAND']['TESTE_PING']
        output = subprocess.check_output(command, shell=True)
        output = output.decode('utf-8')  # Convertendo bytes para string
        JSON_INFO['MACHINE']['INTERNET'] = 'PING google.com' in output
        if not JSON_INFO['MACHINE']['INTERNET']:
            INCOMPATIBILIRIES['UNCONFORMITIES'].add('SEM CONEXAO A INTERNET')
            print_color_red('      -> Sem conexão com a internet               ')
        print_color_green('-> Finalizando verificação internet               ')
    except Exception as e:
        print_color_red('-> Erro ao tentar verificar conexão com a internet:', e) 

def exec_jarvis_status():
    global CONF_INFO, INCOMPATIBILIRIES, JSON_INFO
    print_color_orange('-> Verificando funcionamento jarvis               ')
    try:
        command = CONF_INFO['COMMAND']['JARVIS_STATUS']
        result = subprocess.check_output(command, shell=True)
        result = result.decode('utf-8')  # Convertendo bytes para string
        JSON_INFO['MACHINE']['RUNNING_JARVIS'] = 'running' in result
        
        if not JSON_INFO['MACHINE']['RUNNING_JARVIS']:
            print_color_red('     -> Jarvis não está funcionando')
            INCOMPATIBILIRIES['UNCONFORMITIES'].add('JARVIS DEAD')        
    except Exception as e:
        print_color_red('-> Erro ao verificar funcionamento jarviz:', e)

def have_log_jarvis():
    global JSON_INFO, LOG_JARVIS
    print_color_orange('-> Verificação do log do jarvis...                ')
    try:
        path_file = JSON_INFO['PATHS']['LOG_JARVIS']   
        with open(path_file, 'r') as arquivo:
            linhas = arquivo.readlines()
            ultimas_20_linhas = linhas[-20:]
            for linha in ultimas_20_linhas:
                if 'ERRO' in linha or 'CRITICAL' in linha:
                    LOG_JARVIS = ultimas_20_linhas
                    INCOMPATIBILIRIES['UNCONFORMITIES'].add('LOG JARVIS COM ERRO')
                    print_color_red('-> Erro encontrado no log do jarvis')
                    break
        if LOG_JARVIS is None:  
            JSON_INFO['MACHINE']['LOG_JARVIS_OK'] = True
            print_color_green('-> Log verificado com sucesso                       ')
    except Exception as e:
        print_color_red('-> Erro ao verificar log do jarvis:', e)

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

def have_sqlite3_check():
    global JSON_INFO, CONF_INFO, INCOMPATIBILIRIES
    print_color_orange('-> Verificando instalação SQLITE3                 ')
    is_server = JSON_INFO['JARVIS_ENV']['IS_SERVER']
    command = CONF_INFO['COMMAND']['FIND_SQLITE3']
    try:
        find_sqlite3 = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        find_sqlite3_stdout = find_sqlite3.stdout.decode().strip()
    except subprocess.CalledProcessError:
        find_sqlite3_stdout = None
    try:        
        if is_server:
            if not find_sqlite3_stdout:
                print_color_blue('     -> Instalando SQLITE3                        ')
                INCOMPATIBILIRIES['UNCONFORMITIES'].add('INSTALANDO SQLITE')
                install_sqlite3()
                JSON_INFO['MACHINE']['EXIST_SQLITE3'] = True
        elif not is_server:
            if find_sqlite3_stdout:
                print_color_blue('     -> Removendo SQLITE3                         ')
                INCOMPATIBILIRIES['UNCONFORMITIES'].add('REMOVENDO SQLITE')
                remove_sqlite3()
        print_color_green('-> Finalizando verificação SQLITE3')
        JSON_INFO['MACHINE']['EXIST_SQLITE3'] = True
    except Exception as e:
        print_color_red('-> Erro ao verificar instalação SQLITE3:', e)

def have_check_rabbit():
    global JSON_INFO, CONF_INFO, INCOMPATIBILIRIES
    print_color_orange('-> Iniciando verificação do Rebbit                ')
    is_server = JSON_INFO['JARVIS_ENV']['IS_SERVER']
    status_rabbit()
    try:
        if is_server:
            if JSON_INFO['MACHINE']['RUNNING_RABBIT']:
                restart_rabbit()
                create_rabbitmq_config()
            else:
                installing_rabbit()
                create_rabbitmq_config()
            restart_rabbit()
            status_rabbit()
        elif not is_server and JSON_INFO['MACHINE']['RUNNING_RABBIT']:
            remover_rabbit()
            status_rabbit()
        print_color_green('-> Finalizando verificação do Rebbit              ')
    except Exception as e:
        print_color_red('-> Erro ao executar verificação do Rebbbit:', e)

def status_rabbit():
    global CONF_INFO, JSON_INFO
    command = CONF_INFO['COMMAND']['RABBIT_STATUS']
    try:
        print_color_blue('     -> Verificando status rabbit                 ')
        result = subprocess.check_output(command, shell=True)
        result = result.decode('utf-8')  
        if "running" in result:
            JSON_INFO['MACHINE']['RUNNING_RABBIT'] = True
            print_color_green('     -> Rabbit encontrado                 ')
        else:
            JSON_INFO['MACHINE']['RUNNING_RABBIT'] = False
            print_color_red('     -> Rabbit não encontrado                 ')
    except subprocess.CalledProcessError as e:
        JSON_INFO['MACHINE']['RUNNING_RABBIT'] = False
        print_color_red('     -> Rabbit não encontrado                 ')
        
def remover_rabbit():
    print_color_blue('     -> Removendo Rabbit                   ')
    global CONF_INFO, INCOMPATIBILIRIES
    try:
        remover_rabbit_simple = 'sudo apt-get remove rabbitmq-server -y'
        remover_rabbit_auto_remove = 'sudo apt-get remove --auto-remove rabbitmq-server -y'
        purge_rabbit_auto_remove = 'sudo apt-get purge --auto-remove rabbitmq-server -y'
        update_command = CONF_INFO['COMMAND']['UPDATE']
        subprocess.run(remover_rabbit_simple, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(remover_rabbit_auto_remove, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(purge_rabbit_auto_remove, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(update_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        INCOMPATIBILIRIES['UNCONFORMITIES'].add('Rabbit removido')
        print_color_green('     -> Finalizando remoção do Rabbit                  ')
    except Exception as e:
        print_color_red('     -> Erro ao remover o Rabbit:', e)

def restart_rabbit():
    global CONF_INFO
    restart_command = CONF_INFO['COMMAND']['RESTART_RABBIT']
    try:
        print_color_blue('     -> Reiniciando Rabbit                       ')
        subprocess.run(restart_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_color_green('     -> Rabbit reiniciado                        ')
    except Exception as e:
        print_color_red('     -> Erro ao reiniciar Rabbit:', e)

def installing_rabbit():
    global CONF_INFO, INCOMPATIBILIRIES
    install_rabbit = CONF_INFO['COMMAND']['INSTALLING_RABBIT']
    try:
        print_color_blue('     -> Iniciando instalação rabbit              ')
        process = subprocess.Popen(install_rabbit, shell=True, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.communicate(input='Y\n'.encode())
        process.wait()
        print_color_blue('     -> Instalação do rabbit concluída           ')
        INCOMPATIBILIRIES['UNCONFORMITIES'].add('Rabbit instalado')
    except Exception as e:
        print_color_red('     -> Erro ao instalar rabbit:', e)

def create_rabbitmq_config():
    global JSON_INFO
    conteudo = "[{rabbit, [{loopback_users, []}]}]."
    config_path = JSON_INFO['PATHS']['CREATE_RABBITMQ_CONFIG']
    try:
        print_color_blue('     -> Alterando arquivo Rabbit                  ')
        with open(config_path, 'w') as arquivo:  
            arquivo.write(conteudo) 
        print_color_green('     -> Arquivo alterado do Rabbit               ')
    except Exception as e:
        print_color_red('     -> Erro ao alterar arquivo Rabbit:', e)

def print_log_jarvis():
    print('LOG_JARVIS:')
    if LOG_JARVIS is not None:
        for linha in LOG_JARVIS:
            print(linha.strip())

def fixing_ip():
    global JSON_INFO
    local_ip = JSON_INFO['MACHINE']['LOCAL_IP']
    route = JSON_INFO['MACHINE']['ROUTE']
    dns = JSON_INFO['MACHINE']['DNS']
    command = 'sudo jarvis ip --static {} --mask 24 --gateway {} --dns {}'.format(local_ip, route, dns)
    if not JSON_INFO['MACHINE']['IP_FIXO']:
        head('                    FIXANDO IP                    ')  
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        
def have_mosquitto_check():
    global JSON_INFO, CONF_INFO, INCOMPATIBILIRIES
    print_color_orange('-> Iniciando verificação do Mosquitto             ')
    is_server = JSON_INFO['JARVIS_ENV']['IS_SERVER']
    try:
        status_mosquitto()
        if is_server:
            if JSON_INFO['MACHINE']['RUNNING_MOSQUITTO']:
                config_mosquitto()
            else:
                installing_mosquitto()
                config_mosquitto()
            status_mosquitto()
        elif not is_server and JSON_INFO['MACHINE']['RUNNING_MOSQUITTO']:
            remover_mosquitto()
            status_mosquitto()
        print_color_green('-> Finalizando verificação do Mosquitto     ')
    except Exception as e:
        print_color_red('-> Erro ao executar verificação do Mosquitto:', e)

def status_mosquitto():
    global CONF_INFO, JSON_INFO
    command = CONF_INFO['COMMAND']['MOSQUITTO_STATUS']
    try:
        print_color_blue('     -> Verificando status mosquitto')
        result = subprocess.check_output(command, shell=True)
        result = result.decode('utf-8')  # Convertendo bytes para string
        if 'running' in result:
            print_color_green('     -> Mosquitto encontrado                       ')
            JSON_INFO['MACHINE']['RUNNING_MOSQUITTO'] = True
        else:
            JSON_INFO['MACHINE']['RUNNING_MOSQUITTO'] = False
            print_color_red('     -> Mosquitto não encontrado')
    except subprocess.CalledProcessError:
        JSON_INFO['MACHINE']['RUNNING_MOSQUITTO'] = False
        print_color_red('     -> Mosquitto não encontrado                  ')
        
def config_mosquitto():
    global JSON_INFO, INCOMPATIBILIRIES
    conteudo ="""listener 9001\nprotocol websockets\nlistener 1883\nprotocol mqtt\nallow_anonymous true"""
    path_file = JSON_INFO['PATHS']['CONFIG_MOSQUITTO']
    try:
        print_color_blue('     -> Alterando arquivo Mosquitto               ')
        with open(path_file, 'w') as arquivo:  
            arquivo.write(conteudo)
        print_color_green('     -> Arquivo Mosquitto alterado com sucesso    ')
    except Exception as e:
        print_color_red('     -> Erro ao alterar arquivo Mosquitto:', e)

def remover_mosquitto():
    try:
        print_color_blue('     -> Iniciando remoção do mosquitto                      ')
        command = CONF_INFO['COMMAND']['REMOVE_MOSQUITTO']
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        INCOMPATIBILIRIES['UNCONFORMITIES'].add('Mosquitto removido')
        print_color_green('     -> Mosquitto removido com sucesso                      ')
    except Exception as e:
        print_color_red('     -> Erro ao remover mosquito:', e)
             
def installing_mosquitto():
    global CONF_INFO, INCOMPATIBILIRIES
    install_rabbit = CONF_INFO['COMMAND']['INSTALLING_MOSQUITTO']
    try:
        print_color_blue('     -> Iniciando instalação mosquitto            ')
        process = subprocess.Popen(install_rabbit, shell=True, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.communicate(input='Y\n'.encode())
        process.wait()
        print_color_blue('     -> Finalizada a instalação mosquitto           ')
        INCOMPATIBILIRIES['UNCONFORMITIES'].add('Mosquitto instalado')
    except Exception as e:
        print_color_red('     -> Erro ao instalar mosquitto:', e)
   
def check_speedtest_cli_installed():
    print_color_orange('-> Verificando se speedtest-cli está instalado...')
    try:
        subprocess.call(["speedtest-cli", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_color_green('     -> speedtest-cli já está instalado.')
    except FileNotFoundError:
        print_color_orange('    -> speedtest-cli não está instalado.')
        install_speedtest_cli()

def install_speedtest_cli():
    try:
        print_color_orange('-> Instalando speedtest-cli...')
        subprocess.call(["sudo", "apt", "install", "speedtest-cli"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_color_green('    -> speedtest-cli instalado com sucesso!')
    except subprocess.CalledProcessError as e:
        print_color_red('Erro ao instalar speedtest-cli', e)

def test_internet_speed():
    import speedtest
    global JSON_INFO
    print_color_orange("-> Testando velocidade da internet...")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1e+6  
        upload_speed = st.upload() / 1e+6 
        JSON_INFO['MACHINE']['DOWNLOAD'] = '{:.2f}'.format(download_speed) + 'Mbps'
        JSON_INFO['MACHINE']['UPLOAD'] = '{:.2f}'.format(upload_speed) + 'Mbps'
    except speedtest.NoMatchedServers:
        print_color_red("Erro: Não foi possível encontrar servidores para testar a velocidade da internet. Conexão pode ter caído.")
    except speedtest.ConfigRetrievalError:
        print_color_red("Erro ao recuperar configuração do servidor. Verifique sua conexão com a internet.")
    except Exception as e:
        print_color_red("Erro ao testar velocidade da internet:", e)

        
import subprocess

def print_jarvis_machines():
    global CONF_INFO
    command = CONF_INFO['COMMAND']['JARVIS_MACHINES']
    try:
        print_color_blue("\n------------------JARVIS MACHINES-----------------\n")
        result = subprocess.check_output(command, shell=True)
        print(result.decode('utf-8'))
        print_color_green('-> Jarvis Machines finalizado')
    except subprocess.CalledProcessError as e:
        print_color_red('Erro ao executar jarvis machines:', e)
    except Exception as e:
        print_color_red('Erro ao executar jarvis machines:', e)

             
# INICIALIZAR MACHINES
def process_machines():
    print_color_orange('-> Obtendo informações referente a machines...    ')
    have_ip_info()
    have_machine_data()
    have_hostname_machines() 
    have_if_has_share()
    exec_validation_swap()
    have_test_internet_connection()
    exec_jarvis_status()
    have_log_jarvis()
    have_sqlite3_check()
    have_check_rabbit()
    have_mosquitto_check()
    check_speedtest_cli_installed()
    test_internet_speed()

# CONFIG FOR PRINT
class ColorPrint(Enum):
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    WHITE = '\033[0m'
    BLUE = '\033[34m'
    ORANGE = '\033[33m'

    def __str__(self):
        return self.value


def print_dict_with_format(data, title):
    if data:
        print_color_orange('\n' + title.upper())
        print_color_orange('-' * 50)
        for key, value in data.items():
            if value:
                print_color_green('{}:{}'.format(key, value))
            else:
                print_color_red('{}:{}'.format(key, value))
    else:
        print_color_orange('No data found for {}.'.format(title.upper()))


def print_unconformities_json(title, inconformities):
    global INCOMPATIBILIRIES
    if inconformities:
        print_color_red('\n' + '-'*50)
        print_color_yellow(title.upper())
        print_color_red('-' * 50)
        for  value in inconformities:
            print_color_red( value)
            print_color_red('-' * 50)
    else:
        print_color_yellow('\n' + '-'*50)
        print_color_green('Nem um processo foi alterado')
        print_color_yellow('-'*50 + '\n')


def print_result():    
    global JSON_INFO,CONF_INFO, INCOMPATIBILIRIES   
    print_dict_with_format(JSON_INFO.get('JARVIS_ENV'), 'JARVIS_ENV')
    print_dict_with_format(JSON_INFO.get('MACHINE'), 'MACHINE')  
    print_unconformities_json("Resultados do Processo", INCOMPATIBILIRIES['UNCONFORMITIES'])


def print_color_yellow(text):
    print('{}{}{}'.format(ColorPrint.YELLOW.value, text, ColorPrint.WHITE.value))

def print_color_green(text):
    print('{}{}{}'.format(ColorPrint.GREEN.value, text, ColorPrint.WHITE.value))

def print_color_orange(text):
    print('{}{}{}'.format(ColorPrint.ORANGE.value, text, ColorPrint.WHITE.value))

def print_color_red(text):
    print('{}{}{}'.format(ColorPrint.RED.value, text, ColorPrint.WHITE.value))

def print_color_blue(text):
    print('{}{}{}'.format(ColorPrint.BLUE.value, text, ColorPrint.WHITE.value))

    
def head(text):
    print_color_yellow("-" * 50)
    print_color_yellow('{}'.format(text))
    print_color_yellow("-" * 50)

# MAIN 
def main():
    global JSON_INFO
    head('     VALIDADOR DE INTEGRIDADE DE EQUIPAMENTO      ')
    inicialize_config()
    exec_cache_existente()
    process_machines()
    head('                    RESULTADOS                    ')
    print_result()
    if not JSON_INFO['MACHINE']['LOG_JARVIS_OK']:
        head('                    LOG JARVIS                    ')
        print_log_jarvis()
        
    print_jarvis_machines()
    
    if not JSON_INFO['MACHINE']['IP_FIXO']:
        fixing_ip()
    
if __name__ == "__main__":
    
    main()
    
