import pika

# create pika connection
# BlockingConnection is a synchronous adapter
# "rabbitmq" is referencing the rabbitmq host on minikube
# this line is basicaly limiting connection to rabbitmq cluster
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))

# create a channel with the connection
channel = connection.channel()
