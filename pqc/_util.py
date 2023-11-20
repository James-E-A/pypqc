def using_avx2():
	return False  # TODO

def partition_list(predicate, it):
	l_true = []
	l_false = []
	for item in it:
		if predicate(item):
			l_true.append(item)
		else:
			l_false.append(item)
	return l_true, l_false
