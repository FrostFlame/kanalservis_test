from apscheduler.schedulers.background import BackgroundScheduler

from web.notifier.script import notify


def start():
    """
    Запуск планировщика Telegram-нотифаера.
    Задача отрабатывает каждый день в 10:00.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(notify, 'cron', day='*', hour=10)
    scheduler.start()
