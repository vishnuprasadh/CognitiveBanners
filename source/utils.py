import time
import datetime

def currentimeInFormat(format="%d-%b-%y %H:%M:%S"):
    nowtime = datetime.datetime.now().timetuple()
    ftime = time.strftime(format,nowtime)
    return ftime