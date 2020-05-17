from datetime import datetime
import math


"""
# Para testes:

records = [
    {'source': '48-996355555', 'destination': '48-666666666',
        'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097',
        'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097',
        'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788',
        'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788',
        'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099',
        'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697',
        'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099',
        'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697',
        'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097',
        'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788',
        'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788',
        'end': 1564627800, 'start': 1564626000}
]
"""


BASE_RATE_CALL = 0.36
BASE_RATE_MIN_DAY = 0.09
START_HOUR_DAY_TAX = 6
END_HOUR_DAY_TAX = 22
MINUTE = 60


def get_taxed_start_time(call_start):

    call_taxed_start = datetime(
        call_start.year, call_start.month, call_start.day, START_HOUR_DAY_TAX)

    if call_start < call_taxed_start:
        return call_taxed_start

    return call_start


def get_taxed_end_time(call_start, call_end):

    call_taxed_end = datetime(
        call_start.year, call_start.month, call_start.day, END_HOUR_DAY_TAX)

    if call_end > call_taxed_end:
        return call_taxed_end

    return call_end


def exists_charged_minutes(call_taxed_start, call_taxed_end):
    return call_taxed_end > call_taxed_start


def get_charged_minutes(call_start, call_end):

    call_taxed_start = get_taxed_start_time(call_start)
    call_taxed_end = get_taxed_end_time(call_start, call_end)

    if exists_charged_minutes(call_taxed_start, call_taxed_end):
        return math.floor((call_end - call_start).seconds / MINUTE)

    return 0


def get_tariff(call_start, call_end):

    call_start = datetime.fromtimestamp(call_start)
    call_end = datetime.fromtimestamp(call_end)
    charged_minutes = get_charged_minutes(call_start, call_end)

    return BASE_RATE_CALL + (charged_minutes * BASE_RATE_MIN_DAY)


def classify_by_phone_number(records):

    result = []

    for record in records:

        # TODO: new_phone transformar em outra rotina para ficar mais claro
        new_phone = True

        for i in result:
            if i['source'] == record['source']:
                i['total'] = \
                    round(i['total'] + get_tariff(
                        record['start'], record['end']), 2)

                new_phone = False

        if new_phone:
            phone = {}  # TODO: achar uma forma mais enxuta de criar o dict
            phone['source'] = record['source']
            phone['total'] = \
                round(get_tariff(record['start'], record['end']), 2)
            result.append(phone)

    return sorted(result, key=lambda r: r['total'], reverse=True)
