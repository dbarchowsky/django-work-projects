# Work Projects

Work Projects is a Django app for managing work projects information.

## Installation

`npm install https://s3-us-west-2.amazonaws.com/nrose-django-packages/django-work-projects-0.1.1.post2.tar.gz` *(or `.zip`)*

## Usage

1. Add `work_projects` to `INSTALLED_APPS` setting:
```python
# yourapp/settings.py
# ...
    INSTALLED_APPS = (
        ...
        'work_projects',
    )
```
2. There are no front-end URLs defined for the package.
3. Run `python manage.py migrate` to create the contact info models.
4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create an address (you'll need the Admin app enabled).
5. Intended as a way to quickly share and maintain consistent work project models across Django web applications.