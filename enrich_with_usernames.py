import csv
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from aws_client import get_boto3_client
from datetime import timezone
from dateutil import parser as dt_parser
from boto3.exceptions import Boto3Error
import json



load_dotenv()

input_file = os.getenv('ACTIVE_RESOURCES_FILE')
output_file = os.getenv('ENRICHED_RESOURCES_FILE')

def find_user_from_cloudtrail(resource_name, _unused_resource_type, created_at, region):
    cloudtrail = get_boto3_client('cloudtrail', region)

    # Parse and define time range for lookup
    try:
        created_dt = dt_parser.parse(created_at)
    except Exception as e:
        print(f"[ERROR] Invalid created_at timestamp: {created_at} — {e}")
        return "InvalidDate"

    start_time = created_dt - timedelta(minutes=5)
    end_time = created_dt + timedelta(minutes=10)

    try:
        paginator = cloudtrail.get_paginator('lookup_events')
        pages = paginator.paginate(
            StartTime=start_time,
            EndTime=end_time,
            LookupAttributes=[
                {
                    'AttributeKey': 'ResourceName',
                    'AttributeValue': resource_name
                }
            ]
        )

        for page in pages:
            for event in page.get('Events', []):
                event_name = event.get('EventName', '').lower()
                if not event_name.startswith("create"):
                    continue

                resources = event.get('Resources', [])
                for res in resources:
                    if res.get('ResourceName', '') == resource_name:
                        # Found matching event for resource name
                        return event.get('Username', 'Unknown')

    except Boto3Error as e:
        print(f"[Boto3 ERROR] CloudTrail API failed: {e}")
    except Exception as e:
        print(f"[ERROR] Processing CloudTrail lookup: {e}")

    return "Unknown"
# Read and process
resources = []
with open(input_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Name', '').strip()
        created_at = row.get('CreatedAt')
        region = row.get('Region')
        resource_type = row.get('ResourceType')

        # Skip rows without created_at or region
        if not created_at or not region:
            continue

        # Only look at resources created within the last 30 days
        try:
            created_dt = datetime.fromisoformat(created_at)
        except ValueError:
            print(f"[WARNING] Skipping row with invalid date: {created_at}")
            row['UserName'] = "InvalidDate"
            resources.append(row)
            continue

        if datetime.now(timezone.utc) - created_dt <= timedelta(days=30):
            user_name = find_user_from_cloudtrail(name, resource_type, created_at, region)
            row['UserName'] = user_name
        else:
            row['UserName'] = "OlderThan30Days"


        resources.append(row)

# Save enriched file
fieldnames = list(resources[0].keys())
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(resources)

print(f"✅ Enriched file written to {output_file}")
