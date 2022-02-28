# binusmaya.py

Python wrapper for Binusmaya web API

## Usage

1. Import repo
    
    ```bash
    git clone https://github.com/radityaharya/binusmaya.py
    ```
    
    ```bash
    gh repo clone radityaharya/binusmaya.py
    ```
    
    ```bash
    wget https://github.com/radityaharya/binusmaya.py/archive/refs/heads/master.zip
    unzip master.zip
    ```
    
2. Install requirements 
    
    ```bash
    pip install -r requirements.txt
    ```
    

### Example

```python
from bimay import bimay
import dotenv
import os

dotenv.load_dotenv()
bm = bimay(token=os.getenv("token"), roleId=os.getenv("roleId"))
print(bm.get_schedule_date(date_start = datetime.datetime.now()))
```

**output:**

```json
[
  {
    "dateStart": "2022-03-01T07:20:00",
    "dateEnd": "2022-03-01T08:50:00",
    "title": "[redacted]",
    "content": "[redacted]",
    "location": null,
    "locationValue": null,
    "scheduleType": "Virtual Class",
    "customParam": {
      "classId": "[redacted]",
      "classSessionId": "[redacted]",
      "sessionNumber": 2,
      "classSessionContentId": "[redacted]"
    },
    "classDeliveryMode": "VC",
    "deliveryMode": "VC",
    "deliveryModeDesc": "Video Conference",
    "academicCareerDesc": "Undergraduate",
    "institutionDesc": "BINUS University",
    "organizationRoleId": "[redacted]"
  },
  {
    "dateStart": "2022-03-01T09:20:00",
    "dateEnd": "2022-03-01T10:50:00",
    "title": "[redacted]",
    "content": "[redacted]",
    "location": null,
    "locationValue": null,
    "scheduleType": "Virtual Class",
    "customParam": {
      "classId": "[redacted]",
      "classSessionId": "[redacted]",
      "sessionNumber": 2,
      "classSessionContentId": "[redacted]"
    },
    "classDeliveryMode": "VC",
    "deliveryMode": "VC",
    "deliveryModeDesc": "Video Conference",
    "academicCareerDesc": "Undergraduate",
    "institutionDesc": "BINUS University",
    "organizationRoleId": "[redacted]"
  }
]
```

Disclaimer: This project is not affiliated, associated, authorized, endorsed by, or in any way officially related to "Bina Nusantara University" and or "BinusMaya" and it is used for personal use only.
contact@otid.site