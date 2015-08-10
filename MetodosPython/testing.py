import datetime as dt
import time as tm

dt_ini = dt.datetime.now()
print dt_ini


tm.sleep(3)
dt_fin = dt.datetime.now()

interv = dt_fin-dt_ini
print "intervalo " + str(interv)
print interv.timedelta(interv)