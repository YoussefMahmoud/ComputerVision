from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


class Volume:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

    def get_volume(self):
        # get current dB level and convert to percent
        level = self.volume.GetMasterVolumeLevel()
        min_vol, max_vol, _ = self.volume.GetVolumeRange()
        percent = np.interp(level, [min_vol, max_vol], [0, 100])
        return round(percent)

    def volume_down(self, step_db=2.0):
        level = self.volume.GetMasterVolumeLevel() - step_db
        self.volume.SetMasterVolumeLevel(level, None)

    def volume_up(self, step_db=2.0):
        level = self.volume.GetMasterVolumeLevel() + step_db
        self.volume.SetMasterVolumeLevel(level, None)


if __name__ == "__main__":
    vol = Volume()
    print("Current volume:", vol.get_volume(), "%")
    vol.volume_down()
    print("After volume down:", vol.get_volume(), "%")
