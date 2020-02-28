FROM python:3.6
ENV PROJECT_ROOT /app
WORKDIR $PROJECT_ROOT
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE encouragemint.settings.production
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:8000