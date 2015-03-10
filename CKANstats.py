#!/usr/bin/env python

# Retrieves meta data from CKAN repositories and writes it into a CSV file
# Some snippets taken from http://docs.ckan.org/en/ckan-2.0/api.html


import urllib2
import urllib
import json
import pprint

import csv

repository_url = "datahub.io" # <--- Change this
delimiter = ','


package_list_url = 'http://' + repository_url + '/api/3/action/package_list'

# http://demo.ckan.org/api/3/action/package_search?q=name:ckandown
package_search_url = 'http://' + repository_url + '/api/3/action/package_search'



# Removes non-ASCII / Delimiter characters
def cleanFieldValue(fieldValue):
	fieldValue = str(fieldValue)
	fieldValue = fieldValue.encode("ascii", 'ignore')
	fieldValue = fieldValue.replace(delimiter, "")
	return fieldValue


# Use the json module to dump a dictionary to a string for posting.

data_string = ""

# Make the HTTP request.
list_response = urllib2.urlopen(package_list_url)
assert list_response.code == 200

# Use the json module to load CKAN's response into a dictionary.
package_list = json.loads(list_response.read())

# Check the contents of the response.
assert package_list['success'] is True


with open(repository_url + '.csv', mode='wb') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=delimiter,quotechar='|', quoting=csv.QUOTE_MINIMAL)

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
	csvwriter.writerow(['dataset.id','dataset.name','dataset.license_title','dataset.license_id','dataset.isopen','dataset.tracking_summary.total','dataset.tracking_summary.recent','resource.id','resource.name','resource.created','resource.revision_timestamp','resource.format','resource.url','resource_tracking_summary_total','resource_tracking_summary_recent'])

	for package_name in package_list['result']:
		data_string = urllib.quote(json.dumps({'q': ('name:' + package_name)}))
		
		response = urllib2.urlopen(package_search_url, data_string)
		assert response.code == 200

		search_result = json.loads(response.read())

		assert search_result['success'] is True
		assert search_result['result']['count'] is 1

		for inner_result in search_result['result']['results']:
			dataset_id = cleanFieldValue(inner_result['id'] or "n/a")
			dataset_name = cleanFieldValue(inner_result['name'] or "n/a")
			dataset_license_title = cleanFieldValue(inner_result['license_title'] or "n/a")
			dataset_license_id = cleanFieldValue(inner_result['license_id'] or "n/a")
			dataset_is_open = cleanFieldValue(inner_result['isopen'] or "False")
			# http://docs.ckan.org/en/tracking-fixes/tracking.html#retrieving-tracking-data
			dataset_tracking_summary_total = cleanFieldValue(inner_result['tracking_summary']['total'] or "0")
			dataset_tracking_summary_recent = cleanFieldValue(inner_result['tracking_summary']['recent'] or "0")

			print inner_result['name']

			for resource in inner_result['resources']:
				resource_id = cleanFieldValue(resource['id'] or "n/a")
				resource_name = cleanFieldValue(resource['name'] or "n/a")
				resource_created = cleanFieldValue(resource['created'] or "n/a")
				resource_revision_timestamp = cleanFieldValue(resource['revision_timestamp'] or "n/a")
				resource_format = cleanFieldValue(resource['format'] or "n/a")
				resource_url = cleanFieldValue(resource['url'] or "n/a")

				resource_tracking_summary_total = cleanFieldValue(resource['tracking_summary']['total'] or "0")
				resource_tracking_summary_recent = cleanFieldValue(resource['tracking_summary']['recent'] or "0")


				# Python 2's CSVWriter does not seem to support UTF-8 :/
				# https://github.com/jdunck/python-unicodecsv
				csvwriter.writerow([dataset_id,dataset_name,dataset_license_title,dataset_license_id,dataset_is_open,dataset_tracking_summary_total,dataset_tracking_summary_recent,resource_id,resource_name,resource_created,resource_revision_timestamp,resource_format,resource_url,resource_tracking_summary_total,resource_tracking_summary_recent])
