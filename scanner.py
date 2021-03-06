from time import sleep

import requests
import RPi.GPIO as GPIO

import settings
from class_beep import beep
from pn532 import PN532_SPI


class RFIDScanner(object):
    scanner = None

    endpoint_url = "https://firefox.vryhof.net/api/catalog/rfid/"

    def __init__(self):
        try:
            self.scanner = PN532_SPI(debug=settings.PN532_DEBUG, reset=20, cs=4)
        except RuntimeWarning:
            print("Cleaning up GPIO Channels.")
            GPIO.cleanup()
            self.scanner = PN532_SPI(debug=settings.PN532_DEBUG, reset=20, cs=4)


        if settings.DEBUG or settings.PN532_DEBUG:
            ic, ver, rev, support = self.scanner.get_firmware_version()
            print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

        self.scanner.SAM_configuration()

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()

    def lookup_item(self, rfid_id):
        resp = requests.post(self.endpoint_url, data=dict(rfid_id=rfid_id))

        if settings.DEBUG:
            print(resp.text)

        sleep(0.3)
        
        self.wait_for_scan()

    def wait_for_scan(self):
        if settings.DEBUG:
            print("Waiting for RFID/NFC card...")

        uid = None
        while uid is None:
            uid = self.scanner.read_passive_target(timeout=0.5)

        uid_string = "".join([hex(i) for i in uid])
        self.lookup_item(uid_string)
        beep()

        if settings.DEBUG:
            print("Found card with UID: {}".format(uid_string))

        return uid


if __name__ == "__main__":
    uid = RFIDScanner().wait_for_scan()
