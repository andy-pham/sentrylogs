import tailer # same functionality ad UNIX tail in python
from parsers.nginx import nginx_error_parser, nginx_access_parser
from helpers import send_message
import logging

def nginx(opts=None):
    filepaths = {}

    nginx_error_path = getattr(opts, "nginxerrorpath", False)
    nginx_access_path = getattr(opts, "nginxaccesspath", False)
    
    if nginx_error_path:
        filepaths["error"] = {"filepath": nginx_error_path, "parser": nginx_error_parser}
    if nginx_access_path:
        filepaths["access"] = {"filepath": nginx_access_path, "parser": nginx_access_parser}

    for k,v in filepaths.iteritems():
        logger = "Nginx %s logs" % k
	filepath = v['filepath']
        parser = v['parser']

        try:
            f = open(filepath)
        except:
            continue
        else:
            f.close()

        for line in tailer.follow(open(filepath)):

            # create the message
            date_time_message, otherinfo = parser(line, addcalltime=opts.calltime)
            params = {
		         "message": date_time_message[2],
                         "date": date_time_message[0],
                         "time": date_time_message[1],
            }

            for k,v in otherinfo.iteritems():
               params[k] = v

            if "log_level" in params.keys():
                log_level = params.get("log_level", logging.ERROR)
                del params['log_level']
            else:
                log_level = params.get("log_level", logger.ERROR)

            message = {'message': '%s' % date_time_message[2]}
            message['extended_message'] =  '%s\n'\
                                'Date: %s\n'\
                                'Time: %s\n'\
                                'Request: %s\n'\
                                'Referrer: %s\n'\
                                'Server: %s\n'\
                                'Client: %s\n'\
                                'Host: %s\n'\
                                'Upstream: %s\n'
            site = otherinfo.get("referrer", otherinfo.get("ip", "-"))

            # send the message to sentry using Raven
            send_message(message, params, site, logger, log_level=log_level, sentry_dsn=opts.sentrydsn)
