# CKAN Stats


## First impressions
	select trim(resource_format), COUNT(resource_format) as count from datahubio
	group by resource_format order by count desc
	
![](firstimpressions_resource_format_counts.png)