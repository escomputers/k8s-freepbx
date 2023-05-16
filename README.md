# k8s-freepbx
 This PoC is based on Vultr Kubernetes Engine.

## Storage
1. Create a block storage via Vultr dashboard.

2. Attach Vultr Block Storage with Kubernetes CSI driver

Change your Personal Access Token within the yaml and then run:
```
kubectl create -f storage/vultr_csi/secret.yaml
```

3. Install CSI driver in order to create a new StorageClass
```
kubectl apply -f storage/vultr_csi/install_csi-v0.9.0.yaml
```

4. Check if StorageClass has been created successfully
```
kubectl get storageclass
```

## Database deployment
Freepbx requires MySql/MariaDb

1. Create PersistentVolumeClaim and Persistent Volume
```
kubectl create -f mysql/pvc.yml
kubectl create -f mysql/pv.yml
```

2. Create ConfigMap
```
kubectl apply -f mysql/configmap.yaml
```

3. Create services
```
kubectl apply -f mysql/services.yaml
```

3. Create secret:
```
kubectl create secret generic mysql-password --from-literal=password=YOURPASSWORD
```

4. Deploy
```
kubectl apply -f mysql/statefulset.yaml
```

## Freebpx deployment
1. Create PersistenVolumeClaim
```
kubectl create -f freepbx/pvc.yml
```