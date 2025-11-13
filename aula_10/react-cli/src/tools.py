
import platform
import psutil
import socket
import datetime
import os
import uuid

try:
    import GPUtil
except ImportError:
    GPUtil = None


def get_system_info():
    """Retorna informações gerais e de desempenho do sistema."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat()

    info = {
        "session_id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "system_info": {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "username": os.getlogin(),
            "boot_time": boot_time
        },
        "performance": {
            "cpu_percent": cpu_percent,
            "cpu_count": psutil.cpu_count(),
            "memory_total_gb": round(memory.total / (1024 ** 3), 2),
            "memory_used_gb": round(memory.used / (1024 ** 3), 2),
            "memory_percent": memory.percent,
            "disk_total_gb": round(disk.total / (1024 ** 3), 2),
            "disk_used_gb": round(disk.used / (1024 ** 3), 2),
            "disk_percent": disk.percent,
        }
    }

    # GPU (se disponível)
    if GPUtil:
        gpus = GPUtil.getGPUs()
        if gpus:
            info["gpu"] = [
                {
                    "id": gpu.id,
                    "name": gpu.name,
                    "load_percent": round(gpu.load * 100, 2),
                    "memory_used_gb": round(gpu.memoryUsed / 1024, 2),
                    "memory_total_gb": round(gpu.memoryTotal / 1024, 2),
                    "temperature_c": gpu.temperature,
                }
                for gpu in gpus
            ]
        else:
            info["gpu"] = None

    return info 