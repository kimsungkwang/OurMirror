from time import sleep
import datetime 


def set_time(self,MainWindow):

    while True:
        now=datetime.datetime.now() #현재 시각을 시스템에서 가져옴

        hour = format(int(now.hour), '02')
        minute = format(int(now.minute), '02')

        self.date.setText("%s. %s. %s"%(now.year,now.month,now.day))
        self.time.setText("%s:%s" %(hour,minute))

        sleep(1)