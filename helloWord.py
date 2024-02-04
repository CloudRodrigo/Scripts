import subprocess
import re

# Variáveis globais
is_server = None


variables_to_check_jarvis_env = [
    {'IS_SERVER': 'is_server'},
    {'HAS_HARDWARE': 'has_hardware'},
    {'HARDWARE_VERSION': 'hardware_version'},
    {'CLOUDPARK_VERSION': 'cloudpark_version'},
    {'HAS_PAYMENT': 'has_payment'},
    {'HAS_ALPR': 'has_alpr'},
    {'LCD_VERSION': 'lcd_version'},
    {'JARVIS_DIR',''},
    {'ACCESS_DIR',''}
]

CURRENT_CORRECT_VERSION_CASHIER = '23.10.2'
COMANDO_JARVIS_ENV = 'cat /etc/cloudpark/jarvis.env'

# Lista para armazenar os resultados
results_list = []


def exec_cache_existence():
    try:
        result = subprocess.check_output(COMANDO_JARVIS_ENV, shell=True).decode('utf-8')
        if "cat: /etc/cloudpark/config.yml" in result:
            results_list.append("\n---------------------CAIXA---------------------\n")
            results_list.append("\n-----------------------------------------------\n")
        else:
            print_info_jarvis_env(result)

    except subprocess.CalledProcessError as e:
        results_list.append(f"Erro ao executar o comando: {e}")
    except Exception as e:
        results_list.append(f"Erro inesperado: {e}")


def print_info_jarvis_env(result):
    try:
        results_list.append("\n-----------------------------------------------\n")
        results_list.append("\n----------------------PI-----------------------\n")

        for variable in variables_to_check_jarvis_env:
            get_value_from_file(result, variable)

    except subprocess.CalledProcessError as e:
        results_list.append(f"Erro ao executar o comando: {e}")
    except Exception as e:
        results_list.append(f"Erro inesperado: {e}")


def get_value_from_file(result, variable):
    for key, value in variable.items():
        match = re.search(fr'{key}=(\S+)', result, re.IGNORECASE)
        if match:
            globals()[value] = match.group(1) == 'TRUE'
            results_list.append(f"{key}= {match.group(1)}")
        else:
            results_list.append(f'{key} = N/A')


if __name__ == "__main__":
    exec_cache_existence()

    # Imprime os resultados no final

    print("aa")
    for result in results_list:
        print(result)
