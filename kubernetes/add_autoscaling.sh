#!/usr/bin/env bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl apply -f horizontal_autoscaler.yaml