# CKAN Stats

## Setup
### 1. Retrieve meta data from CKAN-based data repositories
	CKANstats.py
### 2. Load retrieved CSV into SQL (here: PostgreSQL)
	CREATE TABLE datahubio
	(
	  dataset_id character(36),
	  dataset_name character(1024),
	  dataset_license_title character(2014),
	  dataset_license_id character(255),
	  dataset_is_open boolean,
	  dataset_tracking_summary_total integer,
	  dataset_tracking_summary_recent integer,
	  resource_id character(36),
	  resource_name character(1024),
	  resource_created character(26),
	  resource_revision_timestamp character(26),
	  resource_format character(1024),
	  resource_url character(1024),
	  resource_tracking_summary_total integer,
	  resource_tracking_summary_recent integer
	)
	
	COPY datahubio FROM 'datahubio.csv' DELIMITER ',' CSV;
	
### 3. Start querying :)
	
## First impressions

### "format" row is not unified, about 20% w/o definition
	select trim(resource_format), (COUNT(resource_format)::double precision / (select COUNT(resource_format) from datahubio)::double precision * 100) as c from datahubio
	group by resource_format order by c desc

![](firstimpressions_formatspie.png)

	select trim(resource_format), COUNT(resource_format) as count from datahubio
	group by resource_format order by count desc
	
![](firstimpressions_resource_format_counts.png)

### There are at least 29 variants for the format "Excel"

	select trim(resource_format), COUNT(resource_format) as count from datahubio
	where resource_format like '%xls%' or resource_format like '%excel%' or resource_format like '%openxml%.spreadsheet%'
	group by resource_format order by count desc


resource_format|count
-----|-----
application/vnd.ms-excel|298
xlsx|196
zip:xls|54
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet|50
data file in excel|49
microsoft excel|41
application/zip+application/vnd.ms-excel|10
excel|10
application/zip+vnd.ms-excel|6
format-xls|6
xls (zip)|5
application/vnd.ms-excel.sheet.binary.macroenabled.12|4
ms excel csv|2
application/x-excel|2
csv stata excel|2
xls html pdf|2
data file in stata and excel|1
html xls|1
csv xls ods pdf mm|1
data file in excel and rdf|1
data file in excel and stata|1
csv and xls|1
csv xls m.fl.|1
html xls pdf|1
csv xls prn dbase med flere|1
xls csv|1
pdf / xls|1
xls html ascii|1
csv xls openoffice pdf mm|1


### The number of resources per datasets strongly varies
	select AVG(count), STDDEV(count), variance(count) from (
		select trim(dataset_name), COUNT(resource_id) as count from datahubio
		group by dataset_name order by count desc
	) as l


avg|stddev|variance
------|------|------
3.2128405289150868|13.2269114412110874|174.9511862736407655


### Majority of the datasets have exactly one resource file associated
	select count, count(count) from (
		select trim(dataset_name), COUNT(resource_id) as 		count from datahubio
		group by dataset_name order by count desc
	) as l group by count order by l.count
		
![](firstimpressions_resources_per_dataset.png)


### Some of the 'n/a' formats might be retrieved from the resource_url

	select format, count(format) from (
		select UPPER(substring(trim(resource_url) from '...$')) as format 		from datahubio where resource_format = 'n/a'	
	) as i
	group by format order by count(format) desc

format|count
----|----
PDF|747
RG/|295
CES|250
KEY|247
TML|158
PHP|53
CSV|51
ZIP|49
HTM|47
COM|34
OM/|30
SPX|30
TA/|26
D=0|23
OV/|21
JSP|19
ATA|18
ONE|16
.GZ|15
ORG|14
ES/|13
RQL|13
RCH|12
SON|12
OAD|11
AU/|11
ER/|11
=EN|10
TXT|10
DU/|9
XLS|8