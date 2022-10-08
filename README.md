# binusmaya_py

Python wrapper for Binusmaya web API

## Usage

1. Import repo
    
    ```bash
    git clone https://github.com/radityaharya/binusmaya_py
    ```
    
    ```bash
    gh repo clone radityaharya/binusmaya_py
    ```
    
    ```bash
    wget https://github.com/radityaharya/binusmaya_py/archive/refs/heads/master.zip
    unzip master.zip
    ```
    
2. Install requirements 
    
    ```bash
    pip install -r requirements.txt
    ```

3. Install package
    
    ```bash
    pip install .
    ```

### Example

```python
binusmayapy.bimay import Bimay
import dotenv
import os

dotenv.load_dotenv()
bm = Bimay(token=os.getenv("BIMAY_TOKEN"))
print(bm.get_schedule_date(date_start = datetime.datetime.now()))
```

**output:**

```json
[
    {
        "class_id": "[redacted]",
        "class_session_id": "[redacted]",
        "course_name": "[redacted]",
        "course_class": "[redacted]",
        "session_number": 7,
        "delivery_mode": "VC",
        "join_url": "[redacted]",
        "location": {
            "location": null,
            "location_value": null
        },
        "date_start": "[redacted]",
        "date_end": "[redacted]",
        "topic": "[redacted]",
        "subtopic": ["[redacted]"],
        "resources": [
            {
                "resource_id": "[redacted]",
                "resource_name": "Video Conference",
                "resource_type": null,
                "resource_url": null,
                "resource_is_open": true
            },
            {
                "resource_id": "[redacted]",
                "resource_name": "[redacted]",
                "resource_type": null,
                "resource_url": "[redacted]",
                "resource_is_open": true
            },
            {
                "resource_id": "[redacted]",
                "resource_name": "[redacted]",
                "resource_type": "pptx",
                "resource_url": "[redacted]",
                "resource_is_open": true
            },
            {
                "resource_id": "[redacted]",
                "resource_name": "[redacted]",
                "resource_type": null,
                "resource_url": "[redacted]",
                "resource_is_open": true
            },
            {
                "resource_id": "[redacted]",
                "resource_name": "[redacted]",
                "resource_type": null,
                "resource_url": "[redacted]",
                "resource_is_open": true
            },
            {
                "resource_id": "[redacted]",
                "resource_name": "Javascript Introduction",
                "resource_type": null,
                "resource_url": "[redacted]",
                "resource_is_open": true
            }
        ],
        "is_ended": true
    }
]
```

Disclaimer: This project is not affiliated, associated, authorized, endorsed by, or in any way officially related to "Bina Nusantara University" and or "BinusMaya" and it is used for personal use only. The author is not liable for any damage that may occur from the use of this project.
contact@radityaharya.me
