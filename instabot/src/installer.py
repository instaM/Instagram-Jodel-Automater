import platform
import os
class Installer:
    chrome_win_10="C:\\Program Files(x86)\\Google\\Chrome\\Application\\chrome.exe"
    chrome_win_7="C:\\Program Files(x86)\\Google\\Application\\chrome.exe"
    chrome_win_vista="C:\\Users\\%s\\AppDataLocal\\Google\\Chrome"%(os.getlogin())
    chrome_win_8  = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    chrome_ubuntu_16_04 ="/usr/bin/chromium-browser"
    chrome_mac = "/Applications/Google\\Chrome.app/Contents/MacOS/Google\\Chrome"


    def get_chrome_path(self):
        os_name = platform.system()
        chrome_path = "";
        if(os_name == "Windows"):
            win_name = platform.release()
            if(win_name == "10"):
                chrome_path = self.chrome_win_10
            elif(win_name == "7"):
                chrome_path = self.chrome_win_7

            elif (win_name == "7"):
                chrome_path = self.chrome_win_8
            else:
                chrome_path = self.chrome_win_vista
        elif(os_name == "Mac"):
            chrome_path = self.chrome_mac
        else:
            chrome_path = self.chrome_ubuntu_16_04
        if(self.file_exists(chrome_path)):
            return chrome_path
        else:
            return None
    def file_exists(self,file_path):

        return os.path.isfile(file_path)
