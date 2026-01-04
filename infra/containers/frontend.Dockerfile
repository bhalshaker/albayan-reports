# Use a specific version for consistency
FROM docker.io/library/node:25-alpine

# Set environment to production
ENV NODE_ENV=production

WORKDIR /usr/frontendservice

# Grant ownership of the folder to the node user
RUN chown node:node /usr/frontendservice

# Copy dependency files
COPY --chown=node:node apps/frontendservice/package*.json ./

# Copy source code with correct permissions
COPY --chown=node:node apps/frontendservice/. .

# Switch to the non-root user
USER node

# Use 'npm ci' for faster, reliable builds and only install production deps
RUN npm ci --only=production

EXPOSE 3000

# Start the app directly with node
CMD ["node", "server.js"]