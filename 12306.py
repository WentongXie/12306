import requests, datetime, logging, time, traceback, random
from Push import PushMessage

user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"

def CoocieUrl(from_station, to_station, date):
    cookie_base_url = "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={}&ts={}&date={}&flag=N,N,Y"
    station = Station()
    return cookie_base_url.format(from_station + "," + station.getStationCodebyStationName(from_station), to_station + "," + station.getStationCodebyStationName(to_station), date)

def QueryUrl(from_station, to_station, date):
    base_url = "https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT"
    station = Station()
    return base_url.format(date, station.getStationCodebyStationName(from_station), station.getStationCodebyStationName(to_station))

class Station:
    __STATION_URL = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"
    __station_dict = {}
    __last_update = None
    def __init__(self):
        self.__update()

    def __update(self):
        if Station.__last_update == None or (datetime.datetime.now() - Station.__last_update).days > 7:
            logging.info("update station")
            logging.info(Station.__last_update)
            Station.__last_update = datetime.datetime.now()
            rsp = requests.get(Station.__STATION_URL)
            station_list = rsp.text.split("'")[1].split("@")
            for i in station_list:
                if len(i) != 0:
                    data = i.split("|")
                    Station.__station_dict[data[1]] = data[2]
                    Station.__station_dict[data[2]] = data[1]
        logging.debug(Station.__station_dict)

    def getStationCodebyStationName(self, name):
        self.__update()
        return Station.__station_dict[name]

    def getStationNamebyStationCode(self, name):
        self.__update()
        return Station.__station_dict[name]

class Train():
    def __init__(self):
        pass

    def __init__(self, train):
        logging.debug(train)
        l = train.split("|")
        self.__train_id = l[2]                  #??????id
        self.__name = l[3]                      #?????????
        self.__from = l[4]                      #?????????
        self.__to = l[5]                        #?????????
        self.__in = l[6]                        #??????
        self.__out = l[7]                       #??????
        self.__start = l[8]                     #????????????
        self.__arrive = l[9]                    #????????????
        self.__spend = l[10]                    #??????
        self.__superior_soft_sleep = l[21]      #????????????
        self.__soft_sleep = l[23]               #??????/?????????
        self.__no_seat = l[26]                  #??????
        self.__hard_sleep = l[28]               #??????/?????????
        self.__hard_seat = l[29]                #??????
        self.__second_class_seat = l[30]        #?????????/????????????
        self.__first_class_seat = l[31]         #?????????
        self.__business_seat = l[32]            #?????????/?????????

    def getTrainId(self):
        return self.__train_id
    def setTrain_id(self, train_id):
        self.__train_id = train_id

    def getName(self):
        return self.__name
    def setName(self, name):
        self.__name = name

    def getFromStation(self):
        return self.__from
    def setFromStation(self, from_station):
        self.__from = from_station

    def getToStation(self):
        return self.__to
    def setToStation(self, to_station):
        self.__to = to_station

    def getInStation(self):
        return self.__in
    def setInStation(self, in_station):
        self.__in = in_station

    def getOutStation(self):
        return self.__out
    def setOutStation(self, out_station):
        self.__out = out_station

    def getStartTime(self):
        return self.__start
    def setStart(self, start_time):
        self.__start = start_time

    def getArriveTime(self):
        return self.__arrive
    def setArriveTime(self, arrive_time):
        self.__arrive = arrive_time

    def getSpendTime(self):
        return self.__spend
    def setSpendTime(self, spend_time):
        self.__spend = spend_time

    def getSuperiorSoftSleep(self):
        return self.__superior_soft_sleep
    def setSuperiorSoftSleep(self, superior_soft_sleep):
        self.__superior_soft_sleep = superior_soft_sleep

    def getSoftSleep(self):
        return self.__soft_sleep
    def setSoftSleep(self, soft_sleep):
        self.__soft_sleep = soft_sleep

    def getNoSeat(self):
        return self.__no_seat
    def setNoSeat(self, no_seat):
        self.__no_seat = no_seat

    def getHardSleep(self):
        return self.__hard_sleep
    def setHardSleep(self, hard_sleep):
        self.__hard_sleep = hard_sleep

    def getHardSeat(self):
        return self.__hard_seat
    def setHardSeat(self, hard_seat):
        self.__hard_seat = hard_seat

    def getSecondClassSeat(self):
        return self.__second_class_seat
    def setSecondClassSeat(self, second_class_seat):
        self.__second_class_seat = second_class_seat

    def getFirstClassSeat(self):
        return self.__first_class_seat
    def setFirstClassSeat(self, first_class_seat):
        self.__first_class_seat = first_class_seat

    def getBusinessSeat(self):
        return self.__business_seat
    def setBusinessSeat(self, business_seat):
        self.__business_seat = business_seat

