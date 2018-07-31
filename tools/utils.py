from xmltodict import parse, unparse

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

try:
	from cStringIO import StringIO
except ImportError:
	try:
		from StringIO import StringIO
	except ImportError:
		from io import StringIO


def read(path):
	with open(path, 'r') as fp:
		data = fp.read()

	# Parse document from data
	doc = parse(data)

	# Add "tmdbmid" attribute
	for item in doc['anime-list']['anime']:
		if '@tmdbid' not in item:
			continue

		# Set @tmdbmid to @tmdbid (if not defined)
		if '@tmdbmid' not in item:
			item['@tmdbmid'] = item['@tmdbid']

		# Ensure identifiers match
		if item['@tmdbid'] != item['@tmdbmid']:
			raise Exception('%r != %r' % (item['@tmdbid'], item['@tmdbmid']))

	# Index items by anidb id
	doc['anime-list']['anime'] = OrderedDict([
		(item['@anidbid'], item)
		for item in doc['anime-list']['anime']
	])

	return doc, '\r\n' in data

def write(path, doc, unix=False):
	# Convert items to list
	doc['anime-list']['anime'] = doc['anime-list']['anime'].values()

	# Encode document
	buf = StringIO()

	unparse(
		doc,
		output=buf,

		indent='  ',
		newl='\n',
		pretty=True,
		short_empty_elements=True
	)

	# Convert to string
	data = buf.getvalue() + '\n'

	if unix:
		data = data.replace('\n', '\r\n')

	# Write data to path
	with open(path, 'w') as fp:
		fp.write(data)
