from loguru import logger
import sys

# Удаляем все существующие обработчики (если они есть)
logger.remove()

# Настраиваем новый обработчик, который будет записывать логи в файл с ротацией при достижении определенного размера
logger.add("./log/app.log", rotation="10 MB", retention="10 days", compression="zip")

# Настраиваем вывод в консоль с уровнем DEBUG
logger.add(sys.stdout, level="DEBUG")
