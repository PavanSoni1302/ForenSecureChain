from elasticsearch import Elasticsearch
import time
import json

es = Elasticsearch("http://10.0.2.5:9200")

print("🔎 Waiting for a SYSMON EVENT ID 1 (Process Create)...")
print("👉 Please run 'whoami /priv' in a NEW Administrator Command Prompt NOW.")

while True:
    # We specifically ask for Event Code 1 (Process Create)
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"event.code": "1"}},
                    {"wildcard": {"event.provider": "*Sysmon*"}}
                ]
            }
        },
        "size": 1,
        "sort": [{"@timestamp": "desc"}]
    }
    
    try:
        res = es.search(index="winlogbeat-*", body=query)
        if len(res['hits']['hits']) > 0:
            log = res['hits']['hits'][0]['_source']
            
            print("\n" + "="*50)
            print("🎉 CAPTURED EVENT ID 1!")
            print("="*50)
            
            # Check 1: The Standard Field
            std_cmd = log.get('process', {}).get('command_line')
            print(f"1. Standard Field (process.command_line): {std_cmd}")
            
            # Check 2: The Raw Windows Field
            raw_cmd = log.get('winlog', {}).get('event_data', {}).get('CommandLine')
            print(f"2. Raw Field (winlog.event_data.CommandLine): {raw_cmd}")
            
            # Check 3: The Message Field (Fallback)
            message = log.get('message', '')
            if 'CommandLine:' in message:
                print("3. Found inside 'message' block: YES")
            else:
                print("3. Found inside 'message' block: NO")

            print("\n⬇️ RAW LOG DUMP (Look for the command here) ⬇️")
            print(json.dumps(log, indent=2))
            break
        else:
            print(".", end="", flush=True)
            time.sleep(2)
            
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)