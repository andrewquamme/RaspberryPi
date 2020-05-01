from sense_hat import SenseHat
from datetime import datetime
from csv import writer

sense = SenseHat()


def c_to_f(temp):
    return (temp*9/5)+32
    
def get_data():
    sense_data = []
    dt = datetime.now()
    sense_data.append(datetime.now())
    sense_data.append(c_to_f(sense.get_temperature()))
    sense_data.append(sense.get_pressure())
    sense_data.append(sense.get_humidity())

    return sense_data

with open('data.csv', 'w', newline='') as f:
    data_writer = writer(f)
    data_writer.writerow(['date', 'temp', 'pressure', 'humidity'])
    t1 = datetime.now()
    
    while True:
        data = get_data()
        delay = data[0] - t1
        if delay.seconds > 10:
            data_writer.writerow(data)
            t1 = datetime.now()
