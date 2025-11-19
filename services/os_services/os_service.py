from platform import system

def OSService():
    current = system()

    if current == "Windows":
        from services.os_services.windows_os_service import WindowsOSService
        return WindowsOSService()

    elif current == "Linux":
        from services.os_services.linux_os_service import LinuxOSService
        return LinuxOSService()

    elif current == "Darwin":
        from services.os_services.mac_os_service import MacOSService
        return MacOSService()

    else:
        raise Exception(f"OS no soportado: {current}")
