import logging

# Application logger
logger = logging.getLogger("gnosis")
logger.setLevel(logging.INFO)

if not logger.handlers:
    app_handler = logging.FileHandler("app.log")
    app_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(app_handler)

# processing Metrics logger
metrics_logger = logging.getLogger("processing")
metrics_logger.setLevel(logging.INFO)

if not metrics_logger.handlers:
    metrics_handler = logging.FileHandler("processing.log")
    metrics_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    metrics_logger.addHandler(metrics_handler)


# search Metrics logger
# s_metrics_logger = logging.getLogger("search")
# s_metrics_logger.setLevel(logging.INFO)

# if not s_metrics_logger.handlers:
# s_metrics_handler = logging.FileHandler("search.log")
# s_metrics_handler.setFormatter(
#     logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# )
# s_metrics_logger.addHandler(s_metrics_handler)

