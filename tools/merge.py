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
	
	changes = list(resolve(base, local, remote))

	# Apply changes to local
	print('Applying %d change(s)...' % (len(changes),))

	patch(changes, local, in_place=True)

	# Write result to file
	print('Writing result (unix: %r)...' % (unix,))

	write(
		merged_path, local,
		unix=unix
	)

def resolve(base, local, remote):
	for op, path, value in diff(base, remote):
		if op == 'remove' and path == 'anime-list.anime':
			value = list(on_anime_removed(base, local, remote, value))

		# Ignore empty changes
		if not value:
			continue

		# Yield change
		yield op, path, value

def on_anime_removed(base, local, remote, items):
	for key, value in items:
		# Ignore items that have been already removed
		if key not in local['anime-list']['anime']:
			continue

		# Yield removed item
		yield key, value


if __name__ == '__main__':
	main()
