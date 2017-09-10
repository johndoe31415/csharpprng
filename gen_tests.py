#!/usr/bin/python3
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

import os
import subprocess
import random

subprocess.check_call([ "mcs", "gen_test.cs" ])

randomized_tests = 100
for seed in [ -10, 0, 10, 1234567, -(2 ** 31), -(2 ** 31) + 1, (2 ** 31) - 1, (2 ** 31) - 2, 161803398 ] + [ random.randint(-(2 ** 31), (2 ** 31)-1) for i in range(randomized_tests) ]:
	data = subprocess.check_output([ "mono", "gen_test.exe", str(seed) ])
	data = data.decode("utf-8")
	data = data.strip().split("\n")

	seed_value = None
	seed_array = [ ]
	samples = [ ]
	for line in data:
		if line.startswith("+ "):
			seed_value = int(line[2:])
		elif line.startswith("> "):
			seed_array.append(int(line[2:]))
		else:
			samples.append(int(line))

	print("%d : %s : %s" % (seed, " ".join(str(value) for value in seed_array), " ".join(str(value) for value in samples)))

os.unlink("gen_test.exe")
