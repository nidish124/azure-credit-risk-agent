from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging
import sys, os

def setup_logger():
    logger = logging.getLogger("credit_decision")
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s")
    stream_handler.setFormatter(formatter)

    # if not logger.handlers:
    #     logger.addHandler(handler)
    
    # return logger

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        logger.addHandler(stream_handler)

    ai_connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

    if ai_connection_string and not any(
        isinstance(h, AzureLogHandler) for h in logger.handlers
    ):
        ai_handler = AzureLogHandler(
            connection_string=ai_connection_string
        )
        ai_handler.setFormatter(formatter)
        logger.addHandler(ai_handler)

    return logger