import subprocess
import re

CURRENT_CORRECT_VESION_CASHIER = '23.10.2'


def exec_cache_existence():
    result = subprocess.check_output(['cat', '/etc/cloudpark/jarvis.env']).decode('utf-8')
    if "cat: /etc/cloudpark/config.yml" in result:
        print("\n---------------------CAIXA---------------------\n")
        print("\n-----------------------------------------------\n")
        exec_validation_version_cashier()
    else:
        print_info_jarvis_env()


def print_info_jarvis_env():
    try:
        result = subprocess.check_output(['cat', '/etc/cloudpark/jarvis.env']).decode('utf-8')
        print("\n-----------------------------------------------\n")
        print("\n----------------------PI-----------------------\n")
        get_value_config_jarvis_env(result, 'IS_SERVER')
        get_value_config_jarvis_env(result, 'HAS_HARDWARE')
        get_value_config_jarvis_env(result, 'HARDWARE_VERSION')
        get_value_config_jarvis_env(result, 'CLOUDPARK_VERSION')
        get_value_config_jarvis_env(result, 'HAS_PAYMENT')
        get_value_config_jarvis_env(result, 'HAS_ALPR')
        get_value_config_jarvis_env(result, 'LCD_VERSION')

    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando: {}".format(e))
    except Exception as e:
        print("Erro inesperado: {}".format(e))

def get_value_config_jarvis_env(result, variavel):
    match = re.search(r'{}=(TRUE|FALSE)'.format(variavel), result, re.IGNORECASE)
    if match:
        print("{}= {}".format(variavel, match.group(1)))
    else:
        print('{} = N/A'.format(variavel))



def exec_validation_version_cashier():
    try:
        result = subprocess.check_output(['sudo', 'dpkg', '-s', 'cloudpark-desktop']).decode('utf-8')
        match = re.search(r'"Version":\s*"(\d+\.\d+\.\d+)"', result)
        if match and match.group(1) != CURRENT_CORRECT_VESION_CASHIER:
            print(match.group(1))
            """update_version_cashier()"""
        else:
            print("VERSION CAIXA=" + str(match))
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando: {}".format(e))
    except Exception as e:
        print("Erro inesperado: {}".format(e))


def update_version_cashier():
    try:
        link_update = "https://s3.sa-east-1.amazonaws.com/ferramentas.cloudpark.com.br/caixa/cloudpark-desktop_23.10.2_amd64.deb"
        subprocess.check_output(['wget', link_update]).decode('utf-8')
        subprocess.check_output(['sudo', 'dpkg', '--purge', 'cloudpark-desktop']).decode('utf-8')
        subprocess.check_output(['sudo', 'apt-get', 'update'])
        subprocess.check_output(['sudo', 'dpkg', '-i', 'cloudpark-desktop_23.10.2_amd64.deb'])
        subprocess.check_output(['sudo', 'nano', '~/.config/autostart/cloudpark.desktop'])
        print("\n---------------CAIXA ATUALIZADO----------------\n")

    except Exception as e:
        print("Erro inesperado: {}".format(e))


def print_info_ip():
    result = subprocess.check_output(['sudo', 'jarvis', 'ip']).decode('utf-8')
    if "O IP está fixo" in result:
        print("O IP está fixo")
    else:
        print("O IP está DHCP")


def print_jarvis_machines():
    print("\n--------------OPERATION MACHINES---------------\n")
    result = subprocess.check_output(['sudo', 'jarvis', 'machines']).decode('utf-8')

    print(result)


def print_date():
    result = subprocess.check_output(['sudo', 'date']).decode('utf-8')
    print("DATA= " + result)


def print_has_share():
    result = subprocess.check_output(['ls']).decode('utf-8')
    print("SHARE= EXISTE!! " if "share" in result else "SHARE= N/A")


def exec_validation_swap():
    result = subprocess.check_output(['free', '-h']).decode('utf-8')
    swap_line = [line for line in result.split('\n') if 'Swap' in line][0]
    used_swap = subprocess.check_output(['awk', '{print $3}', '/dev/stdin'],
                                        input=swap_line.encode('utf-8')).decode('utf-8').strip()
    if used_swap == '0B':
        print("SWAP= VAZIO")
    else:
        print("SWAP= EM USO")
        clean_swap()


def clean_swap():
    try:
        print("\n-----------------LIMPANDO SWAP-----------------\n")

        result = subprocess.check_output(['sudo', 'swapoff', '-a', ';', 'sudo', 'swapon', '-av']).decode('utf-8')
        print(result)
        print("-------------------TERMINOU--------------------\n")
        print("\n----------------------PI-----------------------\n")
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando: {}".format(e))
    except Exception as e:
        print("Erro inesperado: {}".format(e))


def print_log_jarvis():
    try:
        print("\n-----------------LOG JARVIS OK?-----------------\n")
        result = subprocess.check_output(['sudo', 'tail', '-50', '/var/log/cloudpark/jarvis.log']).decode('utf-8')
        print(result)
        print("-------------------TERMINOU--------------------")

    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando: {}".format(e))
    except Exception as e:
        print("Erro inesperado: {}".format(e))


def exec_jarvis_install():
    result = subprocess.check_output(['sudo', 'service', 'cloudpark-jarvis', 'status']).decode('utf-8')
    if "running" in result:
        print("JARVIS INSTALADO")
        print_log_jarvis()
    else:
        print("JARVIS N/A")


def priint_test_internet_connection():
    result = subprocess.check_output(['ping', '-c', '2', '-w', '2', 'google.com']).decode('utf-8')
    if "PING google.com" in result:
        print("INTERNETC= CONECTADO")
    else:
        print("INTERNETC= N/A")


def main():
    exec_cache_existence()
    print_info_ip()
    print_date()
    print_has_share()
    exec_validation_swap()
    priint_test_internet_connection()
    """ print_exists_sqlite3()"""
    exec_jarvis_install()
    print_jarvis_machines()


if __name__ == "__main__":
    main()
