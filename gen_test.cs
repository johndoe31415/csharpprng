//	csharpprng - Reimplementation of C# System.Random PRNG in Python.
//	Copyright (C) 2017-2017 Johannes Bauer
//
//	This file is part of csharpprng.
//
//	csharpprng is free software; you can redistribute it and/or modify
//	it under the terms of the GNU General Public License as published by
//	the Free Software Foundation; this program is ONLY licensed under
//	version 3 of the License, later versions are explicitly excluded.
//
//	csharpprng is distributed in the hope that it will be useful,
//	but WITHOUT ANY WARRANTY; without even the implied warranty of
//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//	GNU General Public License for more details.
//
//	You should have received a copy of the GNU General Public License
//	along with csharpprng; if not, write to the Free Software
//	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//
//	Johannes Bauer <JohannesBauer@gmx.de>

// mcs gen_test.cs && mono gen_test.exe 12345 && rm -f gen_test.exe

using System;
 
public class TestPRNG {
	static public void Main(String[] args) {
		int seed = int.Parse(args[0]);
		Random rnd = new System.Random(seed);

		Console.WriteLine("+ " + seed);

		var field = rnd.GetType().GetField("SeedArray", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.GetField | System.Reflection.BindingFlags.Instance);
		int[] SeedArray = (int[])field.GetValue(rnd);
		for (int i = 0; i < 56; i++) {
			Console.WriteLine("> " + SeedArray[i]);
		}

		System.Reflection.MethodInfo InternalSample = rnd.GetType().GetMethod("InternalSample", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);

		for (int i = 0; i < 1000; i++) {
			int sample = (int)InternalSample.Invoke(rnd, new object[] { });	
			Console.WriteLine(sample);
		}
	}
}
