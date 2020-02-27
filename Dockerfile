# Environment setup
FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE encouragemint.settings.production
RUN mkdir /encouragemint
WORKDIR /encouragemint
ADD . /encouragemint/
RUN pip install -r encouragemint/requirements.txt

# Server Initialization
EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]