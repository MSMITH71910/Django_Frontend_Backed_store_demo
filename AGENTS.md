# Repository Guidelines

## Project Structure & Module Organization
This is a Django-based e-commerce application. The codebase is organized as follows:
- **`./mysite/`**: Root directory of the Django project.
- **`./mysite/mysite/`**: Project configuration, including settings, URLs, and ASGI/WSGI configurations.
- **`./mysite/myapp/`**: Core application logic.
    - **`./mysite/myapp/models.py`**: Defines the `Product` model with slug generation logic.
    - **`./mysite/myapp/views.py`**: Contains view functions like `index` for rendering pages.
    - **`./mysite/myapp/templates/myapp/`**: HTML templates for the application.
- **`./mysite/media/`**: Directory for user-uploaded files, such as product images.

## Build, Test, and Development Commands
Use the following commands from the `./mysite/` directory:
- **Run Development Server**: `python manage.py runserver`
- **Database Migrations**: `python manage.py makemigrations` followed by `python manage.py migrate`
- **Run Tests**: `python manage.py test`
- **Create Superuser**: `python manage.py createsuperuser`

## Coding Style & Naming Conventions
- Follow standard Django conventions for models, views, and templates.
- **Models**: Use `slugify` for generating unique slugs in the `save` method of models.
- **Templates**: Application-specific templates should be placed in `myapp/templates/myapp/`.

## Testing Guidelines
- Tests are located in `mysite/myapp/tests.py`.
- Ensure new features are accompanied by relevant test cases.
