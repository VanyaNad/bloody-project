# Preloaded Data
   - Admin User
      - Username: admin
      - Password: admin
   - Test User
     - Username: test
     - Password: FT5BAk!4SM@vMny



## How to Run the Project
1. Clone the repository:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py loaddata data.json
   python manage.py runserver
