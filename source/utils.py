import time
import datetime

dateformat = "%d-%b-%y %H:%M:%S"
def currentimeInFormat(format=dateformat):
    nowtime = datetime.datetime.now().timetuple()
    ftime = time.strftime(format,nowtime)
    return ftime

def datetimeInFormat(timetoformat):
    nowtime = timetoformat.timetuple()
    ftime = time.strftime(dateformat,nowtime)
    return ftime



