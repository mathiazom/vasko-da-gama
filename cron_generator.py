import sys
from typing import Optional

from config import Config
from definitions import APP_ROOT


def generate_cron_job(reminder_id, reminder_schedule, reminder_method, cron_config) -> Optional[str]:
    if len(sys.argv) < 1:
        print("[ERROR] No output file path provided")
        return None
    return (
        f"{reminder_schedule} "
        f"cd {cron_config.vasko_dir} || exit 1; PATH=$PATH:/usr/local/bin "
        f"{cron_config.python_path} -u vasko.py {reminder_method} {reminder_id} >> {cron_config.log_path} 2>&1"
        "\n"  # Empty line to please the cron gods ...
    )


def main():
    if len(sys.argv) <= 1:
        print("[FAIL] Missing crontab destination argument")
        return
    config = Config.from_config_file(APP_ROOT / "config.yaml")
    crontab = ""
    method = config.reminders.method
    for reminder_id, s in config.reminders.schedule.items():
        if method == "direct":
            cron_schedule = f"{s.minute} {s.hour} * * {s.weekday}"
        elif method == "schedule":
            cron_schedule = config.cron.scheduling_schedule
        else:
            print(f"[FAIL] Invalid reminders method '{method}")
            return
        cronjob = generate_cron_job(reminder_id, cron_schedule, method, config.cron)
        if cronjob is not None:
            crontab += cronjob
    with open(sys.argv[1], "w+") as cron_file:
        cron_file.write(crontab)


if __name__ == '__main__':
    main()
