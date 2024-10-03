import ecs_logging
import logzero


# StdlibFormatter helps creating logs in json format
# A custom class here, helps us with easy addition of more fields according to our use-case
# Feel free to use StdlibFormatter directly, incase you don't want to add more fields
class APMLogFormatter(ecs_logging.StdlibFormatter):
    def format(self, record):
        result = super().format(record=record)
        return result


def initialize():
    log_formatter = APMLogFormatter(
        exclude_fields=[
            "event",  # this causes troubles with logging on apm service
        ]
    )
    logzero.json()
    logzero.formatter(log_formatter)
    logzero.loglevel(logzero.INFO)
