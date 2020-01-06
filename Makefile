
start_cluster : _start_cluster

postgres : _postgres

stop_cluster : _stop_cluster

create_topic : _create_topic

# Run it like: make create_topic TOPIC=yourtopicname

create_consumer : _create_consumer

# Run it like: make create_consumer TOPIC=yourtopicname MODE=stdout
# OR
# Run it like: make create_consumer TOPIC=yourtopicname MODE=psql

create_producer : _create_producer

# Run it like: make create_producer TOPIC=yourtopicname


_start_cluster:
	( \
	docker-compose up -d ; \
	)

_postgres:
	( \
	 docker exec -it data-challenge-eng_db_1 psql -U postgres ; \
	)

_stop_cluster:
	( \
	 docker-compose stop ; \
	 docker-compose rm -f; \
	)

_create_topic:
	( \
	 python3 ./python_scripts/create_topic.py ${TOPIC} ; \
	)

_create_consumer:
	( \
	 python3 ./python_scripts/consumer.py ${TOPIC} ${MODE} ; \
	)

_create_producer:
	( \
	 python3 ./python_scripts/producer.py ${TOPIC} ; \
	)