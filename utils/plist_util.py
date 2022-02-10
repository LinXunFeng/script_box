import subprocess


class PlistUtil:
    def __init__(self, path):
        self.path = path

    def getValueForKey(self, key):
        pipe = subprocess.Popen(["/usr/libexec/PlistBuddy", "-c", "Print " + key, self.path], stdout=subprocess.PIPE)
        result, _ = pipe.communicate()
        return result

    def setValueForKey(self, key, value):
        subprocess.call(["/usr/libexec/PlistBuddy", "-c", "Set :" + key + " " + value, self.path])

    def addValueForKey(self, key, type, value):
        subprocess.call(["/usr/libexec/PlistBuddy", "-c", "Add :" + key + " " + type + " " + value, self.path])

    def delValueForKey(self, key):
        subprocess.call(["/usr/libexec/PlistBuddy", "-c", "Delete :" + key, self.path])
