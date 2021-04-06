#!/usr/bin/env bash
kubectl apply -f docker-hub-credentials.yml
kubectl apply -f keys.yml
kubectl apply -f web-deployment.yml
kubectl apply -f web-service.yml