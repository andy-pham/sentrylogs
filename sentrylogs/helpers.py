from raven import Client
import logging

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

    data[interface_type] = message
    subject = message.get("message", message.get("url", "Unknown Message"))

    client.capture(
        'Message',
        message=subject,
        data=data,
        level=log_level,
        extra=params
    )
