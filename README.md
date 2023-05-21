# k8s-freepbx
Run <a href="https://www.freepbx.org">FreePBX</a> (<a href="https://www.asterisk.org">Asterisk</a>) on <a href="https://kubernetes.io">Kubernetes.</a>

Just pure open source power.

## Requirements
- FQDN
- Ability to create type A DNS record for FQDN, by inserting public IP address allocated by your cloud provider.

## Storage
This PoC uses <a href="https://www.vultr.com/?ref=9460695">Vultr block storage.</a>

1. Create secret to connect to Vultr API, by changing `api-key` field by inserting your Vultr Personal Access Token, within the yaml and then run
```
kubectl create -f storage/vultr_csi/secret.yaml
```

2. Install CSI driver in order to create a new default `StorageClass` for dynamic volumes provisioning
```
kubectl apply -f storage/vultr_csi/install_csi-v0.9.0.yaml
```

3. Check if `StorageClass` have been created successfully
```
kubectl get storageclass
```

## Database deployment
Freepbx requires <a href="https://www.mysql.com">MySql</a> or <a href="https://mariadb.org">MariaDb</a>

A statefulset of 3 replicas with one pod for WRITE operations and the others for READ ops.
1. Create ConfigMap
```
kubectl apply -f mysql/configmap.yaml
```

2. Create services
```
kubectl apply -f mysql/services.yaml
```

3. Deploy
```
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
TODO

```

```

## Exposing services
1. Deploy <a href="https://github.com/kubernetes/ingress-nginx">nginx-controller</a> (read cloud provider docs to check features, in most cases a public IP address will be automatically allocated to it)
```
kubectl apply -f ingress/nginx-ingress-controller.yaml
```

2. Validate `IngressClass`
```
kubectl get ingressclass
```

### TLS (optional but recommended)
This step uses HTTP-01 challenge with <a href="https://letsencrypt.org">Letsencrypt</a> as `ClusterIssuer`.

1. Install <a href="https://github.com/cert-manager/cert-manager">cert-manager</a> for managing TLS certificates
```
kubectl apply -f cert-manager/install-v1.12.0.yaml
```

2. Deploy Letsencrypt, before applying, change `email` field within the yaml
```
kubectl apply -f letsencrypt/clusterissuer.yaml
```

### KUARD test (optional)
1. Expose and deploy <a href="https://github.com/kubernetes-up-and-running/kuard">KUARD</a> to test nginx-controller (keep order)
```
kubectl apply -f kuard/service.yaml
kubectl apply -f kuard/deployment.yaml
```

2. Check if web server within the pod is running
```
# PLAIN HTTP
kubectl run curl-client --image=curlimages/curl:8.1.0 -i -t --rm --restart=Never -- http://<PODIP>:8080
```

3. Expose services by creating `Ingress`. Before applying, change `hosts` and `host` field in ingress-tls.yaml if you want TLS or `host` field in ingress.yaml (no TLS), by inserting your FQDN
```
# NO TLS
kubectl apply -f kuard/ingress.yaml

# WITH TLS
kubectl apply -f kuard/ingress-tls.yaml
```

4. Check from outside
```
Open http://YOURFQDN or https://YOURFQDN
```