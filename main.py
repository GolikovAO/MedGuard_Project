import pyodbc
import datetime
from datetime import timedelta
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yandex_direct

def prod():

    '''Авторизация mssql'''

    connection_sql = pyodbc.connect('''Driver={ODBC Driver 17 for SQL Server};
                      Server="server";
                      Database=Test;
                      Trusted_Connection=yes;''')

    cursor = connection_sql.cursor()
    cursor.execute('SELECT COUNT(*) FROM CallTouch')
    #cursor.execute('SELECT COUNT(*) FROM CallTouchTest') #Черновик
    row_count_table = cursor.fetchall()[0][0]

    '''Автообновление даты'''
    # DateTo = datetime.datetime.now()
    # DateFrom = DateTo
    # DateFrom = DateFrom.strftime("%d/%m/%Y")
    # DateTo = DateTo.strftime("%d/%m/%Y")
    # print(DateFrom, DateTo, sep = "\n")

    '''Авторизация calltouch'''
    call_touch_id = "id"
    call_touch_counter = 'counter'
    call_touch_server = 'https://api-node16.calltouch.ru'
    call_touch_token = 'token'
    DateTo = '09/10/2020'
    DateFrom = '09/10/2020'

    payload = {'clientApiId': call_touch_token, 'dateFrom': DateFrom,
           'dateTo': DateTo, 'withCallTags': 'true', 'withMapVisits': 'true'}
    request_url = (call_touch_server + '/calls-service/RestAPI/11425/calls-diary/calls?')
    request = requests.get(request_url, params=payload)
    parsing_request = json.loads(request.text)

    print(parsing_request == request.json(), end='\n')
    print(type(parsing_request), end='\n')
    for row in parsing_request:
        Tag = "none"
        tempDateTime = row['date'].split(' ')
        if row['callTags']:
            Tag = str(row['callTags'][0]['names'])
            Tag = Tag[2:len(Tag)-2]
        if str(row['uniqueCall']) == 'True':
            repeat_status = 1
        else:
            repeat_status = 0
        cursor.execute('''
                          INSERT INTO CallTouch (Call_ID, DateCall, TimeCall, CallerNumber, URL,
                          RepeatStatus, SearchQuery, AdsPlatform, AdID, CampaignID, City, CallTag)
                          VALUES
                          (? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                          ''', (row['callId'], tempDateTime[0], tempDateTime[1], row['callerNumber'], row['url'],
                             repeat_status, row['keyword'], row['source'], row['utmContent'], row['utmCampaign'], row['city'], Tag))
        # cursor.execute('''
        #                       INSERT INTO CallTouchTest (Call_ID, DateCall, TimeCall, CallerNumber, URL,
        #                       RepeatStatus, SearchQuery, AdsPlatform, AdID, CampaignID, City, CallTag)
        #                       VALUES
        #                       (? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        #                       ''', (row['callId'], tempDateTime[0], tempDateTime[1], row['callerNumber'], row['url'],
        #                             repeat_status, row['keyword'], row['source'], row['utmContent'], row['utmCampaign'],
        #                             row['city'], Tag))
        connection_sql.commit()

    cursor.execute('SELECT * FROM CallTouch where DateCall = ?', DateFrom)  # DateCall = DateTo поменять на проде
    #cursor.execute('SELECT * FROM CallTouchTest where DateCall = ?', DateFrom)  # Черновик
    result = cursor.fetchall()

    '''Авторизация google sheet'''
    #google_sheet_token = 'token.json' #Черновик
    google_sheet_token = 'token.json'
    auth_sheet = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
    connection_sheet = ServiceAccountCredentials.from_json_keyfile_name(google_sheet_token, auth_sheet)
    client = gspread.authorize(connection_sheet)
    #result_sheet = client.open('TestMedgard') # Черновик
    result_sheet = client.open('Ads_Statistic')

    final_list = []
    for row in result:
        interim_list = []
        for item in row:
            interim_list.append(str(item))
        final_list.append(interim_list)
    print(final_list)

    row_id = 'Ads_Statistic!A' + str(row_count_table + 2)
    result_sheet.values_update(
        row_id,
        params={'valueInputOption': 'USER_ENTERED'},
        body={'values': final_list}
    )

