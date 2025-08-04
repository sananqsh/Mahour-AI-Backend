# AI-Powered Customer Club - Backend API

## 🚀 Features

- **RESTful API**: Comprehensive REST API with Django REST Framework
- **User Management**: Custom user authentication and profile management
- **Reward System**: Dynamic loyalty and rewards management
- **Recommendation Engine**: Personalized product/content recommendations
- **Admin Dashboard**: Comprehensive Django admin interface

# Installation
1. Clone the project
  ```bash
  git clone https://github.com/sananqsh/Findner.git
  ```
3. Change directory to the project root and fill the .env with your API keys and other configurations.
  ```bash
  cd Findner
  cp .env.example .env
  vi .env
  ```
4. Create environment
   ```bash
   python -m virtualenv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Migrate & create superuser
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Run Django
   ```bash
   python manage.py runserver
   ```

# After the installation
- You can access the admin panel at [http://localhost:8000/admin](http://localhost:8000/admin)
- and the API docs are at [http://localhost:8000/swagger/](http://localhost:8000/swagger/).
