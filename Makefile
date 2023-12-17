# Makefile
IMAGE_TAG ?= 2.0.0
ECR_REGISTRY ?= 337689099048.dkr.ecr.ap-southeast-1.amazonaws.com
ECR_REPOSITORY ?= developeriq_be
K8S_NAMESPACE ?= developeriq

.PHONY: deploy
deploy:
	sed 's|{{IMAGE_TAG}}|$(IMAGE_TAG)|;s|{{ECR_REGISTRY}}|$(ECR_REGISTRY)|;s|{{ECR_REPOSITORY}}|$(ECR_REPOSITORY)|;s|{{K8S_NAMESPACE}}|$(K8S_NAMESPACE)|' deployment.yaml | kubectl apply -f -

.PHONY: delete
delete:
	sed 's|{{IMAGE_TAG}}|$(IMAGE_TAG)|;s|{{ECR_REGISTRY}}|$(ECR_REGISTRY)|;s|{{ECR_REPOSITORY}}|$(ECR_REPOSITORY)|;s|{{K8S_NAMESPACE}}|$(K8S_NAMESPACE)|' deployment.yaml | kubectl delete -f -

.PHONY: build-and-push
build-and-push:
	docker build -t $(ECR_REGISTRY)/$(ECR_REPOSITORY):$(IMAGE_TAG) .
	docker push $(ECR_REGISTRY)/$(ECR_REPOSITORY):$(IMAGE_TAG)
