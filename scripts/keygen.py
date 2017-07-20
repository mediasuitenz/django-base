#!/usr/bin/env python

# Generate a random secret key

import random, string

sr = random.SystemRandom()
length = 64

alphabet = string.ascii_letters + string.digits + string.punctuation
print(''.join(sr.choice(alphabet) for l in range(length)))
