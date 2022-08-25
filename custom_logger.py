import logging, coloredlogs


def initialize_logger(logger_level):
    # Create a logger object.
    # logging.basicConfig(format="%(levelname)s:%(message)s")
    # formatter = logging.Formatter("%(asctime)s %(levelname)s:%(message)s")
    coloredlogs.install(
        level=logger_level, fmt="%(asctime)s | %(levelname)s:%(message)s \n"
    )
    logging.debug(" Logger initialized ")
    # logging.info("Info message")
    # logging.warning("WarningHo")
    # logging.error("Error Ho")
    # logging.critical("Critical Ho")
    # logging.debug("Debug Ho")
