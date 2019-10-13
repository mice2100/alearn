# coding=utf-8

import functools
import subprocess
from io import BytesIO
from PIL import Image

_sysrun = functools.partial(
    subprocess.run,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)


class ADBError(Exception):
    pass


class ConnectionError(ADBError):
    pass


class LongTapError(ADBError):
    pass


class ShortTapError(ADBError):
    pass


class adbcmd:

    def __init__(self, device_serial):
        self.device_serial = device_serial

    def connect(self, ip, port=5555):
        """连接网络adb调试设备"""
        cmd = "adb -s {} connect {}:{}".format(self.device_serial, ip, port).split()    # noqa
        try:
            result = _sysrun(cmd, timeout=2)
            returncode = result.returncode
        except subprocess.TimeoutExpired as e:
            errmsg = "Connect {ip}:{port} timeout."
        else:
            if result.returncode != 0:
                raise ConnectionError(result.stderr.decode().strip())
            return "connected" in result.stdout, result.stdout
        raise ConnectionError(errmsg)

    def get_resolution(self):
        """获取屏幕分辨率"""
        cmd = "adb -s {} exec-out wm size".format(self.device_serial).split()
        result = _sysrun(cmd)
        w, h = result.stdout.decode().split("Physical size: ")[-1].split("x")
        return (int(w), int(h))

    def screencap(self, fname):
        """截图，输出为 Pillow.Image 对象"""
        cmd = "adb -s {} exec-out screencap -p".format(self.device_serial).split()
        result = _sysrun(cmd)
        with open(fname, 'wb') as f:
            f.write(result.stdout)
        # img = Image.open(BytesIO(result.stdout))
        # return img

    def screencapImg(self):
        """截图，输出为 Pillow.Image 对象"""
        cmd = "adb -s {} exec-out screencap -p".format(self.device_serial).split()
        result = _sysrun(cmd)
        img = Image.open(BytesIO(result.stdout))
        return img

    def short_tap(self, cord):
        """短按点击，坐标为 (x, y) 格式"""
        cmd = "adb -s {} exec-out input tap {} {}".format(self.device_serial, cord[0], cord[1]).split()
        result = _sysrun(cmd)
        if result.returncode != 0:
            raise ShortTapError(result.stderr.decode().strip())

    def long_tap(self, cord, duration):
        """长按, duration单位为ms，坐标为 (x, y) 格式"""
        cmd = "adb -s {} exec-out input swipe {} {} {} {} {}".format(self.device_serial, cord[0], cord[1], cord[0], cord[1], duration).split()
        result = _sysrun(cmd)
        if result.returncode != 0:
            raise LongTapError(result.stderr.decode().strip())

    def swipe(self, cord, duration=200):
        """长按, duration单位为ms，坐标为 (x1, y1, x2, y2) 格式"""
        cmd = "adb -s {} exec-out input swipe {} {} {} {} {}".format(self.device_serial, cord[0], cord[1], cord[2], cord[3], duration).split()
        result = _sysrun(cmd)
        if result.returncode != 0:
            raise LongTapError(result.stderr.decode().strip())

    def key(self, keycode):
        cmd = "adb -s {} exec-out input keyevent {}".format(self.device_serial, keycode).split()
        result = _sysrun(cmd)
        if result.returncode != 0:
            raise ADBError(result.stderr.decode().strip())

    def _locked(self):
        cmd = "adb -s {} exec-out dumpsys power".format(self.device_serial).split()
        result = _sysrun(cmd)
        if result.returncode != 0:
            raise ADBError(result.stderr.decode().strip())

        ret = 0
        for ln in result.stdout.decode().splitlines():
            if 'mHolding' in ln and '=false' in ln:
                ret += 1
        return ret

    def unlock(self):
        locked = self._locked()
        if locked>0:
            if locked==2:
                self.key("KEYCODE_POWER")
            self.swipe((500, 1600, 500, 800))

    def lock(self):
        locked = self._locked()
        if locked<2:
            self.key("KEYCODE_POWER")

    def startApp(self, aname):
        cmd = "adb -s {} exec-out am start {}".format(self.device_serial, aname).split()
        result = _sysrun(cmd)
        if result.returncode != 0:
            raise ADBError(result.stderr.decode().strip())

    def enable_charger(self, enable):
        cmd = "adb -s {} exec-out su -c 'echo {} > /sys/devices/huawei_charger.32/enable_charger'".format(self.device_serial, int(enable))
        # print(cmd)
        result = _sysrun(cmd, shell=True)
        if result.returncode != 0:
            raise ADBError(result.stderr.decode().strip())

    def get_batterylevel(self):
        """获取电池电量百分比"""
        cmd = "adb -s {} exec-out dumpsys battery".format(self.device_serial).split()
        result = _sysrun(cmd)
        level = result.stdout.decode().split('\n')[7].split("level: ")[-1]
        return int(level)