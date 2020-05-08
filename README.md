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

### Consumers
Python
Redis 5.0

## Installation

> Requirement: docker desktop

````shell script
docker-compose up .
````

