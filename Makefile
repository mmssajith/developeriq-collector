# Makefile
IMAGE_TAG ?= 3.0.0
ECR_REGISTRY ?= 337689099048.dkr.ecr.ap-southeast-1.amazonaws.com
ECR_REPOSITORY ?= developeriq_be
K8S_NAMESPACE ?= developeriq

.PHONY: deploy
deploy:
	kubectl apply -f deployment.yaml --namespace=$(K8S_NAMESPACE)

.PHONY: delete
delete:
	kubectl delete -f deployment.yaml --namespace=$(K8S_NAMESPACE)

.PHONY: build-and-push
build-and-push:
	docker build -t $(ECR_REGISTRY)/$(ECR_REPOSITORY):$(IMAGE_TAG) .
	docker push $(ECR_REGISTRY)/$(ECR_REPOSITORY):$(IMAGE_TAG)
