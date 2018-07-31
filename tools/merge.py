from dictdiffer import diff, patch
from xmltodict import parse, unparse
import os
import sys

from utils import read, write


def main():
	base_path = os.environ.get('BASE')
	local_path = os.environ.get('LOCAL')
	remote_path = os.environ.get('REMOTE')
	merged_path = os.environ.get('MERGED')
	
	print('BASE: %s' % (base_path,))
	print('LOCAL: %s' % (local_path,))
	print('REMOTE: %s' % (remote_path,))
	print('MERGED: %s' % (merged_path,))
	print()

	# Ensure paths have been provided
	for path in (base_path, local_path, remote_path, merged_path):
		if path is None:
			print('Missing path for base, local, remote or merged')
			sys.exit(1)
			return

	# Ensure source paths exist
	for path in (base_path, local_path, remote_path):
		if not os.path.exists(path):
			print('File doesn\'t exist at: %s' % (path,))
			sys.exit(1)
			return

	# Parse items
	base, _ = read(base_path)
	local, unix = read(local_path)
	remote, _ = read(remote_path)

	# Find changes between base and remote
	print('Finding change(s)...')
	
	changes = list(diff(base, remote))

	# Apply changes to local
	print('Applying %d change(s)...' % (len(changes),))

	patch(changes, local, in_place=True)

	# Write result to file
	print('Writing result (unix: %r)...' % (unix,))

	write(
		merged_path, local,
		unix=unix
	)


if __name__ == '__main__':
	main()
