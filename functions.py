# functions.py

from aws_client import get_boto3_client

def get_running_ec2_instances(region):
    ec2 = get_boto3_client('ec2', region)
    instances = []
    try:
        response = ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance.get('InstanceId', 'N/A')
                name_tag = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), None)
                combined_name = f"{instance_id} ({name_tag})" if name_tag else instance_id
                instances.append({
                    'Name': combined_name,
                    'CreatedAt': instance.get('LaunchTime', 'N/A').isoformat(),
                    'ResourceType': 'EC2 Instance'
                })
    except Exception as e:
        print(f"[ERROR] EC2 ({region}): {e}")
    return instances

def get_available_rds_instances(region):
    rds = get_boto3_client('rds', region)
    instances = []
    try:
        response = rds.describe_db_instances()
        for db in response['DBInstances']:
            if db['DBInstanceStatus'] == 'available':
                instances.append({
                    'Name': db['DBInstanceIdentifier'],
                    'CreatedAt': db['InstanceCreateTime'].isoformat(),
                    'ResourceType': 'RDS Instance'
                })
    except Exception as e:
        print(f"[ERROR] RDS ({region}): {e}")
    return instances

def get_active_s3_buckets(region):
    s3 = get_boto3_client('s3', region)
    buckets = []
    try:
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            buckets.append({
                'Name': bucket['Name'],
                'CreatedAt': bucket['CreationDate'].isoformat(),
                'ResourceType': 'S3 Bucket'
            })
    except Exception as e:
        print(f"[ERROR] S3 ({region}): {e}")
    return buckets

def get_active_opensearch_domains(region):
    os_client = get_boto3_client('opensearch', region)
    domains = []
    try:
        domain_names = os_client.list_domain_names()['DomainNames']
        for domain in domain_names:
            desc = os_client.describe_domain(DomainName=domain['DomainName'])
            info = desc['DomainStatus']
            domains.append({
                'Name': info['DomainName'],
                'CreatedAt': info['Created'] if 'Created' in info else 'N/A',
                'ResourceType': 'OpenSearch Domain'
            })
    except Exception as e:
        print(f"[ERROR] OpenSearch ({region}): {e}")
    return domains

def get_active_amplify_apps(region):
    amplify = get_boto3_client('amplify', region)
    apps = []
    try:
        response = amplify.list_apps()
        for app in response['apps']:
            apps.append({
                'Name': app['name'],
                'CreatedAt': app['createTime'].isoformat(),
                'ResourceType': 'Amplify App'
            })
    except Exception as e:
        print(f"[ERROR] Amplify ({region}): {e}")
    return apps

def get_active_elbs(region):
    elb = get_boto3_client('elbv2', region)
    elbs = []
    try:
        response = elb.describe_load_balancers()
        for lb in response['LoadBalancers']:
            elbs.append({
                'Name': lb['LoadBalancerName'],
                'CreatedAt': lb['CreatedTime'].isoformat(),
                'ResourceType': 'ELBv2'
            })
    except Exception as e:
        print(f"[ERROR] ELBv2 ({region}): {e}")
    return elbs

def get_active_kinesis_streams(region):
    kinesis = get_boto3_client('kinesis', region)
    streams = []
    try:
        response = kinesis.list_streams()
        for name in response['StreamNames']:
            desc = kinesis.describe_stream(StreamName=name)
            created_at = desc['StreamDescription']['StreamCreationTimestamp'].isoformat()
            streams.append({
                'Name': name,
                'CreatedAt': created_at,
                'ResourceType': 'Kinesis Stream'
            })
    except Exception as e:
        print(f"[ERROR] Kinesis ({region}): {e}")
    return streams

def get_active_cloudtrails(region):
    ct = get_boto3_client('cloudtrail', region)
    trails = []
    try:
        response = ct.describe_trails()
        for trail in response['trailList']:
            trails.append({
                'Name': trail['Name'],
                'CreatedAt': trail.get('HomeRegion', 'N/A'),
                'ResourceType': 'CloudTrail'
            })
    except Exception as e:
        print(f"[ERROR] CloudTrail ({region}): {e}")
    return trails

def get_active_elasticache_clusters(region):
    cache = get_boto3_client('elasticache', region)
    clusters = []
    try:
        response = cache.describe_cache_clusters(ShowCacheNodeInfo=True)
        for cluster in response['CacheClusters']:
            if cluster['CacheClusterStatus'] == 'available':
                clusters.append({
                    'Name': cluster['CacheClusterId'],
                    'CreatedAt': cluster['CacheClusterCreateTime'].isoformat(),
                    'ResourceType': 'ElastiCache'
                })
    except Exception as e:
        print(f"[ERROR] ElastiCache ({region}): {e}")
    return clusters
