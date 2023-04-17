from datetime import datetime, timezone, timedelta

offset = timedelta(hours=3)
MSC_TZ = timezone(offset)


def get_msc_formatted_datetime(time: datetime) -> str:
    return datetime.now(MSC_TZ).strftime('%d.%m.%Y %H:%M:%S')
