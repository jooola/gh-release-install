from typing import Optional


class Log:
    # Use a negative value to disable logs
    levels = ("error", "info", "debug")
    level = 0

    @staticmethod
    def log(level: int, message: str):
        if Log.level >= level:
            print(f"{Log.levels[level]}: {message}")

    @staticmethod
    def error(message: str):
        Log.log(0, message)

    @staticmethod
    def info(message: str):
        Log.log(1, message)

    @staticmethod
    def debug(message: str):
        Log.log(2, message)

    @staticmethod
    def set_level(level: Optional[int]):
        if level is not None:
            Log.level = min(max(level, -1), 2)
