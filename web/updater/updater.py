from apscheduler.schedulers.background import BackgroundScheduler

from web.updater.script import update_db


def start():
    """
    Запуск планировщика обновителя БД.
    Задача отрабатывает каждые 5 минут.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_db, 'interval', minutes=5)
    scheduler.start()
