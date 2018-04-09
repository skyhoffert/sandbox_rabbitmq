# Sky Hoffert
# April 9, 2018
# gs.py
# Node for a ground station using rmq/pika

import pika
import sys
import pickle

def send_message( channel, exch, queue, msg ):
    channel.basic_publish( exchange=exch, routing_key=queue, body=msg )
    
    # LOG
    print('[ GS ] Sent message: {}'.format( msg ) )
    sys.stdout.flush()

def main():
    connection = pika.BlockingConnection( pika.ConnectionParameters( host='localhost' ) )
    channel = connection.channel()

    # set up the exchange
    channel.exchange_declare( exchange='msl', exchange_type='direct' )

    # set up the command queue (cmd)
    # GS -> PROBE
    channel.queue_declare( queue='cmd' )
    channel.queue_bind( exchange='msl', queue='cmd' )
    
    # set up the telemetry queue (tlm)
    # PROBE -> GS
    channel.queue_declare( queue='tlm' )
    channel.queue_bind( exchange='msl', queue='tlm' )
    
    # set up the log queue (log)
    # PROBE -> GS
    channel.queue_declare( queue='log' )
    channel.queue_bind( exchange='msl', queue='log' )

    # send a message!
    packet = { 'id': 0, 'commmand': 'stop', 'params': {'val': 0} }
    message = pickle.dumps( packet )
    send_message( channel=channel, exch='msl', queue='cmd', msg=message )

    # close the connection
    connection.close()

if __name__ == '__main__':
    main()
    sys.exit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    