def Test():
    '''Авторизация mssql'''

    connection_sql = pyodbc.connect('''Driver={ODBC Driver 17 for SQL Server};
                          Server=server;
                          Database=Test;
                          Trusted_Connection=yes;''')

    cursor = connection_sql.cursor()
    cursor.execute('TRUNCATE TABLE CallTouchTest') #Очистка
    cursor.execute('SELECT COUNT(*) FROM CallTouchTest') #Черновик
    row_count_table = cursor.fetchall()[0][0]

    '''Автообновление даты'''
    # DateTo = datetime.datetime.now()
    # DateFrom = DateTo
    # DateFrom = DateFrom.strftime("%d/%m/%Y")
    # DateTo = DateTo.strftime("%d/%m/%Y")
    # print(DateFrom, DateTo, sep = "\n")

    '''Авторизация calltouch'''
    call_touch_id = 
    call_touch_counter = ''
    call_touch_server = 'https://api-node16.calltouch.ru'
    call_touch_token = ''
    DateTo = '13/11/2020'
    DateFrom = '13/11/2020'

    payload = {'clientApiId': call_touch_token, 'dateFrom': DateFrom,
               'dateTo': DateTo, 'withCallTags': 'true', 'withMapVisits': 'true'}
    request_url = (call_touch_server + '/calls-service/RestAPI/11425/calls-diary/calls?')
    request = requests.get(request_url, params=payload)
    parsing_request = json.loads(request.text)

    print(parsing_request == request.json(), end='\n')
    print(type(parsing_request), end='\n')
    for row in parsing_request:
        Tag = "None"
        Campaign = str(row['utmCampaign']).split('_')
        Group = str(row['utmContent']).split('_')
        AdKeyword = str(row['utmTerm']).split('_')

        if len(AdKeyword) == 1:
            AdKeyword.append('None')
            AdKeyword[1] = AdKeyword[0]
            AdKeyword[0] = 'None'
        if len(AdKeyword) > 2:
            for i in range(1, len(AdKeyword) - 1):
               AdKeyword[0] = AdKeyword[0] + AdKeyword[i]
            AdKeyword[1] = AdKeyword[len(AdKeyword) - 1]

        if len(Group) == 1: 
            Group.append(('None'))
        if len(Group) > 2:
            for i in range(1, len(Group) - 1):
                Group[0] = Group[0] + Group[i]
            Group[1] = Group[len(Group)-1]

        if (len(Campaign)) == 1:
            Campaign.append('None')

        tempDateTime = row['date'].split(' ')
        if row['callTags']:
            Tag = str(row['callTags'][0]['names'])
            Tag = Tag[2:len(Tag) - 2]
        if str(row['uniqueCall']) == 'True':
            repeat_status = 1
        else:
            repeat_status = 0
        cursor.execute('''
                              INSERT INTO CallTouchTest (Call_ID, DateCall, TimeCall, CallerNumber, URL,
                              RepeatStatus, AdsPlatform, CampaignID, CampaignName, GroupID, GroupName, 
                              AdID, SearchQuery, City, CallTag)
                              VALUES
                              (? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                              ''', (row['callId'], tempDateTime[0], tempDateTime[1], row['callerNumber'], row['url'],
                                    repeat_status, row['source'], Campaign[1], Campaign[0], Group[1], Group[0],
                                    AdKeyword[0], AdKeyword[1], row['city'], Tag))
        connection_sql.commit()

    cursor.execute('SELECT * FROM CallTouchTest where DateCall = ?', DateFrom)  # Черновик
    result = cursor.fetchall()

    '''Авторизация google sheet'''
    google_sheet_token = 'token.json' #Черновик
    auth_sheet = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
    connection_sheet = ServiceAccountCredentials.from_json_keyfile_name(google_sheet_token, auth_sheet)
    client = gspread.authorize(connection_sheet)
    result_sheet = client.open('TestMedgard') # Черновик

    final_list = []
    for row in result:
        interim_list = []
        for item in row:
            interim_list.append(str(item))
        final_list.append(interim_list)
    print(final_list)

    row_id = 'Ads_Statistic!A' + str(row_count_table + 2)
    result_sheet.values_update(
        row_id,
        params={'valueInputOption': 'USER_ENTERED'},
        body={'values': final_list}
    )

def TestYandexDirect():
    connection_sql = pyodbc.connect('''Driver={ODBC Driver 17 for SQL Server};
                              Server=server;
                              Database=Test;
                              Trusted_Connection=yes;''')

    cursor = connection_sql.cursor()

    yandexReport = yandex_direct.yandex_getCost()

    for row in yandexReport:
        cursor.execute('''
                                          INSERT INTO CampaignDailyCost (DateOfGet, Platform, CampaignName, Cost)
                                          VALUES
                                          (? ,?, ?, ?)
                                          ''',
                       (row[0], "Yandex.Direct", row[1], row[2]))
        connection_sql.commit()


#Test()
TestYandexDirect()

'''
Интеграция calltouch api + direct api + google sheet api + google ads api + mssql
1. Вытянуть данные с яндекс - 2 дня / 4 дня
2. Вытянуть данные с google - 2 дня / 4 дня
3. Вытянуть сделки (заявки с сайта) - 3 дня / 6 дней
4. Добавить триггеры в БД - 2 дня / 4 дня
5. Обернуть в try / except  - 1 день / 2 дня
6. Сформировать .exe - 2 часа / 4 часа
7. Сформировать .bat - 1 день / 2 дня
'''