# coding=utf-8

import functools
import subprocess
# from io import BytesIO

# from PIL import Image

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
        cmd = f"adb -s {self.device_serial} connect {ip}:{port}".split()    # noqa
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
        cmd = f"adb -s {self.device_serial} exec-out wm size".split()
        result = _sysrun(cmd)
        w, h = result.stdout.decode().split("Physical size: ")[-1].split("x")
        return (int(w), int(h))

    def screencap(self, fname):
        """截图，输出为 Pillow.Image 对象"""
        cmd = f"adb -s {self.device_serial} exec-out screencap -p".split()
        result = _sysrun(cmd)
        with open(fname, 'wb') as f:
            f.write(result.stdout)
        # img = Image.open(BytesIO(result.stdout))
        # return img

    def short_tap(self, cord):
        """短按点击，坐标为 (x, y) 格式"""
        cmd = f"adb -s {self.device_serial} exec-out input tap {cord[0]} {cord[1]}".split()
        result = _sysrun(cmd)
        if result.returncode != 0:
            raise ShortTapError(result.stderr.decode().strip())

    def long_tap(self, cord, duration):
        """长按, duration单位为ms，坐标为 (x, y) 格式"""
        cmd = f"adb -s {self.device_serial} exec-out input swipe {cord[0]} {cord[1]} {cord[0]} {cord[1]} {duration}".split()
        result = _sysrun(cmd)
        if result.returncode != 0:
            raise LongTapError(result.stderr.decode().strip())

    def swipe(self, cord):
        """长按, duration单位为ms，坐标为 (x1, y1, x2, y2) 格式"""
        cmd = f"adb -s {self.device_serial} exec-out input swipe {cord[0]} {cord[1]} {cord[2]} {cord[3]}".split()
        result = _sysrun(cmd)
        if result.returncode != 0:
            raise LongTapError(result.stderr.decode().strip())

    def key(self, keycode):
        cmd = f"adb -s {self.device_serial} exec-out input keyevent {keycode}".split()
        result = _sysrun(cmd)
        if result.returncode != 0:
            raise ADBError(result.stderr.decode().strip())

    def _locked(self):
        cmd = f"adb -s {self.device_serial} exec-out dumpsys power".split()
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
