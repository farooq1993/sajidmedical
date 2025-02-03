import logging
from rest_framework.response import Response
from rest_framework import status
from healthcare.utils import error_messages

logger = logging.getLogger("healthcare")
logger_excp = logging.getLogger('healthcare_excp')
# cron_logger = logging.getLogger('healthcare_cron')
# cron_logger_excp = logging.getLogger('healthcare_cron_excp')


def main_exception(view, exception, error_message=None):
    logger.error(exception)
    logger.exception("Exception raised in {} as {}".format(view, str(exception)))
    logger_excp.error(exception)
    logger_excp.exception(
        "Exception raised in {} as {}".format(view, str(exception)))
    if error_message:
        return Response(error_message, status=status.HTTP_412_PRECONDITION_FAILED)
    return Response(error_messages.GENERIC_API_FAILURE, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def start_logger_info(view, request):
    logger.info(f"{view} started....")
    logger.info(request)
    return True


def end_logger_info(view, response):
    logger.info(f"{view} ended....")
    logger.info(response)
    return True


def basic_response(message, status, view=None):
    end_logger_info(view, message)
    return Response(message, status=status)


def helper_error(view, function_name, exception):
    logger.error(view)
    logger.exception(f"Exception raised in {view},function_name={function_name} as {str(exception)}")

    logger_excp.error(exception)
    logger_excp.exception(f"Exception raised in {view} as {str(exception)}")
    return True


def logger_info(str):
    logger.info(str)
    logger_excp.info(str)
