## 🔧 Setup Instructions

### 1. 📦 Install Dependencies

```bash
pip install boto3 python-dotenv python-dateutil
```

# Input and output file paths
RESOURCE_COST_FILE=resource_cost.txt
REGIONS_FILE=regions.txt
ACTIVE_RESOURCES_FILE=active_resources.csv
ENRICHED_CSV=active_enriched.csv


# AWS credentials (optional if already configured via AWS CLI)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=your_session_token  # optional

## ⚙️ How It Works

### 🔍 Step 1: Discover Active Resources

Run the following command to discover active AWS resources:

```bash
python get_active_resources.py
```
### Step 2 : Enrich With Usernames

```bash
python enrich_with_usernames.py
```
