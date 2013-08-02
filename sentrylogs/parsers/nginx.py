#
# parse a tipical nginx error log like this
#
# 2012/11/29 19:30:02
# [error] 15596#0: *4 open() "/srv/active/collected-static/50x.html" failed (2: No such file or directory),
# client: 65.44.217.34,
# server: ,
# request: "GET /api/megapage/poll/?cursor=1354216956 HTTP/1.1",
# upstream: "http://0.0.0.0:9000/api/megapage/poll/?cursor=1354216956",
# host: "165.225.132.103",
# referrer: "http://165.225.132.103/megapage/"


from string import strip
import re
import logging
from datetime import datetime, timedelta
from dateutil.tz import tzoffset

def nginx_error_parser(line):
    csv_list = line.split(",")
    date_time_message = csv_list.pop(0).split(" ",2)
    otherinfo = dict()

    raise Exception(date_time_message[2])

    for l in csv_list:
        kv = l.split(":",1)
        if len(kv)>0:
            value = strip(kv[1])
            if not value:
                value = "-"
        else:
            value = "-"
        otherinfo[strip(kv[0])] = value

    otherinfo['log_level'] = logging.ERROR

    return date_time_message, otherinfo

def nginx_access_parser(line):
    m = re.search('^(?P<ip>[\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}) - - \[(?P<date>[\w\W]+)\] "(?P<request>[\w\W^"]+)" (?P<status>[\d]{3}) (?P<proc>[\d]+) "(?P<server>[\w\W^"]+)" "(?P<useragent>[\w\W^"]+)$', line)

    dt = m.group('date')
    dt_str = dt.split(" ")
    dt = datetime.strptime(dt_str[0], "%d/%b/%Y:%H:%M:%S")
    dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tzoffset(None, timedelta(hours=int(dt_str[1][0:-2]), minutes=int(dt_str[1][-2:])).total_seconds()))

    otherinfo = dict(ip=m.group('ip'), request_str=m.group('request'), status=m.group('status'), server=m.group('server'), useragent=m.group('useragent'))

    otherinfo['log_level'] = logging.INFO

    return dt.strftime("%Y/%b/%d %H:%M:%S").split(" ")+[m.group('request')], otherinfo
