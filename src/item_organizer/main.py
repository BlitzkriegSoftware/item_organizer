from applogger.applogger import configure_logging


def main():
    logger = configure_logging()
    logger.info("item-organizer start up")


if __name__ == "__main__":
    main()
