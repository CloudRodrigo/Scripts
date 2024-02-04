#!/usr/bin/env python3

import platform
import os
import subprocess

def get_processor_info():
    try:
        result = subprocess.check_output(['lscpu']).decode('utf-8')
        print("Processor Information:")
        lines = result.split('\n')
        
        # Extraindo as informações desejadas
        model = [line.split(':', 1)[1].strip() for line in lines if 'Model name' in line][0]
        physical_cores = [line.split(':', 1)[1].strip() for line in lines if 'Core(s) per socket' in line][0]
        virtual_cores = [line.split(':', 1)[1].strip() for line in lines if 'Thread(s) per core' in line][0]
        frequency = [line.split(':', 1)[1].strip() for line in lines if 'CPU max MHz' in line][0]
        cache = [line.split(':', 1)[1].strip() for line in lines if 'L3 cache' in line][0]
        socket = [line.split(':', 1)[1].strip() for line in lines if 'Socket(s)' in line][0]
        chipset = platform.processor()

        print(f"Model name: {model}")
        print(f"Core(s) per socket: {physical_cores}")
        print(f"Thread(s) per core: {virtual_cores}")
        print(f"CPU max MHz: {frequency} MHz")
        print(f"Cache L3: {cache}")
        print(f"Socket(s): {socket}")
        print(f"Chipset: {chipset}")

    except Exception as e:
        print(f"Error getting processor information: {e}")

def get_memory_info():
    try:
        result = subprocess.check_output(['free', '-h']).decode('utf-8')
        print("\nMemory Information:")
        print(result)
    except Exception as e:
        print(f"Error getting memory information: {e}")

def get_storage_info():
    try:
        result = subprocess.check_output(['df', '-h']).decode('utf-8')
        print("\nStorage Information:")
        print(result)
    except Exception as e:
        print(f"Error getting storage information: {e}")

def has_gpu():
    try:
        result = subprocess.check_output(['lspci | grep VGA'], shell=True).decode('utf-8')
        print("\nVideo Card Information:")
        print(result)
        return "VGA" in result
    except Exception as e:
        print(f"Error checking video card: {e}")
        return False

def get_network_info():
    try:
        result = subprocess.check_output(['ifconfig']).decode('utf-8')
        print("\nNetwork Information:")
        print(result)
    except Exception as e:
        print(f"Error getting network information: {e}")

def get_temperature():
    try:
        result = subprocess.check_output(['sensors']).decode('utf-8')
        print("\nTemperature Information:")
        print(result)
    except Exception as e:
        print(f"Error obtaining temperature information: {e}")

def main():
    print(f"Operational system: {platform.system()} {platform.version()}")

    get_processor_info()
    get_memory_info()
    get_storage_info()

    if has_gpu():
        print("\nHas Video Card.")
    else:
        print("\nDoes not have a video card.")

    get_network_info()
    get_temperature()

if __name__ == "__main__":
    main()