# Django + Pubsub

> Should not be used in production.

Demo to show how to use Django signals to trigger pubsub events.  
Those events will be consumed be a service and store the information in Redis

## Stack

Python 3.7

### Django  - Administration panel and publisher
Django 3.0.6
MySQL 8.0

### Pubsub
Localstack (SQS, SNS)

### Consumer
Python
Redis 5.0

## Installation

> Requirement: docker desktop

Build all the container image for each services included in the demo.

````shell script
docker-compose build 
````

### Start application

Django is the publisher. The service (see docker-compose.yml) depends on pubsub, pubsub-streaming, and 
product-service-consumer.

- **pubsub**: API that abstract SNS/SQS  
- **pubsub-streaming**: will consume the internal queue of the pubsub to send back messages to SNS
- **product-service-consumer**: consumer. This service will pull message from the queue and store the information in 
Redis


#### Start Django

````shell script
docker-compose up django 
````

There is a `db.sqlite3` included with the project. You can set your own database connexion if you want.
The administration panel of Django is available at http://localhost:8000/admin/.

The username/password are: admin/password

## Components

### Django

The application will start automatically at with the `docker-compose up django`.

## Pubsub

The application will start automatically at with the `docker-compose up pubsub`.  
The consumer (`demo-pubsub-streaming`) will also be available.

## Consumer

The application will start automatically at with the `docker-compose up django`.  
Since the objective is to see the updates from Django to Redis, it is possible to check any action.

Connect to the Redis container and start the monitor:
````shell script
docker exec -it demo-redis bash   
root@....:/data# redis-cli  
127.0.0.1:6379> monitor
````

## Flow

The objective if to send messages to the pubsub from the source of truth (Django). Those messages will be process 
(Pubsub) and be process by the consumer (product-service-consumer).

> Publisher  ->    Pubsub   ->    Consumer

 
### Notes

As for now, only the brands events are published. See services/django/products/models.py


