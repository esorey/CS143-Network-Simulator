# constants.py
# Contains the constants that other classes and files will use

NO_CNGSTN_CTRL = 0
TCP_RENO = 1
FAST_TCP = 2


# Units conversions
MB_TO_BYTES = float(1000000)        # Multiplier to convert MB to bytes
KB_TO_BYTES = float(1000)           # Multiplier to convert KB to bytes 
BYTES_TO_MBITS = 0.000008   # Multiplier to convert bytes to megabits
SEC_TO_MS = float(1000)             # Convert seconds to milliseconds
MS_TO_SEC = 0.001

DATA_PKT_SIZE = float(1024)     # Bytes per data packet
ACK_PKT_SIZE = float(64)            # Bytes per acknowledgement packet
RTABLE_PKT_SIZE = float(64)	# Bytes per routing table packet

LINK_BUFFER_UNIDIR_CAPACITY = float(50) # The capacity for a link buffer in one direction. Pick a better number plz.

CONSECUTIVE_PKT_DELAY = 0.5     # Send new packets every 0.5 ms when sending consecutive packets
TIMEOUT_TIME = 2               # Default packet timeout time, otherwise use avg RTT 
FAST_PERIOD = 20
BELLMAN_PERIOD = 5000		# Time between each bellman ford event enqueued in ms
DEFAULT_WINDOW_SIZE = 500
global Bellman_not_done
global system_EQ            # the global event queue struct
global system_analytics     # the global analytics class
global debug
global all_flows_done
global testcase
debug = False
testcase = 1
cngstn_ctrl = 1

global bellman_ford
bellman_ford = True
