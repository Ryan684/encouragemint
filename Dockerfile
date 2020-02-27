FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /encouragemint
WORKDIR /encouragemint
ADD . /encouragemint/
RUN pip install -r encouragemint/requirements.txt
RUN python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000