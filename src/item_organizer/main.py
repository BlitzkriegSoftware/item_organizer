from applogger.applogger import configure_logging


def main():
    message: str = "item-organizer start up"
    logger = configure_logging()
    logger.info(message)
    print(message)


if __name__ == "__main__":
    main()
