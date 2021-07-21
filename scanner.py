import RPi.GPIO as GPIO

import settings
from class_beep import beep
from pn532 import PN532_SPI


class RFIDScanner(object):
    scanner = None

    def __init__(self):
        self.scanner = PN532_SPI(debug=settings.DEBUG, reset=20, cs=4)

        if settings.DEBUG:
            ic, ver, rev, support = self.scanner.get_firmware_version()
            print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

        self.scanner.SAM_configuration()

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()

    def wait_for_scan(self):
        if settings.DEBUG:
            print("Waiting for RFID/NFC card...")

        uid = None
        while uid is None:
            uid = self.scanner.read_passive_target(timeout=0.5)

        uid_string = "".join([hex(i) for i in uid])
        beep()
        if settings.DEBUG:
            print("Found card with UID: {}".format(uid_string))

        return uid


if __name__ == "__main__":
    uid = RFIDScanner().wait_for_scan()
