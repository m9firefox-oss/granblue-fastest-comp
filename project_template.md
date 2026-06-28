# Project Template

## 1. Architecture

```
app/
├── api/            # I/O only (FastAPI)
├── service/        # business logic orchestration
├── domain/         # data + behavior (core logic)
├── infra/          # external dependencies (DB, files)
└── local/          # local assets (images, configs)
```

---

## 2. Coding Principles

- Put logic inside class methods.
- Move logic to classes that own the data.
- Do not write business logic in API/UI/test.
- Keep methods short and single-responsibility.
- Methods must use instance variables.
- Split classes when responsibilities grow.
- Organize classes by package.

---

## 3. API Specification Template

### Endpoint
`POST /resource/action`

### Request
| field | type | description |
|-------|------|-------------|
| file/body | image/* or JSON | input data |

### Response
```json
{
  "result": "...",
  "meta": {}
}
```

### Error
```json
{
  "error": "message",
  "code": 400
}
```

---

## 4. Domain Model Template

### Value Object
```python
class ResourceData:
    raw: bytes
    def to_json(self): ...
```

### Domain Model
```python
class Resource:
    name: str
    attributes: dict
    def calculate(self): ...
```

### Service Layer
```python
class ResourceService:
    def execute(self, data): ...
```

---

## 5. Glossary

| term | definition |
|------|------------|
| domain | core business concept |
| service | logic combining domains |
| API | input/output layer |
| value object | immutable data class |
| infra | external dependency |

---

## 6. Image Processing Requirements

- Preprocessing: grayscale, resize, contrast adjustment.
- Feature extraction: ORB / SIFT / SURF.
- Matching: BFMatcher.
- Unicode normalization: NFC.

---

## 7. Development Phases

### Phase 1 — Foundation
- directory structure  
- domain/service/api skeleton  
- test environment  

### Phase 2 — Core Logic
- domain models  
- service logic  
- API implementation  

### Phase 3 — Processing
- preprocessing  
- feature extraction  
- matching  
- evaluation  

### Phase 4 — UI Integration
- Bubble/Web  
- API connection  

### Phase 5 — Optimization
- logging  
- error handling  
- performance tuning  

---

## 8. Reusable Prompt

```
Use strict OOP principles:
- business logic in classes
- API must be thin
- service layer handles workflows
- domain layer holds data + behavior
- no procedural logic in API/UI/test
- split classes when responsibilities grow
- use NFC normalization for filenames
Generate code following this architecture.
```

