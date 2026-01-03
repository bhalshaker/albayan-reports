# Use a specific version for consistency
FROM node:25-alpine

# Set environment to production
ENV NODE_ENV=production

WORKDIR /usr/frontendservice

# Grant ownership of the folder to the node user
RUN chown node:node /usr/frontendservice

# Copy dependency files
COPY --chown=node:node package*.json ./

# Use 'npm ci' for faster, reliable builds and only install production deps
RUN npm ci --only=production

# Copy source code with correct permissions
COPY --chown=node:node . .

# Switch to the non-root user
USER node

EXPOSE 3000

# Start the app directly with node
CMD ["node", "server.js"]