def CheckTicket(train):
    return ((train.getSecondClassSeat() != "???" and train.getSecondClassSeat() != "") or
        (train.getFirstClassSeat() != "???" and train.getFirstClassSeat() != "") or
        (train.getBusinessSeat() != "???" and train.getBusinessSeat() != ""))

def FormatTrain(train):
    station = Station()
    ret = "??????id: " + train.getTrainId() + "\n"
    ret += "?????????: " + train.getName() + "\n"
    ret += "?????????: " + station.getStationNamebyStationCode(train.getFromStation()) + "\n"
    ret += "?????????: " + station.getStationNamebyStationCode(train.getToStation()) + "\n"
    ret += "??????: " + station.getStationNamebyStationCode(train.getInStation()) + "\n"
    ret += "??????: " + station.getStationNamebyStationCode(train.getOutStation()) + "\n"
    ret += "????????????: " + train.getStartTime() + "\n"
    ret += "????????????: " + train.getArriveTime() + "\n"
    ret += "??????: " + train.getSpendTime() + "\n"
    ret += "????????????: " + train.getSuperiorSoftSleep() + "\n"
    ret += "??????/?????????: " + train.getSoftSleep() + "\n"
    ret += "??????: " + train.getNoSeat() + "\n"
    ret += "??????/?????????: " + train.getHardSleep() + "\n"
    ret += "??????: " + train.getHardSeat() + "\n"
    ret += "?????????/????????????: " + train.getSecondClassSeat() + "\n"
    ret += "?????????: " + train.getFirstClassSeat() + "\n"
    ret += "?????????/?????????: " + train.getBusinessSeat() + "\n"
    return ret

def QueryTrain(from_station, to_station, date):
    cookie_url = CoocieUrl(from_station, to_station, date)
    query_url = QueryUrl(from_station, to_station, date)
    logging.info("cookie_url: %s, query_url: %s.", cookie_url, query_url)
    with requests.Session() as s:
        rsp = s.get(cookie_url, headers = {"User-Agent": user_agent})
        logging.info(rsp.headers)
        logging.debug(s.cookies)
        rsp = s.get(query_url, headers = {"User-Agent": user_agent})
        logging.debug(rsp.text)
        d = rsp.json()
    logging.debug(d)
    ret = []
    for i in d["data"]["result"]:
        ret.append(Train(i))
    return ret

def Query(list):
    push = ""
    for i in list:
        train = QueryTrain(i["from_station"], i["to_station"], i["date"])
        push += "*" * 30 + "\n"
        push += "from: {}, to:{}, date: {}.\n".format(i["from_station"], i["to_station"], i["date"])
        for i in train:
            if CheckTicket(i):
                push += FormatTrain(i) + "\n"
        push += "*" * 30 + "\n"
    return push

def main():
    name = "12306.txt"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename = name, level = logging.INFO, format = LOG_FORMAT)
    l = [
        {
            "from_station": "??????",
            "to_station": "??????",
            "date": "2022-01-29"
        },
        {
            "from_station": "??????",
            "to_station": "??????",
            "date": "2022-01-30"
        }
    ]
    while True:
        time.sleep(random.randint(0, 60))
        try:
            push = Query(l)
            if push == "":
                PushMessage("???????????????", push)
        except Exception as e:
            logging.error("Exception: %s", traceback.format_exc())
        time.sleep(600)

if __name__ == "__main__":
    main()
