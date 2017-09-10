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

import sys
import struct
from CSharpPRNG import CSharpPRNG

class ArcticFoxDeobfuscator(object):
	def __init__(self, filename):
		with open(filename, "rb") as f:
			seed_bytes = bytes(seedbyte ^ 0x17 for seedbyte in f.read(4))
			(seed, ) = struct.unpack("<i", seed_bytes)
			prng = CSharpPRNG(seed)
			xordata = prng.next_bytes(9)
			obfuscated_data = f.read()
			self._deobfuscated_data = bytes(obfuscated_byte ^ xordata[i % 9] for (i, obfuscated_byte) in enumerate(obfuscated_data))

	@property
	def deobfuscated_data(self):
		return self._deobfuscated_data

	@property
	def is_valid(self):
		return self._deobfuscated_data[0 : 3] == bytes.fromhex("ef bb bf")

	@property
	def xml_text(self):
		return self._deobfuscated_data[3:].decode()

deobfuscator = ArcticFoxDeobfuscator(sys.argv[1])
if deobfuscator.is_valid:
	print(deobfuscator.xml_text)
else:
	print("Cannot deobfuscate file.")
