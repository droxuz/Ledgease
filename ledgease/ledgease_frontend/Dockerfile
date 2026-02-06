FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json .
COPY package-lock.json .
RUN npm install

# Copy Project
COPY . .

# Expose Port
EXPOSE 5173

# Run command
CMD [ "npm", "run", "dev", "--", "--host"]

