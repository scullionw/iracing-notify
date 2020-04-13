FROM node AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm i
COPY ./public /app/public
COPY ./src /app/src
RUN npm run build

FROM nginx
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/build /usr/share/nginx/html