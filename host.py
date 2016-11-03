from link import linkqueue()
import flow
class Host:
	"""A Host: end points of the network"""
	def __init__(self, id, link):
		super(Host, self).__init__()
		self.arg = arg
		self.link = link
		linkqueue = linkqueue()

	'''Add the passed packets to the link queue of the 
	link it is connected to'''
	def sendPackets(packets, destination):
		linkqueue.sendPackets(packets)

	'''Receive the packets from the link queue'''
	def receivePackets():
		packet = linkqueue.get()
		if packet.ID == "ACK":
			# inform that acknowledgmetn received
			flow.push("ack received")
		else: # Data packet
			flow.push("ack")
