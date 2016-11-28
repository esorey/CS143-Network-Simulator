# constants.py
# Contains the constants that other classes and files will use

# Units conversions
MB_TO_BYTES = float(1000000)		# Multiplier to convert MB to bytes
KB_TO_BYTES = float(1000)			# Multiplier to convert KB to bytes 
BYTES_TO_MBITS = 0.000008 	# Multiplier to convert bytes to megabits
SEC_TO_MS = float(1000) 			# Convert seconds to milliseconds

DATA_PKT_SIZE = float(1024)		# Bytes per data packet
ACK_PKT_SIZE = float(64)			# Bytes per acknowledgement packet

LINK_BUFFER_UNIDIR_CAPACITY = float(50) # The capacity for a link buffer in one direction. Pick a better number plz.

CONSECUTIVE_PKT_DELAY = 0.5 	# Send new packets every 0.5 ms when sending consecutive packets
global system_EQ 			# the global event queue struct
global system_analytics		# the global analytics class


global debug 
debug = False
