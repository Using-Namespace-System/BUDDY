# Step 1: Use the official Node.js image as a base
FROM node:18 AS build

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy package.json and package-lock.json (to take advantage of Docker's caching)
COPY package.json package-lock.json ./

# Step 4: Install dependencies
RUN npm install

# Step 5: Copy the rest of the app's source code
COPY . .

# Step 6: Build the React app for production
RUN npm run build

# Step 7: Use Nginx to serve the React app (production-ready)
FROM nginx:alpine

# Step 8: Copy the build output from the previous image to Nginx's HTML folder
COPY --from=build /app/build /usr/share/nginx/html

# Step 9: Expose the port for the Nginx server
EXPOSE 80

# Step 10: Start Nginx when the container is run
CMD ["nginx", "-g", "daemon off;"]
