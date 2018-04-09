# Sky Hoffert
# April 9, 2018
# probe.py
# Node for a probe using rmq/pika

import pika
import sys
import pickle

connection = pika.BlockingConnection( pika.ConnectionParameters( host='localhost' ) )
channel = connection.channel()

print('[ PROBE ] Waiting for logs. To exit press CTRL+C')
sys.stdout.flush()

def consume_cmd(ch, method, properties, body):
    message = pickle.loads( body )
    print("[ PROBE ] %r" % message)
    sys.stdout.flush()

channel.basic_consume( consume_cmd, queue='cmd' , no_ack=True )

channel.start_consuming()