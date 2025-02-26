import sys

from loguru import logger


logger.remove()
log_format_base = (
    " | "
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<yellow>{file.name}:{function}</yellow>:"
    "<fg #006400>{line}</fg #006400>\n"
    "{message}"
)
log_formats = {
    "INFO": f" <blue>{{level}}</blue>{log_format_base}",
    "DEBUG": f" <cyan>{{level}}</cyan>{log_format_base}",
    "WARNING": f" <yellow>{{level}}</yellow>{log_format_base}",
    "ERROR": f" <red>{{level}}</red>{log_format_base}",
}


def create_filter(log_level: str):
    return lambda record: record["level"].name == log_level


log_format_file = (
    " {level} | {time:YYYY-MM-DD HH:mm:ss} | "
    "{file.name}:{function}:{line}\n{message}"
)

for level, log_format in log_formats.items():
    logger.add(
        sys.stdout,
        format=log_format,
        level=level,
        filter=create_filter(level),
    )

logger.add(
    "bot.log",
    rotation="500 MB",
    retention="10 days",
    format=log_format_file,
)
