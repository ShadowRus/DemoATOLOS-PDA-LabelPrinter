import subprocess
import time
import os
import signal
import socket
from logger.logger_config import logger
from configuration.system_config import PORT

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def start_application_server():
    logger.info(f'start application')
    return subprocess.Popen(["uvicorn", "start_server:app", "--reload", "--host", f"{extract_ip()}", "--port", f"{PORT}"])
def start_application_ui():
    logger.info(f'start application web_ui')
    return subprocess.Popen(["streamlit","run", "./web_ui/admin_console.py"])


def main():
    process = start_application_server()
    process_2 = start_application_ui()

    while True:
        try:
            # Ожидание сигнала на необходимость перезапуска.
            pid, status = os.wait()
            if os.WIFSIGNALED(status) and os.WTERMSIG(status) == signal.SIGUSR1:

                logger.info("Received restart signal")
                process.terminate()
                process.wait()
                time.sleep(0.5)
                process = start_application_server()

        except ChildProcessError:
            # Если родительский процесс завершился, выйти из цикла.
            break


if __name__ == "__main__":
    main()
