import subprocess
import re
import requests

class GoogleGeoLocator:
    def __init__(self, api_key):
        self.api_key = api_key

    def is_valid_mac(self, mac):
        return re.fullmatch(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", mac) is not None

    def get_wifi_interface(self):
        output = subprocess.check_output(["iw", "dev"]).decode()
        match = re.search(r"Interface\s+(\S+)", output)
        if not match:
            raise RuntimeError("No se encontró interfaz Wi-Fi.")
        return match.group(1)

    def scan_wifi_iw(self):
        iface = self.get_wifi_interface()
        output = subprocess.check_output(["sudo", "iw", "dev", iface, "scan"]).decode()

        networks = []
        blocks = output.split("BSS ")

        for blk in blocks[1:]:
            m_bssid = re.search(r"([0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5})", blk)
            m_signal = re.search(r"signal:\s+(-?\d+\.?\d*)", blk)

            if not m_bssid:
                continue

            mac = m_bssid.group(1).strip()
            if not self.is_valid_mac(mac):
                continue

            rssi = int(float(m_signal.group(1))) if m_signal else -60

            networks.append({
                "macAddress": mac,
                "signalStrength": rssi
            })

        return networks

    def geolocate_google(self):

        networks = self.scan_wifi_iw()

        url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={self.api_key}"

        payload = {
            "wifiAccessPoints": networks
        }

        resp = requests.post(url, json=payload)
        location = resp.json().get("location", {})
        return location.get("lat", 0), location.get("lng", 0)
