from datetime import datetime,timedelta
import time
now = datetime.now()
ti = time.time()


print now
print now + timedelta(hours= 1), now + timedelta(days=1), now + timedelta(days=1, hours=2, minutes=3, seconds=4)





print ti
print datetime.fromtimestamp(ti)

dt = datetime(2014, 10, 10, 12, 30, 40)
print dt
dts =  1429417200.0
dtss = dt.timetuple()
print dt
print  datetime.fromtimestamp(dts)
print dtss
