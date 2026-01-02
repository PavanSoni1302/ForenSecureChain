from elasticsearch import Elasticsearch
import time

# 1. SETUP CONNECTION
# We point to your Ubuntu Server IP.
es = Elasticsearch("http://10.0.2.5:9200")

print("🔎 Searching specifically for SYSMON logs...")
print("   (Run 'Restart-Service winlogbeat' on Windows if this takes too long)")

# 2. START THE LOOP
while True:
    # 3. DEFINE THE SEARCH
    # We are asking for:
    # - Any log where the 'event.provider' field contains the word "Sysmon"
    # - Sort by newest first ("desc") so we see fresh data
    query = {
        "query": {
            "wildcard": {
                "event.provider": "*Sysmon*"
            }
        },
        "size": 1,
        "sort": [{"@timestamp": "desc"}]
    }
    
    try:
        # 4. SEND QUERY TO UBUNTU
        res = es.search(index="winlogbeat-*", body=query)
        hits = res['hits']['hits']
        
        # 5. CHECK RESULTS
        if len(hits) > 0:
            # We found one!
            log = hits[0]['_source']
            
            print("\n" + "="*40)
            print("🎉 SUCCESS! Sysmon log found!")
            print("="*40)
            
            # Print the timestamp to see if it's from 2025 or 2026
            print(f"Time:    {log.get('@timestamp')}")
            
            # Print the command line (This is what the AI needs!)
            # We use .get() repeatedly to avoid crashing if a field is missing
            cmd = log.get('process', {}).get('command_line', "No Command Line Field Found")
            print(f"Command: {cmd}")
            
            print("\n✅ Your pipeline is FIXED. You can run the Detection Engine now.")
            break  # EXIT THE LOOP
        else:
            # Database said "No results", so print a dot and try again in 2 seconds
            print(".", end="", flush=True) 
            time.sleep(2)
            
    except Exception as e:
        # If the database is offline or IP is wrong, print the error
        print(f"\n❌ Connection Error: {e}")
        time.sleep(5)