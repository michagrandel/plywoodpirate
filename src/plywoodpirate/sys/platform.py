# <> with ❤️ by Micha Grandel - hello@michagrandel.eu

""" platform information, and platform specific methods """

from __future__ import annotations

import os
import platform
import subprocess
import re
from typing import Optional

import nvsmi
import psutil
from apppath import AppPath

from ..string import color as clicolor


def get_processor_name() -> str:
    """ Returns the name of the CPU
    
    Returns:
        str: CPU Name
    """
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command ="sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name.*:", "", line,1)
    return ""

def get_basic_system_info(app: Optional[AppPath] = None) -> dict[str, str|bool]:
    """
    get platform information
    
    collects information about:
    - GPU Name
    - GPU Memory
    - GPU Temperature
    - CPU Name
    - Total Memory
    - Free Memory
    - Memory Warning, if memory is less than 1%
    - Total Disk space
    - Free Disk space
    - Disk Warning, if disk space is less than 10%
    - Python Version
    - Script name
    - Script version
    - Hostname
    - Platform
    
    Args:
        app(AppPath, optional): application information. Defaults to None.
    
    Returns:
        dict[str, str]: dictionary with platform information
    """
    if app is None:
        app = AppPath(app_name="unknown", app_version="unknown", ensure_existence_on_access=False)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage("/")

    gpu_info = nvsmi.get_gpus()
    gpu_information = []
    for gpu in gpu_info:
        gpu_id = gpu.id
        gpu_name = gpu.name
        gpu_temp = gpu.temperature
        gpu_driver = gpu.driver
        gpu_mem = gpu.mem_total
        gpu_details = f"{gpu_id}: {gpu_name} {gpu_driver} ({gpu_mem}/{gpu_temp}°C)"
        gpu_information.append(gpu_details)

    mem_available = memory_info.available/1024/1024/1024
    mem_total = memory_info.total/1024/1024/1024
    disk_available = disk_info.free/1024/1024/1024
    disk_total = disk_info.total/1024/1024/1024

    disk_warning = False
    if disk_available / disk_total < 0.1:
        disk_warning = True
        dsk_info = clicolor.red(f"{disk_available:3.0f} GiB / {disk_total:3.0f} GiB")
    elif disk_available / disk_total < 0.1:
        dsk_info = clicolor.yellow(f"{disk_available:3.0f} GiB / {disk_total:3.0f} GiB")
    else:
        dsk_info = f"{disk_available:3.0f} GiB / {disk_total:3.0f} GiB"


    mem_warning = False
    if mem_available / mem_total < 0.01:
        mem_warning = True
        mem_info = clicolor.red(f"{mem_available:3.0f} GiB / {mem_total:3.0f} GiB")
    elif mem_available / mem_total < 0.1:
        mem_info = clicolor.yellow(f"{mem_available:3.0f} GiB / {mem_total:3.0f} GiB")
    else:
        mem_info = f"{mem_available:3.0f} GiB / {mem_total:3.0f} GiB"

    return {
        "python": f"{platform.python_version()}",
        "script": app.app_name,
        "version": app.app_version(),
        "hostname": platform.node(),
        "platform": platform.system(),
        "cpu": get_processor_name(),
        "gpu": ";".join([g for g in gpu_information]),
        "mem": mem_info,
        "mem_warning": mem_warning,
        "disk": dsk_info,
        "disk_warning": disk_warning,
    }
