def flip_link_id(id):
	'''
	Flip the link ID given
	'''
    res = None
    if id[-1] == 'a':
        res = id[:-1] + 'b'
    elif id[-1] == 'b':
        res = id[:-1] + 'a'
    else:
        raise ValueError("Invalid link id pass to flip_link_id: %s" % id)
    return res
