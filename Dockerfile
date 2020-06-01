FROM python:3.7

# Install node & yarn
RUN apt-get -y install curl \
  && curl -sL https://deb.nodesource.com/setup_12.x | bash \
  && apt-get install nodejs \
  && curl -o- -L https://yarnpkg.com/install.sh | bash

# Install Python dependencies
WORKDIR /app/backend
COPY ./backend/requirements.txt /app/backend/
RUN pip3 install --upgrade pip -r requirements.txt

# Install JS dependencies
WORKDIR /app/frontend
COPY ./frontend/package.json ./frontend/yarn.lock /app/frontend/
RUN $HOME/.yarn/bin/yarn install

# Add the rest of the code
COPY . /app/

# Build & collect static files static files
RUN $HOME/.yarn/bin/yarn build
RUN mkdir /app/backend/staticfiles

WORKDIR /app

# SECRET_KEY is only included here to avoid raising an error when generating static files.
RUN DJANGO_SETTINGS_MODULE=backend.settings.production \
  SECRET_KEY=foo \
  python3 manage.py collectstatic --noinput

EXPOSE $PORT

CMD python3 manage.py runserver 0.0.0.0:$PORT