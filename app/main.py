import subprocess
import time


def run_server():
    """Запуск сервера в отдельном процессе."""
    subprocess.Popen(["python", "app/server.py"])


def run_bot():
    """Запуск бота."""
    subprocess.Popen(["python", "app/bot.py"])


if __name__ == "__main__":
    run_server()
    time.sleep(3)  # Небольшая задержка для запуска сервера
    run_bot()
