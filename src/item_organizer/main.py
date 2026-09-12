from app_logger.applogger import AppLogger


def main():
    message: str = "item-organizer start up"
    logger = AppLogger.logger_get()
    logger.info(message)
    print(message)


if __name__ == "__main__":
    main()
