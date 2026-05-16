# Requirements — Todo Priority Filtering

## REQ-1: Priority Field on Todo Entity

The Todo entity MUST expose a `priority` field with values `HIGH`, `MEDIUM`, `LOW`.

### AC-1.1
**Given** a new Todo is created without specifying priority
**When** the response is returned
**Then** `priority` equals `"MEDIUM"`

### AC-1.2
**Given** a new Todo is created with `priority: "HIGH"`
**When** the response is returned
**Then** `priority` equals `"HIGH"`

### AC-1.3
**Given** a request to create a Todo with `priority: "INVALID"`
**When** the API processes the request
**Then** the response status is `422 Unprocessable Entity`

---

## REQ-2: Filter Todos by Priority

`GET /todos` MUST accept an optional `?priority=` query parameter.

### AC-2.1
**Given** three Todos exist with priorities HIGH, MEDIUM, LOW
**When** `GET /todos?priority=HIGH` is called
**Then** only the HIGH-priority Todo is returned

### AC-2.2
**Given** three Todos exist with priorities HIGH, MEDIUM, LOW
**When** `GET /todos` is called without `?priority=`
**Then** all three Todos are returned

### AC-2.3
**Given** `GET /todos?priority=INVALID` is called
**Then** response status is `422 Unprocessable Entity`

---

## REQ-3: Update Priority via PATCH

`PATCH /todos/{id}` MUST accept an optional `priority` field.

### AC-3.1
**Given** a Todo with priority `LOW`
**When** `PATCH /todos/{id}` with `{"priority": "HIGH"}` is sent
**Then** the Todo's priority is updated to `HIGH` and returned in the response

---

## Test Coverage Map

| REQ | AC | Test Target |
|---|---|---|
| REQ-1 | AC-1.1 | unit: domain/todo entity default priority |
| REQ-1 | AC-1.2 | unit: domain/todo entity explicit priority |
| REQ-1 | AC-1.3 | integration: POST /todos with invalid priority |
| REQ-2 | AC-2.1 | integration: GET /todos?priority=HIGH |
| REQ-2 | AC-2.2 | integration: GET /todos (no filter) |
| REQ-2 | AC-2.3 | integration: GET /todos?priority=INVALID |
| REQ-3 | AC-3.1 | integration: PATCH /todos/{id} priority update |

---

## Scope Contract

**IN**: Priority enum field, creation default, filter query, PATCH update.
**OUT**: Sorting, multi-value filter, notifications.
