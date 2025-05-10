# process_imessage_numbers

A simple Python utility to check which phone numbers in your list are iMessage-enabled, using the BlueBubbles API. This script is useful if you want to narrow a large list of numbers down to numbers that are likely personal lines; for example, if one has a list of numbers businesses in their area have listed publicly, the ones that are iMessage enabled are likely the owners' personal lines.

---

## 📋 Features

- **CSV Input**  
  Reads a plain CSV file of phone numbers (one per line).  
- **Normalization**  
  Cleans non-digit characters and normalizes to US E.164 format (e.g. `+1XXXXXXXXXX`).  
- **Deduplication**  
  Automatically removes duplicate entries.  
- **iMessage Check**  
  Queries your local BlueBubbles server to see which numbers support iMessage.  
- **CSV Output**  
  Writes a new CSV containing only the iMessage-enabled numbers.

---

## 🔧 Prerequisites

1. **Python 3.6+**  
   Install from [python.org](https://www.python.org/downloads/).  
2. **BlueBubbles macOS server**  
   - Install the BlueBubbles app and follow the [official documentation](https://bluebubbles.app).  
   - Have your server URL and API password ready.  
3. **Credentials files** in the `process_imessage_numbers` folder:  
   - `credentials.txt` — first line: your BlueBubbles server URL  
   - `pwd.txt` — first line: your BlueBubbles API password  

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/process_imessage_numbers.git
cd process_imessage_numbers
 ```

2. **Prepare your input**:

   * Create a file called `input_numbers.csv` in this folder.
   * List one phone number per line (no headers, no extra columns):

     ```csv
     555-123-4567
     (555) 234-5678
     +1 555 345 6789
     ```

3. **Add your BlueBubbles credentials**:

   ```bash
   echo "http://localhost:1234" > credentials.txt
   echo "your_api_password_here" > pwd.txt
   ```

4. **Run the script**:

   ```bash
   python process_imessage_numbers.py input_numbers.csv --output imessage_only.csv
   ```

   * **`--output`** is optional (defaults to `imessage_numbers.csv`).

5. **View the results**:

   * Open `imessage_only.csv` (or your chosen output file) to see only the iMessage-enabled phone numbers.

---

## 🔍 How It Works

1. **Reads** each line of your input file.
2. **Cleans** non-digit characters, normalizes to `+1XXXXXXXXXX` format.
3. **Deduplicates** entries to avoid repeat checks.
4. **Waits** a random 5–10 seconds between each check to prevent rate-limits.
5. **Sends** a request to your BlueBubbles server API endpoint `/api/v1/handle/availability/imessage`.
6. **Parses** the JSON response, keeping only phone numbers where `data.available == true`.
7. **Writes** the filtered list to your specified output CSV.

---

## ❓ Troubleshooting

* **Script errors during startup**: Ensure `credentials.txt` and `pwd.txt` exist and contain valid values.
* **Permission denied**: Run the script with a Python virtual environment or with `sudo` if necessary.
* **Empty output**: No numbers in your list are iMessage-enabled, or your BlueBubbles server isn’t reachable. Verify your server URL and password.
