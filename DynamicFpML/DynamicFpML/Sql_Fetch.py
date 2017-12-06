import cx_Oracle

trade_id=3317457

def MWDBConnect1(trade_id):
    "uname - username, password, host is ln17odcqascan03, port is 1521, DBName is TSTxxMSV"
    con = cx_Oracle.Connect('mwtest_ro/mwtest_ro@ln17odcqaorc001b:1521/TST05MSV')
    cur=con.cursor()
    print "Starting"

    query = ('SELECT DISTINCT ENT_APPLICATION_ID  FROM ENTITY_SIDE_MAJORS where pR_CLEARING_TRADE_ID=\'{trade_id}\' AND CONTRACT_STATE =\'New-Clearing\' and Legal_entity =\'BATTSTBKLEA1\'').format(trade_id=trade_id)
    cur1 = cur.execute(query)
    #connection = OracleConnection('ln17odcqascan03:1521','TST05MSV,''mwtest_ro','mwtest_ro')
    #cur1 = connection.execute_query(query)
    print cur1
    for result in cur1:
        print "hello"
        print "results" + result
        print "results" + cur1
    return

    cur.close()
    con.close()
