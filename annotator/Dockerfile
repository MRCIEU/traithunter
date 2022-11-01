# -*- mode: dockerfile -*-
# build stage
FROM node:12.2.0-alpine as build-stage
RUN apk add --no-cache git
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build

# production stage
FROM nginx:1.16.0-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
