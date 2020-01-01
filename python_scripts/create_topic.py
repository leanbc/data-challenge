from kafka.admin import KafkaAdminClient, NewTopic
import sys
import logging
import subprocess
import os


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)



def main():

    topic_name= sys.argv[1]

    try:
        num_partitions= int(sys.argv[2])
    except:
        num_partitions= 1

    try:
        replication_factor= int(sys.argv[3])
    except:
        replication_factor=  1



    # Getting servers using /broker-list.sh

    path_to_function = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    cmd= path_to_function + '/broker-list.sh'

    b=subprocess.run(cmd, capture_output=True)



    bootstrap_servers='localhost' + b.stdout.decode('utf-8')


    logging.info('bootstrap_servers: ' + bootstrap_servers)


    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers, client_id='test')

    topic_list = []

    topic_list.append(NewTopic(name= topic_name , num_partitions=num_partitions, replication_factor=replication_factor))

    admin_client.create_topics(new_topics=topic_list, validate_only=False)

    logging.info('Topic {}, with num_partitions {} and replication_factor {} has been created'.format(topic_name,str(num_partitions),str(replication_factor)))


if __name__ == "__main__":
    main()