FROM node:15.10.0 as build-front
WORKDIR /app
COPY front/package.json ./
COPY front/yarn.lock ./
RUN yarn install
COPY front/ ./
RUN yarn build



FROM python:3.9
WORKDIR /usr/src/app
RUN apt update && apt install -y docker.io
RUN pip install --upgrade pip poetry
COPY back/pyproject.toml ./
COPY back/poetry.lock ./
RUN poetry install
COPY back/ ./
COPY --from=build-front /app/dist/spa/ static/
EXPOSE 5000/tcp
CMD poetry run uvicorn --host 0.0.0.0 --port 5000 --log-level warning app:app ; sleep 9000000
