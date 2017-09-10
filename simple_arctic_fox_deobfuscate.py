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

with open(sys.argv[1], "rb") as f:
	data = f.read()[4:]

xor_pattern = bytes(byte ^ plaintext for (byte, plaintext) in zip(data[0 : 9], bytes.fromhex("ef bb bf") + b"<Seria"))
deobfuscated_data = bytes(byte ^ xor_pattern[i % 9] for (i, byte) in enumerate(data))
print(deobfuscated_data[3:].decode())

