import os
import csv
from dotenv import load_dotenv
from functions import *

load_dotenv()

# Read service list from cost file
with open(os.getenv('RESOURCE_COST_FILE'), 'r') as f:
    services = [line.split('($)')[0].strip() for line in f if '($)' in line]

# Read regions from regions.txt
with open(os.getenv('REGIONS_FILE'), 'r') as f:
    regions = [line.strip() for line in f if line.strip()]

output_file = os.getenv('ACTIVE_RESOURCES_FILE')
fieldnames = ['Name', 'CreatedAt', 'ResourceType', 'Region']
all_resources = []
unique_names = set()  # Track already added names

# Switch-style function map
service_functions = {
    'EC2-Instances': get_running_ec2_instances,
    'Relational Database Service': get_available_rds_instances,
    'S3-Buckets': get_active_s3_buckets,
    'OpenSearch Service': get_active_opensearch_domains,
    'Amplify': get_active_amplify_apps,
    'Elastic Load Balancing': get_active_elbs,
    'Kinesis': get_active_kinesis_streams,
    'CloudTrail': get_active_cloudtrails,
    'ElastiCache': get_active_elasticache_clusters
}

# Loop through each region and each service
for region in regions:
    for service in services:
        func = service_functions.get(service)
        if func:
            print(f"🔍 Fetching {service} in {region}...")
            try:
                resources = func(region)
                for resource in resources:
                    name = resource.get('Name')
                    if not name or name in unique_names:
                        continue
                    resource['Region'] = region  # Add region info
                    unique_names.add(name)
                    all_resources.append(resource)
            except Exception as e:
                print(f"[ERROR] Failed for {service} in {region}: {e}")
        else:
            print(f"[WARNING] No function mapped for service: {service}")

# Write combined results to CSV
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_resources)

print(f"✅ Active resources saved to {output_file}")
