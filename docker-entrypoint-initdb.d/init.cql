CREATE KEYSPACE cricket
	WITH REPLICATION = {
		'class': 'org.apache.cassandra.locator.SimpleStrategy',
		'replication_factor': '1'
	}
	AND DURABLE_WRITES = true;

use cricket;

CREATE TABLE cricket.cricket_data3(
	 date_ date,
	 hasSquad boolean,
	 id text,
	 matchEnded boolean,
	 matchStarted boolean,
	 matchType text,
	 name text,
	 series_id text,     
	 status text,	 
	 venue text
 );