class Log:
    levels = ("quiet", "error", "info", "debug")
    level = 1

    @staticmethod
    def log(level: int, message: str):
        if Log.level >= level:
            print(f"{Log.levels[level]}: {message}")

    @staticmethod
    def error(message: str):
        Log.log(1, message)

    @staticmethod
    def info(message: str):
        Log.log(2, message)

    @staticmethod
    def debug(message: str):
        Log.log(3, message)
