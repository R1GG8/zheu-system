# Система ЖЭУ — Взаимодействие жителей и управляющей компании

## Архитектура проекта

### 1. Use Case Diagram (Диаграмма прецедентов)

```mermaid
---
title: Use Case Diagram - Система ЖЭУ
---

flowchart TD
    %% Актёры
    Resident["Житель"] 
    Admin["Администратор / Диспетчер"] 
    Master["Мастер\n(Сантехник / Электрик)"] 

    %% Система
    subgraph "Система ЖЭУ"
        direction TB
        
        UC1((Авторизация<br>и регистрация))
        UC2((Просмотр<br>новостей))
        UC3((Создать<br>заявку))
        UC4((Просмотр<br>своих заявок))
        UC5((Получать<br>push-уведомления))
        
        UC6((Создать /<br>Опубликовать новость))
        UC7((Просмотр<br>всех заявок))
        UC8((Изменить<br>статус заявки))
        UC9((Назначить<br>исполнителя))
        UC10((Добавить<br>комментарий))
    end

    %% Связи
    Resident --> UC1
    Resident --> UC2
    Resident --> UC3
    Resident --> UC4
    Resident --> UC5

    Admin --> UC1
    Admin --> UC6
    Admin --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC10

    Master --> UC1
    Master --> UC7
    Master --> UC8
    Master --> UC9
    Master --> UC10

    %% Стили (классический PlantUML вид)
    classDef actor fill:#FEF3C7, stroke:#854D0E, stroke-width:3px, color:#000000, font-weight:bold
    classDef usecase fill:#DBEAFE, stroke:#1E40AF, stroke-width:3px, color:#000000
    
    class Resident,Admin,Master actor
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9,UC10 usecase
```
### 2. Class Diagram - Система ЖЭУ

```mermaid
---
title: Class Diagram - Система ЖЭУ
---

classDiagram
    direction TB

    %% ==================== Пользователи ====================
    class User {
        + id : UUID
        + username : String
        + email : String
        + phone : String
        + role : UserRole
        + apartment_number : String
        + full_name : String
        + is_active : Boolean
    }

    class Resident {
        + address : String
    }

    class Employee {
        + position : String
        + department : String
    }

    User <|-- Resident
    User <|-- Employee

    %% ==================== Сущности ====================
    class News {
        + id : UUID
        + title : String
        + content : Text
        + image : ImageField
        + created_at : DateTime
        + is_published : Boolean
    }

    class Application {
        + id : UUID
        + number : String
        + title : String
        + description : Text
        + category : Enum
        + status : Enum
        + priority : Enum
        + created_at : DateTime
        + updated_at : DateTime
    }

    class ApplicationStatusHistory {
        + id : UUID
        + status : Enum
        + comment : String
        + created_at : DateTime
    }

    class Notification {
        + id : UUID
        + title : String
        + message : String
        + type : Enum
        + is_read : Boolean
        + created_at : DateTime
    }

    %% ==================== Связи ====================
    Resident "1" --> "0..*" Application : "создаёт"
    Employee "0..1" --> "0..*" Application : "выполняет"

    Application "1" --> "0..*" ApplicationStatusHistory : "история"
    Application --> "0..*" Notification : "уведомления"
    News --> "0..*" Notification : "уведомления"
    User "1" --> "0..*" Notification : "получает"
```
**Диаграммы являются актуальными на момент последнего обновления. По мере развития проекта они могут обновляться.**