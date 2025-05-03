# Контракты GRPC

---

### Пример для генерации

```bash
python -m grpc_tools.protoc -I. --python_out=. --mypy_out=. --grpc_python_out=. protos/user_service/user_service.proto
```

---