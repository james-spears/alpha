### STAGE 1: build the production ###

# We label our stage as ‘builder’
FROM node:10 as builder

COPY package.json package-lock.json ./

## Storing node modules on a separate layer will prevent unnecessary npm installs at each build

# RUN apk --no-cache add --virtual native-deps \
#   g++ gcc libgcc libstdc++ linux-headers make python && \
#   npm install --quiet node-gyp -g &&\
#   npm install --quiet && \
RUN npm ci && mkdir /ng-app && mv ./node_modules ./ng-app
#   apk del native-deps 

WORKDIR /ng-app

COPY . .

## Build the angular app in production mode and store the artifacts in dist folder

RUN npm run ng build -- --prod --aot --output-path=dist

### STAGE 2: Setup production layer ###

FROM nginx:1.14.1-alpine

## Copy our default nginx config
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./nginx/static /static
# Uncomment below to use detectify
# COPY ./nginx/4ca47bf08d2e04ae37030073552a27c8.txt 4ca47bf08d2e04ae37030073552a27c8.txt

## Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

## From ‘builder’ stage copy over the artifacts in dist folder to default nginx public folder
COPY --from=builder /ng-app/dist /usr/share/nginx/html

# EXPOSE 4200
CMD ["nginx", "-g", "daemon off;"]