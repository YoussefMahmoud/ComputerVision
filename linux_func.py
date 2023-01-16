import os
import re



class Volume():
    #getting the current volume level
    def volume():
        #regex to extract the volume level from command line
        percentage_regex = re.compile(r'\d{1,3}.?\d{0,2}%')
        volume_level = re.findall(percentage_regex, os.popen('amixer -D pulse get Master').read())
        #reading the volume level from command line
        return volume_level[1]
    
    #raising the volume level by 5%
    def volume_up():
        os.system('amixer -q -D pulse sset Master 5%+')
    #reducing the volume level by 5%
    def volume_down():
        os.system('amixer -q -D pulse sset Master 5%-')

