FROM node:16-alpine as common

WORKDIR /usr/src/app
COPY package.json yarn.lock ./
RUN yarn install

FROM common as builder
ADD . ./
RUN yarn build

FROM common
RUN apk update && apk add sqlite
COPY  --from=builder /usr/src/app/dist/ ./
CMD yarn serve
