class Data:
	"""
	Summary: Represents a Node in the Doubly Linked List used in the LRU object.

	Description: Each node contains a pointer to the previous and the next node of the list.
	The pointers of the previous node of the head of the list as well the next node of the
	tail of the list shall be NULL.  
	"""
	def __init__(self, key=None, value=None):
		"""
		Summary: Initiliazes an instance of class Data.

		Description: If no parameters are provided, key and value are initialized to NULL.

		Arguments:
		key -- Must be unique for each Data object within the list of Nodes.
		value -- Value of the Data object.
		"""
		self.key   = key
		self.value = value

	def to_string(self):
		"""
		Summary: Returns a string with the key & value of a Data object.
		"""
		return '[{0}, {1}]'.format(self.key, self.value)

class Node:
	"""
	Summary: Represents a Node in the Doubly Linked List used in the LRU object.

	Description: Each node contains a pointer to the previous and the next node of the list.
	The pointers of the previous node of the head of the list as well the next node of the
	tail of the list shall be NULL.  
	"""
	def __init__(self, data=Data(), prev=None, next=None):
		"""
		Summary: Initiliazes an instance of class Node.

		Description: If no parameters are provided, data, prev and next are 
		initialized to NULL.

		Arguments:
		data -- Data object associated with the Node.
		prev -- Pointer to the previous Node of the List.
		next -- Pointer to the next Node of the List.
		"""
		self.prev   = prev # Link to previous Node 
		self.next   = next # Link to next Node
		self.data   = data # Data object of the Node

# Represents a LRU Cache
class LRU:
	"""
	Summary: Represents a Least Recent Used algorithm for Cache Memory management.

	Description: Algorithm is implemented using a Doubly Linked List, whilst each
	node contains a pointer to the previous and next nodes, as well as a Data object.
	A Hash Map is used to store the pointers for each node of the list and be able to 
	access them in O(1).
	"""
	def __init__(self, size, max_reads=-1):
		"""
		Summary: Initializes a LRU class object.

		Arguments:
		size -- Maximum number of items of the Cache
		head -- Pointer to the Head of the Doubly Linked List.
		tail -- Pointer to the tail of the Doubly Linked List.
		map -- Hash Map containing pointers to all elements of the List.
		max_reads -- Indicates how many times the cache may be read before resset.
					 By default equal to -1 (no limit)
		"""
		self.size      = size
		self.head      = Node()
		self.tail      = Node()
		self.map       = {}
		self.max_reads = max_reads
		self.reads     = 0

	def push(self, data):
		""" 
		Summary: Moves a Node to the top of the list.
		
		Description: If node exists in the list, it is moved to the top,
		otherwise, if not existing, it adds it to the list. 
		If the list is full after the insertion, the last node of the list is removed.

		Arguments:
		data -- (key, value): expects a key and value to be inserted
		
		Returns:
			True if head of the list was correctly updated, otherwise returns False.
		
		Example:
		self.push(('key_1','value_1'))
		"""
		if ((self.max_reads == -1) 
			or ((self.max_reads != -1) and (self.reads < self.max_reads))):
			if (self.size != 0):
				self.reads += 1
				if (data.key in self.map):
					if (self.map[data.key].data.value != data.value):
							self.map[data.key].data = data
					# if existing node is the tail
					if (self.map[data.key] == self.tail):
						self.tail = self.map[data.key].prev
						self.tail.next = None
						self.head.prev = self.map[data.key]
						self.map[data.key].next = self.head
						self.head = self.map[data.key]
					# if existing node is not the head
					elif (not (self.map[data.key] == self.head)):
						self.map[data.key].prev.next = self.map[data.key].next
						self.map[data.key].next.prev = self.map[data.key].prev
						self.head.prev = self.map[data.key]
						self.map[data.key].next = self.head
						self.head = self.map[data.key]
				# if node does not exist in list ...
				else:
					aNewNode = Node(data)
					# if list is not full ...
					if (len(self.map) < self.size):
						if (len(self.map) == 0):
							self.tail     = aNewNode
						else:
							aNewNode.next  = self.head
							self.head.prev = aNewNode
						self.head      = aNewNode
						self.map[data.key] = aNewNode
					# if list is full ...
					elif (len(self.map) >= self.size):
						aNewNode.next  = self.head
						self.head.prev = aNewNode
						self.head = aNewNode
						self.map[data.key] = aNewNode
						self.pop()
				return (self.head == self.map[data.key])
			else:
				print("Could not add element. Cache size is 0 !")
		elif ((self.max_reads != -1) and (self.reads >= self.max_reads)):
			self.clear()
			print ("""Maximum number of Cache accessess achieved ({} times).
Clearing Cache ...""".format(self.max_reads))
			return False

	def pop(self):
		""" 
		Summary: Deletes last element of the list.

		Arguments:
		data -- (key, value): expects a key and value to be inserted
		
		Returns:
			True if last element of the list was correctly deleted,
			otherwise, returns False.
		
		Example:
		self.pop()
		"""
		try:
			del self.map[self.tail.data.key]
		except KeyError:
			print("Tail Key {0} not found !".format(self.tail.data.key))
			return False
		if (len(self.map) == 1):
			self.head = None
			self.tail = None
		elif (len(self.map) >= 2):
			self.tail      = self.tail.prev
			self.tail.next = None
		return True

	def clear (self):
		self.map.clear()
		self.head  = None
		self.tail  = None
		self.reads = 0

	def print(self):
		"""
		Summary: Print method for the Doubly Linked List. 
		Prints the Data of each node starting from the head.
		"""
		aNode = self.head
		while (aNode != None):
			print(aNode.data.to_string(), end = ' ')
			aNode = aNode.next
		print('')
		return

if __name__ == '__main__':
	aLRU = LRU(3)
	aLRU.push(Data('A', 'A_VAL_1'))
	aLRU.push(Data('B', 'B_VAL_1'))
	aLRU.push(Data('C', 'C_VAL_1'))
	aLRU.push(Data('D', 'D_VAL_1'))
	aLRU.push(Data('B', 'B_VAL_2'))
	aLRU.push(Data('C', 'C_VAL_2'))
	aLRU.print()