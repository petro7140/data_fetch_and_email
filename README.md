# Custom API Data Fetcher

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it:
   ```bash
   python -m venv myenv
   source myenv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

- Update API URLs and authentication tokens in `api_connector.py`.
- Set the email credentials in `email_sender.py`.

## Usage

- Run the scheduler to start fetching data daily:
  ```bash
  python scheduler.py
  ```

## Troubleshooting

- Ensure all API keys and tokens are valid.
- Check email credentials and SMTP server settings. 