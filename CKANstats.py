#!/usr/bin/env python

# Retrieves meta data from CKAN repositories and writes it into a CSV file
# Some snippets taken from http://docs.ckan.org/en/ckan-2.0/api.html


import urllib2
import urllib
import json
import pprint

import csv

package_list_url = 'http://demo.ckan.org/api/3/action/package_list'

# http://demo.ckan.org/api/3/action/package_search?q=name:ckandown
package_search_url = 'http://demo.ckan.org/api/3/action/package_search'


# Use the json module to dump a dictionary to a string for posting.

data_string = ""

# Make the HTTP request.
list_response = urllib2.urlopen(package_list_url)
assert list_response.code == 200

# Use the json module to load CKAN's response into a dictionary.
package_list = json.loads(list_response.read())

# Check the contents of the response.
assert package_list['success'] is True


with open('ckanstats.csv', mode='wb') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

	# dataset.id
	# dataset.name
	# dataset.license_title
	# dataset.license_id
	# resource.id
	# resource.name
	# resource.created
	# resource.revision_timestamp
	# resource.format
	# resource.url
	csvwriter.writerow(['dataset.id','dataset.name','dataset.license_title','dataset.license_id','resource.id','resource.name','resource.created','resource.revision_timestamp','resource.format','resource.url'])

	for package_name in package_list['result']:
		data_string = urllib.quote(json.dumps({'q': ('name:' + package_name)}))
		
		response = urllib2.urlopen(package_search_url, data_string)
		assert response.code == 200

		search_result = json.loads(response.read())

		assert search_result['success'] is True
		assert search_result['result']['count'] is 1

		for inner_result in search_result['result']['results']:
			dataset_id = inner_result['id'] or ""
			dataset_name = inner_result['name'] or ""
			dataset_license_title = inner_result['license_title'] or ""
			dataset_license_id = inner_result['license_id'] or ""

			print inner_result['name']

			for resource in inner_result['resources']:
				resource_id = resource['id'] or ""
				resource_name = resource['name'] or ""
				resource_created = resource['created'] or ""
				resource_revision_timestamp = resource['revision_timestamp'] or ""
				resource_format = resource['format'] or ""
				resource_url = resource['url'] or ""


				# Python 2's CSVWriter does not seem to support UTF-8 :/
				# https://github.com/jdunck/python-unicodecsv
				csvwriter.writerow([dataset_id.encode("ascii", 'ignore'),dataset_name.encode("ascii", 'ignore'),dataset_license_title.encode("ascii", 'ignore'),dataset_license_id.encode("ascii", 'ignore'),resource_id.encode("ascii", 'ignore'),resource_name.encode("ascii", 'ignore'),resource_created.encode("ascii", 'ignore'),resource_revision_timestamp.encode("ascii", 'ignore'),resource_format.encode("ascii", 'ignore'),resource_url.encode("ascii", 'ignore')])
