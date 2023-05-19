# k8s-freepbx

## Storage
This PoC uses <a href="https://www.vultr.com/?ref=9460695" target="_blank">Vultr block storage.</a>

1. Create secret to connect to Vultr API, by changing your Personal Access Token within the yaml and then run:
```
kubectl create -f storage/vultr_csi/secret.yaml
```

2. Install CSI driver in order to create a new StorageClass
```
kubectl apply -f storage/vultr_csi/install_csi-v0.9.0.yaml
```

3. Check if StorageClass has been created successfully
```
kubectl get storageclass
```

## Database deployment
Freepbx requires MySql/MariaDb

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

4. Test connection
```
kubectl run mysql-client --image=mysql:5.7 -i -t --rm --restart=Never -- mysql -h mysql-read -e "SHOW DATABASES;"
```

or
```
kubectl run mysql-client-loop --image=mysql:5.7 -i -t --rm --restart=Never --\
  bash -ic "while sleep 1; do mysql -h mysql-read -e 'SELECT @@server_id,NOW()'; done"
```


## Freebpx deployment
1. Create PersistenVolumeClaim
```
kubectl create -f freepbx/pvc.yml
```