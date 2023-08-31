# This is a script to generate test data.
# It has no utility in a production environment.

import argparse
import os
import random

# Define command line arguments
parser = argparse.ArgumentParser(description='Generate files of random data')
parser.add_argument('num_files', type=int, help='Number of files to generate')
parser.add_argument('file_size', type=int, help='Size of each file in bytes')
parser.add_argument('--output_dir', default='data', help='Output directory for generated files')
args = parser.parse_args()

# Create output directory if it doesn't exist
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

# Generate random data and write to files
for i in range(args.num_files):
    filename = os.path.join(args.output_dir, f'marmosets{i}.dat')
    print("Generating file", filename)
    with open(filename, 'wb') as f:
        data = bytearray(random.getrandbits(8) for _ in range(args.file_size))
        f.write(data)
print("Done")