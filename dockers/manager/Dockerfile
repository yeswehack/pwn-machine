FROM node:15.10.0 as build-front
WORKDIR /app
COPY front/package*.json ./
RUN yarn install
COPY front/ ./
RUN yarn build



FROM python:3.9
WORKDIR /usr/src/app
RUN pip install --upgrade pip poetry
COPY api/pyproject.toml ./
RUN poetry install
COPY api/ ./
COPY --from=build-front /app/dist/spa/ static/
CMD poetry run gunicorn --bind 0.0.0.0:5000 main:app
