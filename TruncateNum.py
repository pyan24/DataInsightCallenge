
import re

# Convert a floating number to 2 decimal places number
class CTruncateNum(float):
    def __init__(self,num):
        self.t = num

    def ChopNum(self):
        #truncate number only keep 2 decimal places
        str1=str("%.3f" % self.t)
        str2='.'
        result = str1[:str1.index(str2)+3]+'\n'
        return result