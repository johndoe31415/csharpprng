#	csharpprng - Reimplementation of C# System.Random PRNG in Python.
#	Copyright (C) 2017-2017 Johannes Bauer
#
#	This file is part of csharpprng.
#
#	csharpprng is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	csharpprng is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with csharpprng; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

class CSharpPRNG(object):
	"""C# PRNG reimplemented in Python. Reference:
	http://referencesource.microsoft.com/#mscorlib/system/random.cs"""

	_MSEED = 161803398
	_MBIG = (2 ** 31) - 1

	@staticmethod
	def _i32(value):
		value = value & 0xffffffff
		if value >= 0x80000000:
			return -(0xffffffff - value) - 1
		else:
			return value

	def __init__(self, seed):
		assert(isinstance(seed, int))
		assert(-(2 ** 31) <= seed < (2 ** 31))

		self._seed_array = [ 0 ] * 56
		if seed == -(2 ** 31):
			seed = (2 ** 31) - 1
		else:
			seed = abs(seed)
		mj = self._MSEED - seed
		self._seed_array[55] = mj
		mk = 1
		for i in range(1, 55):
			ii = (21 * i) % 55
			self._seed_array[ii] = mk
			mk = mj - mk
			if mk < 0:
				mk += self._MBIG
			mj = self._seed_array[ii]

		for k in range(1, 5):
			for i in range(1, 56):
				self._seed_array[i] = self._i32(self._seed_array[i] - self._seed_array[1 + (i + 30) % 55])
				if self._seed_array[i] < 0:
					self._seed_array[i] += self._MBIG

		self._inext = 0
		self._inextp = 21

	def next_word(self):
		loc_inext = self._inext + 1
		loc_inextp = self._inextp + 1
		if loc_inext >= 56:
			loc_inext = 1
		if loc_inextp >= 56:
			loc_inextp = 1

		result = self._seed_array[loc_inext] - self._seed_array[loc_inextp]
		if result == self._MBIG:
			result -= 1
		if result < 0:
			result += self._MBIG

		self._seed_array[loc_inext] = result
		(self._inext, self._inextp) = (loc_inext, loc_inextp)
		return result

	def next_words(self, count):
		return [ self.next_word() for i in range(count) ]

	def next_bytes(self, count):
		return bytes(word & 0xff for word in self.next_words(count))

if __name__ == "__main__":
	def diff_arrays(reference_values, calculated_values):
		if reference_values == calculated_values:
			return
		for (i, (reference, calculated)) in enumerate(zip(reference_values, calculated_values)):
			print("%3d: %12d %12d %12d" % (i, reference, calculated, calculated - reference))

	with open("testdata.txt") as f:
		pass_cnt = 0
		fail_cnt = 0
		for line in f:
			line = line.rstrip("\r\n")
			(seed, seed_array, samples) = line.split(":")
			seed = int(seed)
			seed_array = [ int(value) for value in seed_array.split() ]
			expected_samples = [ int(value) for value in samples.split() ]

			rnd = CSharpPRNG(seed)
			calculated_seed_array = list(rnd._seed_array)
			calculated_samples = rnd.next_words(len(expected_samples))

			if (calculated_seed_array == seed_array) and (calculated_samples == expected_samples):
				pass_cnt += 1
			else:
				fail_cnt += 1

			if fail_cnt == 1:
				# First failing test
				print(seed)
				print("-" * 120)
				diff_arrays(seed_array, calculated_seed_array)
				print("-" * 120)
				diff_arrays(expected_samples, calculated_samples)
		print("%d PASS, %d FAIL" % (pass_cnt, fail_cnt))

