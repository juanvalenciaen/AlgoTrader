import darwinex_ticks

dwt = darwinex_ticks.DarwinexTicksConnection(dwt_ftp_user=' '
                        dwt_ftp_pass=''
                        dwt_ftp_hostname=''
                        dwt_ftp_port='')

data = dwt.ticks_from_darwinex('EURUSD',start='2018-08-02 08',
                                end='2018-08-03 08')

print(data)

#to get info:
#https://www.youtube.com/watch?v=qmsqNSF9q_U&ab_channel=TradingZorro