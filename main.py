from __future__ import division

import os
import xml.etree.ElementTree as ET
from subprocess import DEVNULL, STDOUT, check_call

from wox import Wox

pycharm_recent_xml = r"C:\Users\David\.PyCharm2016.1\config\options\recentProjectDirectories.xml"
pycharm_exe = r"C:\Program Files (x86)\JetBrains\PyCharm 2016.1.4\bin\pycharm.exe"


class WOXPyCharm(Wox):
    def query(self, key):
        results = []

        path_list = []
        tree = ET.parse(pycharm_recent_xml)
        root = tree.getroot()
        component = root.find("component")
        if not component:
            return results
        recent_paths = None
        for option in component.findall("option"):
            if "name" in option.attrib:
                if option.attrib["name"] == "recentPaths":
                    recent_paths = option
                    break
        if not recent_paths:
            return results
        option_list = recent_paths.find("list")
        if not option_list:
            return results
        for option in option_list.findall("option"):
            if "value" in option.attrib:
                if option.attrib["value"]:
                    path_list.append(option.attrib["value"])

        for path in path_list:
            results.append({"Title": "PyCharm: " + os.path.basename(os.path.normpath(path)), "SubTitle": path,
                            "IcoPath": "Images\\app.png",
                            "JsonRPCAction": {"method": "open_pycharm", "parameters": [path],
                                              "dontHideAfterAction": False}})

        return results

    def open_pycharm(self, path):
        try:
            check_call([pycharm_exe, os.path.normpath(path)], stdout=DEVNULL, stderr=STDOUT)
        except Exception:
            pass


if __name__ == "__main__":
    WOXPyCharm()
