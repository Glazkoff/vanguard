# Stage 1 - build frontend app
# FROM node:10-alpine as build-deps

# WORKDIR /app/

# COPY frontend/package.json frontend/package-lock.json /app/
# RUN npm install

# COPY frontend /app/
# COPY .env /app/.env
# RUN npm run build

# Stage 2 - nginx & frontend dist
FROM nginx:1.25.3-alpine3.18

COPY nginx/prod.conf /etc/nginx/nginx.conf
COPY nginx/favicon/* /var/www/favicon/
# COPY --from=build-deps /app/dist/ /dist/

CMD ["nginx", "-g", "daemon off;"]