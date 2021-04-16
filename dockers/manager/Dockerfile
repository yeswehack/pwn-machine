FROM node:15.10.0 as build-front
WORKDIR /app
COPY front/package*.json ./
RUN yarn install
COPY front/ ./
RUN yarn build



FROM python:3.9
WORKDIR /usr/src/app
RUN pip install --upgrade pip poetry
COPY back/pyproject.toml ./
RUN poetry install
COPY back/ ./
COPY --from=build-front /app/dist/spa/ static/
CMD poetry run uvicorn --host 0.0.0.0 --port 5000 main:app
