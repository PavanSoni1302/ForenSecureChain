from elasticsearch import Elasticsearch
import json

# Connect
es = Elasticsearch("http://10.0.2.5:9200")

print("1. Checking connection...")
if es.ping():
    print("✅ Connection OK!")
else:
    print("❌ Connection Failed.")
    exit()

print("\n2. Checking Indices...")
indices = es.indices.get_alias(index="*")
print("Found indices:", list(indices.keys()))

print("\n3. Grabbing LAST log (No filters)...")
# We remove the 'process.command_line' requirement
query = {
    "query": {"match_all": {}},
    "size": 1,
    "sort": [{"@timestamp": "desc"}]
}

res = es.search(index="winlogbeat-*", body=query)

if len(res['hits']['hits']) > 0:
    print("✅ SUCCESS! Found a log.")
    log = res['hits']['hits'][0]['_source']
    print("Timestamp:", log.get('@timestamp'))
    
    # CHECK IF COMMAND LINE EXISTS
    cmd = log.get('process', {}).get('command_line')
    if cmd:
        print(f"🎉 Command Line Found: {cmd}")
    else:
        print("⚠️ Log found, BUT 'command_line' is MISSING.")
        print("Reason: Sysmon might not be installed or configured.")
else:
    print("❌ DB is empty.")