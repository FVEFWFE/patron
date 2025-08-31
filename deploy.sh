#!/bin/bash

# Dex Volkov Private Content Vault - Deployment Script

set -e

echo "================================================"
echo "   Dex Volkov Private Content Vault Deployer   "
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}This script should not be run as root!${NC}"
   exit 1
fi

# Function to generate secure random string
generate_secret() {
    openssl rand -hex 32
}

# Check for required commands
command -v docker >/dev/null 2>&1 || { echo -e "${RED}Docker is required but not installed. Aborting.${NC}" >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo -e "${RED}Docker Compose is required but not installed. Aborting.${NC}" >&2; exit 1; }

echo -e "${GREEN}✓ Prerequisites checked${NC}"

# Setup environment
echo -e "${YELLOW}Setting up environment...${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env <<EOF
# Dex Volkov Environment Configuration
SECRET_KEY=$(generate_secret)
DATABASE_URL=sqlite:////app/instance/app.db
FLASK_ENV=production
SITEURL=https://vault.example.com
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${YELLOW}! .env file already exists, skipping...${NC}"
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p app/static/videos
mkdir -p app/static/images
mkdir -p instance
mkdir -p ssl

echo -e "${GREEN}✓ Directories created${NC}"

# Generate self-signed SSL certificate (for testing)
if [ ! -f ssl/cert.pem ]; then
    echo -e "${YELLOW}Generating self-signed SSL certificate...${NC}"
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes -subj "/CN=localhost"
    echo -e "${GREEN}✓ SSL certificate generated (self-signed for testing)${NC}"
else
    echo -e "${YELLOW}! SSL certificate already exists, skipping...${NC}"
fi

# Build and start containers
echo -e "${YELLOW}Building Docker containers...${NC}"
docker-compose -f docker-compose.dexvolkov.yml build

echo -e "${YELLOW}Starting services...${NC}"
docker-compose -f docker-compose.dexvolkov.yml up -d

# Wait for services to start
echo -e "${YELLOW}Waiting for services to initialize...${NC}"
sleep 10

# Check if services are running
if docker-compose -f docker-compose.dexvolkov.yml ps | grep -q "Up"; then
    echo -e "${GREEN}✓ Services started successfully${NC}"
else
    echo -e "${RED}✗ Failed to start services${NC}"
    docker-compose -f docker-compose.dexvolkov.yml logs
    exit 1
fi

# Initialize database
echo -e "${YELLOW}Initializing database...${NC}"
docker-compose -f docker-compose.dexvolkov.yml exec -T web flask db init || true
docker-compose -f docker-compose.dexvolkov.yml exec -T web flask db migrate -m "Initial migration" || true
docker-compose -f docker-compose.dexvolkov.yml exec -T web flask db upgrade || true

echo -e "${GREEN}✓ Database initialized${NC}"

# Create admin user
echo -e "${YELLOW}Creating admin user...${NC}"
docker-compose -f docker-compose.dexvolkov.yml exec -T web python << EOF
from app import db, create_app
from app.models import User
import sys

app = create_app()
with app.app_context():
    # Check if admin already exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@dexvolkov.local', role='admin')
        admin.set_password('changeme123!')  # CHANGE THIS PASSWORD!
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully")
    else:
        print("Admin user already exists")
EOF

echo -e "${GREEN}✓ Admin user created (username: admin, password: changeme123!)${NC}"
echo -e "${RED}⚠ IMPORTANT: Change the admin password immediately!${NC}"

# Display status
echo ""
echo "================================================"
echo -e "${GREEN}     Deployment Complete!${NC}"
echo "================================================"
echo ""
echo "Access your vault at:"
echo -e "${YELLOW}  https://localhost${NC} (self-signed cert warning expected)"
echo ""
echo "Admin panel:"
echo -e "${YELLOW}  https://localhost/admin${NC}"
echo ""
echo "Default credentials:"
echo -e "${YELLOW}  Username: admin${NC}"
echo -e "${YELLOW}  Password: changeme123!${NC}"
echo ""
echo -e "${RED}Security Checklist:${NC}"
echo "  1. Change admin password immediately"
echo "  2. Replace self-signed SSL certificate with valid cert"
echo "  3. Update SITEURL in .env file"
echo "  4. Configure firewall rules"
echo "  5. Set up regular backups"
echo "  6. Review and update persona_config.json"
echo ""
echo "To stop services:"
echo -e "${YELLOW}  docker-compose -f docker-compose.dexvolkov.yml down${NC}"
echo ""
echo "To view logs:"
echo -e "${YELLOW}  docker-compose -f docker-compose.dexvolkov.yml logs -f${NC}"
echo ""
echo "================================================"