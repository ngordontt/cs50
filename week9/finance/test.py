import datetime

dt=datetime.datetime.strptime("20180112220241","%Y%m%d%H%M%S")
dt = datetime.datetime.strftime(dt,"%c")
print(dt)