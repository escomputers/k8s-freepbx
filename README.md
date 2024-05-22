# k8s-freepbx
Run <a href="https://www.freepbx.org">FreePBX</a> (<a href="https://www.asterisk.org">Asterisk</a>) on <a href="https://kubernetes.io">Kubernetes.</a>

Just pure open source power.

## Requirements
- FQDN
- Ability to create type A DNS record for the public IP address allocated by the cloud provider

This PoC is based on <a href="https://www.vultr.com/?ref=9460695">Vultr Kubernetes Engine</a>

## Database deployment
Freepbx requires <a href="https://www.mysql.com">MySql</a> or <a href="https://mariadb.org">MariaDb</a>

A statefulset of 3 replicas (adjust replicas number according to your needs) with one pod for WRITE operations and the others for READ ops.
1. Create Namespace and ConfigMap
```bash
kubectl apply -f mysql/namespace.yaml
kubectl apply -f mysql/configmap.yaml
```

2. Create services
```bash
kubectl apply -f mysql/services.yaml
```

3. Deploy
```bash
kubectl apply -f mysql/statefulset.yaml
```

4. Test connection with READ operation
```
kubectl run mysql-client --image=mysql:5.7 -i -t --rm --restart=Never -- mysql -h mysql-read -e "SHOW DATABASES;"
```

or
```
kubectl run mysql-client-loop --image=mysql:5.7 -i -t --rm --restart=Never --\
  bash -ic "while sleep 1; do mysql -h mysql-read -e 'SELECT @@server_id,NOW()'; done"
```


## Freebpx deployment
1.
```

```

## Exposing services
1. Deploy <a href="https://github.com/kubernetes/ingress-nginx">nginx-controller</a> (read cloud provider docs to check features, in most cases a public IP address will be automatically allocated to it)

### TLS (optional but recommended)
This step uses HTTP-01 challenge with <a href="https://letsencrypt.org">Letsencrypt</a> as `ClusterIssuer`.

1. Install <a href="https://github.com/cert-manager/cert-manager">cert-manager</a> for managing TLS certificates
```bash
kubectl apply -f cert-manager/install-v1.12.0.yaml
```

2. Deploy Letsencrypt, before applying, change `email` field within the yaml
```bash
kubectl apply -f letsencrypt/clusterissuer.yaml
```

### KUARD test (optional)
1. Expose and deploy <a href="https://github.com/kubernetes-up-and-running/kuard">KUARD</a> to test networking functionality (keep order)
```bash
kubectl apply -f kuard/service.yaml
kubectl apply -f kuard/deployment.yaml
```

2. Check if web server within the pod is running
```bash
# PLAIN HTTP
kubectl run curl-client --image=curlimages/curl:8.1.0 -i -t --rm --restart=Never -- http://<PODIP>:8080
```

3. Expose services by creating `Ingress`. Before applying, change `hosts` and `host` field in ingress-tls.yaml if you want TLS or `host` field in ingress.yaml (no TLS), by inserting your FQDN
```bash
# NO TLS
kubectl apply -f kuard/ingress.yaml

# WITH TLS
kubectl apply -f kuard/ingress-tls.yaml
```

4. Check from outside
```bash
Open http://YOURFQDN or https://YOURFQDN
```