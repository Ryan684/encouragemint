#!/usr/bin/env bash
kubectl apply -f docker-hub-credentials.yml
kubectl apply -f keys.yml
kubectl apply -f database-persistent-volume.yml
kubectl apply -f database-persistent-volume-claim.yml
kubectl apply -f database-deployment.yml
kubectl apply -f database-service.yml
kubectl apply -f broker-deployment.yml
kubectl apply -f broker-service.yml
kubectl apply -f web-deployment.yml
kubectl apply -f worker-deployment.yml
kubectl apply -f web-service.yml