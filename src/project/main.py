import logging
import atexit
import os
import sys

                                                                                 
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                                                    
env_path = os.path.join(project_root, "..", ".env")
env_path = os.path.abspath(env_path)
os.environ["DOTENV_PATH"] = env_path

                                                    
LOG_FILENAME = os.path.join(project_root, "..", "log.txt")
log_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)-5.5s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

                                  
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

                                
try:
    file_handler = logging.FileHandler(LOG_FILENAME, encoding='utf-8', mode='w')
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
except Exception as e:
    print(f"Не удалось настроить логирование в файл {LOG_FILENAME}: {e}")

                                   
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)

logging.info("Логирование настроено. Вывод в консоль и файл %s", LOG_FILENAME)
logging.info(f"Путь к .env файлу: {env_path}")

                                     
from PySide6.QtWidgets import QApplication
from gui import create_gui


def setup_api():
    try:
        from osu_api import setup_api_keys, restore_env_defaults

                                           
        if not setup_api_keys():
                                                                     
            logging.warning("API ключи не настроены. Будет предложено ввести их через интерфейс.")
            return True                                

        return True
    except Exception as e:
        logging.exception(f"Ошибка при настройке API: {e}")
        return True                                                


def main():
                                                           
    app = QApplication(sys.argv)

                                                 
    if not setup_api():
        return 1

                   
    window = create_gui()

                                      
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())