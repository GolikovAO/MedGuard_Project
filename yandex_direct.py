from tapi_yandex_direct import YandexDirect

ACCESS_TOKEN = "token"
def yandex_getCost ():
    # Обязательные параметры помечены звездочкой.
    api = YandexDirect(
        # *Токен доступа.
        access_token=ACCESS_TOKEN,
        # True включить песочницу.
        # По умолчанию False
        is_sandbox=True,
        # Если вы делаете запросы из под агентского аккаунта,
        # вам нужно указать логин аккаунта для которого будете делать запросы.
        login = "",
        # Повторять запрос, если будут превышениы лимиты
        # на кол-во отчетов или запросов.
        # По умолчанию True.
        retry_if_exceeded_limit=True,
        # Кол-во повторов при возникновении серверных ошибок.
        # По умолчанию 5 раз.
        retries_if_server_error=5,
        # Режим формирования отчета: online, offline или auto.
        # По умолчанию "auto"
        processing_mode='offline',
        # Когда True, будет повторять запрос, пока отчет не будет готов.
        # По умолчанию True
        wait_report=True,
        # Если заголовок указан, денежные значения в отчете возвращаются в валюте
        # с точностью до двух знаков после запятой. Если не указан, денежные
        # значения возвращаются в виде целых чисел — сумм в валюте,
        # умноженных на 1 000 000.
        # По умолчанию False
        return_money_in_micros=False,
        # Не выводить в отчете строку с названием отчета и диапазоном дат.
        # По умолчанию True
        skip_report_header=True,
        # Не выводить в отчете строку с названиями полей.
        # По умолчанию False
        skip_column_header=True,
        # Не выводить в отчете строку с количеством строк статистики.
        # По умолчанию True
        skip_report_summary=True,
    )

    body = {
        "params": {
            "SelectionCriteria": {
                "DateFrom": "2020-11-13",
                "DateTo": "2020-11-13",
            },
            "FieldNames": [
                "Date",
                "CampaignName",
                "Cost"
            ],
            "ReportName": ("Test"),
            "ReportType": "CAMPAIGN_PERFORMANCE_REPORT",
            "DateRangeType": "CUSTOM_DATE",
            "Format": "TSV",
            "IncludeVAT": "NO",
            "IncludeDiscount": "NO"
            }
        }
    result = api.reports().post(data=body)
    #print(result().data)

    # Преобразование.
    result().transform()
    tmp = result().transform()
    return tmp