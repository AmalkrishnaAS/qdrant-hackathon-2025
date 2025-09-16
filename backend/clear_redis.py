from upstash_redis import Redis

# Initialize Redis client with your Upstash URL and token
redis = Redis(url="https://sacred-boxer-43750.upstash.io", token="AqrmAAIgcDECbhjVdcEZb8HVEOtmIIM196fa5GtSBFFWZ_GgIc0UMA")

# Execute the FLUSHALL command
redis.flushall()

print("All data cleared from the Upstash Redis database.")