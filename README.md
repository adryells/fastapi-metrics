## O básico (ref.: https://opentelemetry.io/docs/languages/python/getting-started/)
instalar lib `opentelemetry-distro` pra rodar os comandos no terminal e instalar as basicas (api e sdk) em uma lapada só

- importante rodar o comando "opentelemetry-bootstrap -a install" após instalar o distro

ao rodar o app fastapi a seguinte variavel deve ser setada:

```export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true```

e então:
```shell
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name dice-server uvicorn main:app
```
com a configuração acima todos os bagulhos aparecerão no terminal, oq eh util mas paia

[OTLP]

não esquecer de instalar a lib:opentelemetry-exporter-otlp

pra passar os bagulhos pra um coletor local tem q por o seguinte codigo no /tmp/otel-collector-config.yaml

```yaml
# /tmp/otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
exporters:
  debug:
    verbosity: detailed
processors:
  batch:
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [debug]
      processors: [batch]
    metrics:
      receivers: [otlp]
      exporters: [debug]
      processors: [batch]
    logs:
      receivers: [otlp]
      exporters: [debug]
      processors: [batch]
```

e então rodar o container:

```shell
docker run -p 4317:4317 \
    -v /tmp/otel-collector-config.yaml:/etc/otel-collector-config.yaml \
    otel/opentelemetry-collector:latest \
    --config=/etc/otel-collector-config.yaml
```

com isso o comando pra rodar o app fica menor pois traces e metricas por padrão vão pro OTLP então não precisa indicar isso:

`opentelemetry-instrument --logs_exporter otlp uvicorn main:app`
