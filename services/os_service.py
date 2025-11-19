from platform import system

def OSService():
    current = system()

    if current == "Windows":
        from services.windows_os_service import WindowsOSService
        return WindowsOSService()

    elif current == "Linux":
        from services.linux_os_service import LinuxOSService
        return LinuxOSService()

    elif current == "Darwin":
        from services.mac_os_service import MacOSService
        return MacOSService()

    else:
        raise Exception(f"OS no soportado: {current}")
