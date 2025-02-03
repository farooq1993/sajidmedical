from cron_base_setup import *
from django.utils import timezone
from datetime import datetime, timedelta
from healthcare.utils import db_helper,constants
from healthcare.models.master_model import CronScriptLock

today_date = timezone.now().date()
# from_date = timezone.now().date() - timedelta(days=2)
current_time = datetime.now().time()
from_time = datetime.combine(datetime.today(), current_time) - timedelta(minutes=30)

def main(cron_script_obj):
    try:
        if cron_script_obj.is_one_time_cron:
            if cron_script_obj.one_time_cron_status == CronScriptLock.RUNNING:
                return True
            db_helper.update_cron_status_one_time_cron(cron_script_obj, CronScriptLock.RUNNING)
            get_appointment_lst = db_helper.get_appointment({"is_active":constants.ACTIVE,"current_time": current_time})
            logger.info(f"CronName:update_appointment_status -- MethodName:main objects got--- {get_appointment_lst}")
            logger.info(f"CronName:update_appointment_status -- MethodName:main objects got--- {get_appointment_lst.count()}")
            if not get_appointment_lst:
                db_helper.update_cron_status_one_time_cron(cron_script_obj, CronScriptLock.STOPPED)
                return False
            get_appointment_lst.update(is_active=False)
            db_helper.update_cron_status_one_time_cron(cron_script_obj, CronScriptLock.STOPPED)
        else:
            if cron_script_obj.regular_cron_status == CronScriptLock.RUNNING and not db_helper.check_cron_date(cron_script_obj):
                return True
            db_helper.update_cron_status_regular_cron(cron_script_obj, CronScriptLock.RUNNING)
            get_appointment_lst= db_helper.get_appointment({
                "date":today_date, "current_time": current_time,"is_active":constants.ACTIVE
                })
            logger.info(f"CronName:update_appointment_status -- MethodName:main objects got--- {get_appointment_lst}")
            logger.info(f"CronName:update_appointment_status -- MethodName:main objects got--- {get_appointment_lst.count()}")
            if not get_appointment_lst:
                db_helper.update_cron_status_regular_cron(cron_script_obj, CronScriptLock.STOPPED)
                return False
            get_appointment_lst.update(is_active=False)
            db_helper.update_cron_status_regular_cron(cron_script_obj, CronScriptLock.STOPPED)
    except Exception as ex:
        logger.error(str(ex))
        logger.exception(f"Exception Occur The Cron:update_appointment_status and The method:main ----{ex}")
        return False



if __name__ == '__main__':
    try:
        logger.info("update_appointment_status " + str(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S UTC")))
        cron_script_obj = db_helper.check_script_log("update_appointment_status")
        logger.info(
            f"update_appointment_status has started  at {str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S UTC'))}")
        main(cron_script_obj)
        logger.info(
            f"update_appointment_status has completed at {str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S UTC'))}")
    except Exception as ex:
        logger.exception(f"Exception Occur The Cron:update_appointment_status and The method:__name__ ----{ex}")
