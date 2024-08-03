# Use the official Node.js base image
FROM node:latest

# Set the working directory in the container
WORKDIR /code/frontend

# Copy package.json and package-lock.json first to leverage Docker cache
COPY ./frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY ./frontend .

# Build the application
#RUN npm run build

# Expose the port that the app runs on
EXPOSE 3000

# Start the Next.js application
#CMD ["npm", "run", "dev"]
