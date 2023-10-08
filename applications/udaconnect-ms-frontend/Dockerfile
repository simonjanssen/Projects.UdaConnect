FROM node:14.8.0-alpine3.12

WORKDIR /home/node/app

COPY package.json ./

COPY package-lock.json ./

RUN npm install \
    && npm install react-scripts@3.4.3 -g

COPY . .

EXPOSE 3000

CMD ["npm", "start"]

