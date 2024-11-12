# Variables
DOCKER_COMPOSE_FILE = docker-compose.yml
PROJECT_NAME = api_standard
SERVICES = api-gateway push-service customer-service

# Helper function to run docker-compose commands
define dc
	@docker-compose -f $(DOCKER_COMPOSE_FILE) -p $(PROJECT_NAME) $(1)
endef

# Default target
.PHONY: all
all: build up

# Build all services
.PHONY: build
build:
	$(call dc,build)

# Build a specific service
.PHONY: build-service
build-service:
	$(call dc,build $(filter-out $@,$(MAKECMDGOALS)))

# Start all services
.PHONY: up
up:
	$(call dc,up -d)

# Start a specific service
.PHONY: up-service
up-service:
	$(call dc,up -d $(filter-out $@,$(MAKECMDGOALS)))

# Stop all services
.PHONY: down
down:
	$(call dc,down)

# Stop a specific service
.PHONY: down-service
down-service:
	$(call dc,stop $(filter-out $@,$(MAKECMDGOALS)))

# Remove all containers, networks, and volumes
.PHONY: clean
clean: down
	$(call dc,rm -fsv)
	@docker volume prune -f
	@docker network prune -f

# Show logs of all services
.PHONY: logs
logs:
	$(call dc,logs -f)

# Show logs of a specific service
.PHONY: logs-service
logs-service:
	$(call dc,logs -f $(filter-out $@,$(MAKECMDGOALS)))

# Restart all services
.PHONY: restart
restart: down up

# Restart a specific service
.PHONY: restart-service
restart-service:
	$(call dc,stop $(filter-out $@,$(MAKECMDGOALS)))
	$(call dc,up -d $(filter-out $@,$(MAKECMDGOALS)))

# Scale services (e.g., make scale-service service=api-gateway replicas=3)
.PHONY: scale-service
scale-service:
	$(call dc,up -d --scale $(service)=$(replicas))

# Status of all services
.PHONY: status
status:
	$(call dc,ps)

# Attach to a specific service (e.g., make attach-service service=api-gateway)
.PHONY: attach-service
attach-service:
	@docker attach $(PROJECT_NAME)_$(filter-out $@,$(MAKECMDGOALS))

# Deploy (build and start services)
.PHONY: deploy
deploy: clean build up
