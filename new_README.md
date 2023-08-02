# k8s-freepbx
Run <a href="https://www.freepbx.org">FreePBX</a> (<a href="https://www.asterisk.org">Asterisk</a>) on <a href="https://kubernetes.io">Kubernetes.</a>

Just pure open source power.

## Requirements
- FQDN
- VoIP SIP trunk/trunks (DID/DIDs)
- Ability to create type A DNS record for FQDN, by inserting public IP address allocated by your cloud provider.

### Create namespaces
```bash
kubectl apply -f namespaces.yaml
```

### Mysql setup
```bash
# for minikube
kubectl apply -f mysql/minikube-pvc.yaml
# or in case of Vultr block storage
kubectl apply -f mysql/pvc.yaml
kubectl apply -f mysql/pv.yaml

# then
kubectl apply -f mysql/configmap.yaml
kubectl apply -f mysql/services.yaml

# minikube
kubectl apply -f mysql/minikube-statefulset.yaml

# Vultr
kubectl apply -f mysql/statefulset.yaml
```
