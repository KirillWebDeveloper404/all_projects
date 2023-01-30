from datetime import datetime

import pytz

time_zone = pytz.timezone("Etc/GMT-3")
datetime_now = datetime.now(tz=time_zone)
print(datetime_now)