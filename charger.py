from adbcmd import adbcmd

if __name__ == "__main__":
    adb = adbcmd('F8UDU15519010985')
    level = adb.get_batterylevel()
    if level<20:
        adb.enable_charger(True)

    if level>90:
        adb.enable_charger(False)