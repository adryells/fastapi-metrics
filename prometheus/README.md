## PROMETHEUS
### Docker command
```shell
docker run --rm -v ${PWD}/prometheus.yml:/prometheus/prometheus.yml -p 9090:9090 prom/prometheus --enable-feature=otlp-write-receive
```
ou configurar um compose:

```shell
version: '3.9'

services:
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/prometheus/prometheus.yml
    command: --enable-feature=otlp-write-receive
    restart: unless-stopped

```

### instale
```shell
pip install opentelemetry-exporter-prometheus
```

## Grafana
### Docker command
```shell
docker run -d \
  --name grafana \
  -p 3000:3000 \
  --env GF_SECURITY_ADMIN_USER=admin \
  --env GF_SECURITY_ADMIN_PASSWORD=admin \
  --restart unless-stopped \
  grafana/grafana
```
ou configurar compose:
```shell
  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin 
      - GF_SECURITY_ADMIN_PASSWORD=admin 
    depends_on:
      - prometheus
    restart: unless-stopped
```