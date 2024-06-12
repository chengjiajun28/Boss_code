import logging
import os
from logging.handlers import TimedRotatingFileHandler
import platform


def get_logger(modulename):
    # 日志打印格式
    log_fmt = '%(asctime)s %(levelname)s: %(message)s'
    formatter = logging.Formatter(log_fmt)

    # 创建TimedRotatingFileHandler对象
    logfile = f"./log/{modulename}.log"
    dirname = os.path.dirname(os.path.abspath(logfile))
    os.makedirs(dirname, exist_ok=True)
    log_file_handler = TimedRotatingFileHandler(filename=logfile, when="midnight", backupCount=30, encoding="utf-8")
    log_file_handler.setFormatter(formatter)

    # 设置日志记录级别为INFO
    logger = logging.getLogger(modulename)
    logger.setLevel(logging.INFO)
    logger.addHandler(log_file_handler)

    return logger


plat = platform.system().lower()

# 在不同的代码文件中导入对应的logger并使用
# 示例代码
# 在代码文件1中
# modulename = "module1"
# logger1 = get_logger(modulename)
# logger1.info("Message from code file 1")
# logger1.error("Error message from code file 1")

# 在代码文件2中
# modulename = "module2"
# logger2 = get_logger(modulename)
# logger2.info("Message from code file 2")
# logger2.error("Error message from code file 2")
