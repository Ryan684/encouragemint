FROM python:3.7

# Install node
RUN apt-get -y install curl \
  && curl -sL https://deb.nodesource.com/setup_12.x | bash \
  && apt-get install nodejs

# Install Python dependencies
WORKDIR /app/backend
COPY ./backend/requirements.txt /app/backend/
RUN pip3 install --upgrade pip -r requirements.txt

# Install JS dependencies
WORKDIR /app/frontend
COPY ./frontend/package.json /app/frontend/
RUN npm install

# Add the rest of the code
COPY . /app/
WORKDIR /app