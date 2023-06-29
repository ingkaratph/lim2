servers = {
    'server1': {
        'server': '172.23.10.51',
        'database': 'SAR',
        'username': 'sa',
        'password': 'Automatic',
        'driver': '{ODBC Driver 17 for SQL Server}'
    },
    'server2': {
        'server': '192.168.1.100',
        'database': 'DB2',
        'username': 'admin',
        'password': '123456',
        'driver': '{ODBC Driver 17 for SQL Server}'
    }
}


column_ = {
    'query1' : "[ReqNo],[JobType],[Branch],[RequestSection],[ReqDate],[CustFull],[CustShort],[Code],[SampleCode],[SampleStatus],[SampleType],[ProcessReportName],[SamplingDate],[InstrumentName],[ItemName],[ItemStatus],[AnalysisDueDate],[RemarkNo]",
    'query2' : "[RemarkNo],[CustShort],[SamplingDate],[ReceiveDate],[DueDate],[SampleType],[ProcessReportName],[SampleRemark]"
}