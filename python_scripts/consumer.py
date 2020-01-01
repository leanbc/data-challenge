from kafka import KafkaConsumer
from json import loads
import logging
import sys
import os
from datetime import datetime
import psycopg2

try:
    topic=sys.argv[1]
    mode=sys.argv[2]
except IndexError:
    logging.error('-------------------------------------')
    logging.error('You need to specify an existing topic and the mode of execution as an argument at runtime.')
    logging.error('Something like :')
    logging.error('python3 consumer.py topicname stdout/psql')
    logging.error('-------------------------------------')
    raise



setting_absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

path_to_log_folder= setting_absolute_path + '/logs/' + topic


#check if directory exist


if os.path.exists(path_to_log_folder):
    filelist = [ f for f in os.listdir(path_to_log_folder)]
    for f in filelist:
        os.remove(os.path.join(path_to_log_folder, f))
else:
    os.mkdir(path_to_log_folder)



logging.basicConfig(filename= path_to_log_folder + '/'  +  datetime.now().strftime('%Y%m%d_%H%M%S') +'.log', filemode='w', level=logging.INFO)






def create_table(topic=topic):

    conn=psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='example', port=4444)

    cursor=conn.cursor()

    stmt="""
    DROP TABLE IF EXISTS {0};
    CREATE TABLE {0} (
    uid text,
    message text,
    ts text)
    """.format(topic)

    cursor.execute(stmt)
    conn.commit()

    conn.close()

def insert_value(table_name, val1 ,val2, val3):

    conn=psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='example', port=4444)

    cursor=conn.cursor()

    stmt="INSERT INTO {} (uid, message, ts) VALUES ('{}', '{}', '{}');".format(table_name,val1,val2,val3)

    cursor.execute(stmt)
    conn.commit()

    conn.close()


def main():

    consumer = KafkaConsumer(
        topic,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['localhost:9092'])

    create_table(topic=topic)

    i = 0

    if mode=='psql':

        for m in consumer:

            i+=1
            message=str(m.value).replace("'", "''")
            insert_value(topic,
                         val1= str(m.value['uid']),
                         val2=message ,
                         val3=datetime.utcfromtimestamp(int(m.value['ts'])).strftime('%Y-%m-%d %H:%M:%S'))

    elif mode=='stdout':

        for m in consumer:
            i+=1
            print(m.value)
            print(datetime.utcfromtimestamp(int(m.value['ts'])).strftime('%Y-%m-%d %H:%M:%S'))
            logging.info('{}'.format(str(i)))




if __name__ == "__main__":
    main()