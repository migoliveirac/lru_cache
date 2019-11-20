import lru
import unittest
import string
import random

def getRandomString(stringLength=5):
    """Generates a random string of fixed length """
    chars = string.ascii_lowercase
    return ''.join(random.choice(chars) for i in range(stringLength))

class TestLRU(unittest.TestCase):
	def test_push(self):
		"""
		Summary: Tests method push() from class LRU.

		------------
		Test Case 1:
		Summary: Adds 1 element to the Cache. Capacity is 3 elements.

		Expected: 
		- Head and Tail of the list point to the new node. 
		- Hash Map has 1 element, equal to the newly added node.

		------------
		Test Case 2:
		Summary: Adds 2 different elements to the Cache. Capacity is 3 elements.

		Expected: 
		- Head of the list points to the newest node.
		- Tail of the list points to the oldest node. 
		- Hash Map has 2 elements. Contents of each must match the inserted ones.

		------------
		Test Case 3:
		Summary: Adds 4 different elements to the Cache. Capacity is 3 elements.

		Expected: 
		- Head of the list points to the newest node.
		- Tail of the list points to the oldest node.
		- Hash Map has 3 elements. Contents of each must match the last 3 inserted ones.
		- Linked List must contain 3 elements (newest first).

		------------
		Test Case 4:
		Summary: Adds 4 different elements to the Cache and adds a 5th element whose key
		is the same of the 3rd inserted element. Capacity is 3 elements.

		Expected: 
		- Head of the list points to the newest node.
		- Tail of the list points to the oldest node.
		- Hash Map has 3 elements. Contents of each must match the last 3 inserted ones.
		- Linked List must contain 3 elements (newest first).
		- Repeated element must have simply be moved to the top of the list.

		------------
		Test Case 5:
		Summary: Adds/reads 10000 times to the Cache. 
		Capacity is 5000 elements. Maximum number of accesses is 8000.

		Expected: 
		- Cache contains 2000 elements.
		"""
		aLRU = lru.LRU(3)
		# ------------
		# Test Case 1:
		aLRU.clear()
		aNewData = lru.Data('A', 'A_VAL_1') 
		aLRU.push(aNewData)
		# aLRU.print()

		self.assertEqual(aNewData, aLRU.head.data)
		self.assertEqual(aNewData, aLRU.tail.data)
		self.assertDictEqual(dict({'A': aLRU.head}), aLRU.map)

		# ------------
		# Test Case 2:
		aLRU.clear()
		del aNewData
		aNewData = [lru.Data('A', 'A_VAL_1'), lru.Data('B', 'B_VAL_1')]
		[aLRU.push(aData) for aData in aNewData]
		# aLRU.print()

		self.assertEqual(aNewData[0], aLRU.tail.data)
		self.assertEqual(aNewData[1], aLRU.head.data)
		self.assertDictEqual(dict({'B': aLRU.head, 
								   'A': aLRU.tail}), 
							aLRU.map)

		# ------------
		# Test Case 3:
		aLRU.clear()
		del aNewData
		aNewData = [lru.Data('A', 'A_VAL_1'), 
					lru.Data('B', 'B_VAL_1'), 
					lru.Data('C', 'C_VAL_1'),
					lru.Data('D', 'D_VAL_1')]
		[aLRU.push(aData) for aData in aNewData]
		# aLRU.print()

		self.assertEqual(aNewData[1], aLRU.tail.data)
		self.assertEqual(aNewData[3], aLRU.head.data)
		self.assertDictEqual(dict({'D': aLRU.head, 
								   'C': aLRU.head.next,
								   'B': aLRU.tail}), 
							aLRU.map)

		# ------------
		# Test Case 4:
		aLRU.clear()
		del aNewData
		aNewData = [lru.Data('A', 'A_VAL_1'), 
					lru.Data('B', 'B_VAL_1'), 
					lru.Data('C', 'C_VAL_1'),
					lru.Data('D', 'D_VAL_1'),
					lru.Data('C', 'C_VAL_2')]
		[aLRU.push(aData) for aData in aNewData]
		# aLRU.print()

		self.assertEqual(aNewData[1], aLRU.tail.data)
		self.assertEqual(aNewData[4], aLRU.head.data)
		self.assertDictEqual(dict({'C': aLRU.head, 
								   'D': aLRU.head.next,
								   'B': aLRU.tail}), 
							aLRU.map)

		# ------------
		# Test Case 5:
		aNewData.clear()
		del aLRU
		# Creates LRU Cache with x5000 capacity with maximum nr of accesses x8000
		aLRU = lru.LRU(5000, 8000)

		[aNewData.append(lru.Data(n, getRandomString(5))) for n in range(0, 10000)]
		[aLRU.push(aData) for aData in aNewData]


		self.maxDiff = None
		self.assertEqual(aNewData[8001], aLRU.tail.data)
		self.assertEqual(aNewData[9999], aLRU.head.data)
		self.assertEqual(1999, len(aLRU.map))
		self.assertEqual(1999, aLRU.reads)

		def test_pop(self):
			"""
			Summary: Tests method pop() from class LRU.

			------------
			Test Case 1:
			Summary: Cache has 1 element. Capacity is 3 elements.
			Delete x1 the last element.

			Expected: 
			- Head and Tail of the list are empty. 
			- Hash Map is empty.

			------------
			Test Case 2:
			Summary: Cache has 3 element. Capacity is 3 elements.
			Delete x1 the last element.

			Expected: 
			- Head of the list remains unchanged.
			- Tail of the list is updated to the 2nd element. 
			- Hash Map contains the 2 first inserted elements.

			------------
			Test Case 3:
			Summary: Cache has 3 elements. Capacity is 3 elements.
			Delete x3 the last element.

			Expected: 
			- Head and Tail of the list are empty. 
			- Hash Map are empty.

			------------
			Test Case 4:
			Summary: Cache has 0 elements. Capacity is 3 elements.
			Delete x1 the last element.

			Expected: 
			- Head and Tail of the list remain empty. 
			- Hash Map remains empty.
			"""
			aLRU = lru.LRU(3)
			# ------------
			# Test Case 1:
			aLRU.clear()
			aNewData = lru.Data('A', 'A_VAL_1') 
			aLRU.push(aNewData)
			aLRU.pop()
			# aLRU.print()

			self.assertIsNone(aLRU.head)
			self.assertIsNone(aLRU.tail)
			self.assertIsNone(aLRU.map)

			# ------------
			# Test Case 2:
			aLRU.clear()
			del aNewData
			aNewData = [lru.Data('A', 'A_VAL_1'), 
						lru.Data('B', 'B_VAL_1'), 
						lru.Data('C', 'C_VAL_1')]
			[aLRU.push(aData) for aData in aNewData]
			aLRU.pop()
			# aLRU.print()

			self.assertEqual(aNewData[1], aLRU.tail.data)
			self.assertEqual(aNewData[2], aLRU.head.data)
			self.assertDictEqual(dict({'C': aLRU.head, 
									   'B': aLRU.tail}), 
								aLRU.map)

			# ------------
			# Test Case 3:
			aLRU.clear()
			del aNewData
			aNewData = [lru.Data('A', 'A_VAL_1'), 
						lru.Data('B', 'B_VAL_1'), 
						lru.Data('C', 'C_VAL_1'),
						lru.Data('D', 'C_VAL_1'),
						lru.Data('B', 'B_VAL_2'),
						lru.Data('A', 'A_VAL_2')]
			[aLRU.push(aData) for aData in aNewData]
			[aLRU.pop() for aNode in aLRU.map]
			# aLRU.print()

			self.assertIsNone(aLRU.head)
			self.assertIsNone(aLRU.tail)
			self.assertIsNone(aLRU.map)

			# ------------
			# Test Case 4:
			aLRU.clear()
			del aNewData
			aLRU.pop()
			# aLRU.print()

			self.assertIsNone(aLRU.head)
			self.assertIsNone(aLRU.tail)
			self.assertIsNone(aLRU.map)

if __name__ == '__main__':
	unittest.main()