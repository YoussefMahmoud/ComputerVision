from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#getting a list of current speakers
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

#getting the volume level
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume_level = volume.GetMasterVolumeLevel()
range = volume.GetVolumeRange()

class Volume():
    def volume():
        vol = np.interp(volume_level, [-37, 0], [0, 100])


    def volume_down():
        volume_level = volume_level - 2
        volume.SetMasterVolumeLevel(volume_level, None)

    def volume_up():
        volume_level = volume_level + 2
        volume.SetMasterVolumeLevel(volume_level, None)
