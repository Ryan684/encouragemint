#!/usr/bin/env bash
kubectl apply -f docker-hub-credentials.yaml
kubectl apply -f secrets.yaml
kubectl apply -f api-config.yml
kubectl apply -f api-deployment.yaml
kubectl apply -f api-service.yaml