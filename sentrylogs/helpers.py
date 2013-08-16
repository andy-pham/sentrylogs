from raven import Client
import logging
import datetime

def send_message(message, params, site, logger,
        interface_type="sentry.interfaces.Message",
        log_level=logging.ERROR, sentry_dsn=None):
    data={
        'site': site,
        'logger': logger,
    }

    if sentry_dsn:
        client = Client(dsn=sentry_dsn)
    else:
        raise Exception("No Sentry DSN")

    if "request" in params.keys():
        interface_type = "sentry.interfaces.Http"
        data[interface_type] = params["request"]
    else:
        data[interface_type] = message
    
    if params["QueryObject"] and params["QueryObject"] != "-":
        tags = params["QueryObject"]
    else:
        tags = None
        
    if params["urlpath"] and params["urlpath"] != "-":
        if not tags:
            tags = {}
        tags["UrlPath"] = params["urlpath"]
    
    if params["ip"] and params["ip"] != "-":
        if not tags:
            tags = {}
        tags["UserIP"] = params["ip"]
    
    date = datetime.datetime.strptime("%s %s" % (params["date"],params["time"]), "%Y/%b/%d %H:%M:%S")
    
    subject = message.get("message", message.get("url", "Unknown Message"))

    client.capture(
        'Message',
        message=subject,
        data=data,
        level=log_level,
        extra=params,
        tags=tags,
        date=date
    )
