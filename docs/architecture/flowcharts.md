# 🔄 Voice CBT - System Flowcharts

## 1. High-Level System Architecture Flow

```mermaid
graph TB
    subgraph "Client Layer"
        A[User Interface] --> B[Voice Recording]
        B --> C[Audio Processing]
    end
    
    subgraph "API Gateway"
        D[FastAPI Backend] --> E[Authentication]
        E --> F[Rate Limiting]
        F --> G[Security Middleware]
    end
    
    subgraph "Core Services"
        H[Speech-to-Text] --> I[Emotion Detection]
        I --> J[RAG Generator]
        J --> K[Response Validation]
    end
    
    subgraph "Data Layer"
        L[PostgreSQL] --> M[ClickHouse]
        M --> N[ChromaDB]
    end
    
    subgraph "Monitoring"
        O[Prometheus] --> P[Grafana]
    end
    
    C --> D
    G --> H
    K --> L
    D --> O
```

## 2. User Journey Flow

```mermaid
flowchart TD
    A[User Visits App] --> B{First Time?}
    B -->|Yes| C[Onboarding Process]
    B -->|No| D[Login]
    
    C --> E[Complete Profile]
    E --> F[Set Preferences]
    F --> G[Start First Session]
    
    D --> H[Dashboard]
    H --> I[Start New Session]
    
    G --> J[Voice Recording]
    I --> J
    
    J --> K[Audio Processing]
    K --> L[Emotion Detection]
    L --> M[Generate Response]
    M --> N[Display Response]
    
    N --> O{Continue Session?}
    O -->|Yes| J
    O -->|No| P[End Session]
    
    P --> Q[Save Session Data]
    Q --> R[Update Analytics]
    R --> H
```

## 3. Audio Processing Pipeline

```mermaid
flowchart LR
    A[Audio Input] --> B[Preprocessing]
    B --> C[Noise Reduction]
    C --> D[Audio Enhancement]
    D --> E[Speech-to-Text]
    E --> F[Text Processing]
    F --> G[Emotion Analysis]
    G --> H[Context Extraction]
    H --> I[RAG Retrieval]
    I --> J[Response Generation]
    J --> K[Response Validation]
    K --> L[Audio Output]
```

## 4. Database Interaction Flow

```mermaid
graph TB
    subgraph "Application Layer"
        A[API Request] --> B[Authentication]
        B --> C[Business Logic]
    end
    
    subgraph "Data Access Layer"
        C --> D[Database Service]
        D --> E[ORM Layer]
    end
    
    subgraph "Database Layer"
        E --> F[PostgreSQL<br/>Primary Data]
        E --> G[ClickHouse<br/>Analytics]
        E --> H[ChromaDB<br/>Vectors]
    end
    
    subgraph "Caching Layer"
        I[Redis Cache] --> J[Session Data]
        I --> K[Response Cache]
    end
    
    D --> I
    F --> L[Data Replication]
    L --> G
```

## 5. Security Flow

```mermaid
flowchart TD
    A[Incoming Request] --> B[IP Validation]
    B --> C{Rate Limit OK?}
    C -->|No| D[Block Request]
    C -->|Yes| E[Authentication]
    
    E --> F{Valid Token?}
    F -->|No| G[Return 401]
    F -->|Yes| H[Authorization Check]
    
    H --> I{Has Permission?}
    I -->|No| J[Return 403]
    I -->|Yes| K[Input Validation]
    
    K --> L{Input Valid?}
    L -->|No| M[Return 400]
    L -->|Yes| N[Process Request]
    
    N --> O[Log Activity]
    O --> P[Return Response]
```

## 6. Monitoring and Analytics Flow

```mermaid
graph TB
    subgraph "Application Metrics"
        A[User Interactions] --> B[Session Data]
        C[System Performance] --> D[Resource Usage]
        E[Error Events] --> F[Error Tracking]
    end
    
    subgraph "Data Collection"
        B --> G[Prometheus Metrics]
        D --> G
        F --> G
        G --> H[Time Series DB]
    end
    
    subgraph "Visualization"
        H --> I[Grafana Dashboards]
        I --> J[Real-time Monitoring]
        I --> K[Historical Analysis]
    end
    
    subgraph "Alerting"
        J --> L[Threshold Checks]
        L --> M[Alert Generation]
        M --> N[Notification System]
    end
```

## 7. AI Model Pipeline Flow

```mermaid
flowchart TD
    A[Audio Input] --> B[Feature Extraction]
    B --> C[Audio Emotion Model]
    C --> D[Audio Predictions]
    
    E[Text Input] --> F[Text Preprocessing]
    F --> G[Text Emotion Model]
    G --> H[Text Predictions]
    
    D --> I[Fusion Network]
    H --> I
    I --> J[Combined Predictions]
    
    J --> K[Context Analysis]
    K --> L[Knowledge Retrieval]
    L --> M[RAG Generation]
    M --> N[Response Validation]
    N --> O[Therapeutic Response]
```

## 8. Deployment Flow

```mermaid
flowchart LR
    A[Code Commit] --> B[GitHub Actions]
    B --> C[Run Tests]
    C --> D{Tests Pass?}
    D -->|No| E[Deploy Failed]
    D -->|Yes| F[Build Images]
    
    F --> G[Push to Registry]
    G --> H[Deploy to Staging]
    H --> I[Integration Tests]
    I --> J{Staging OK?}
    J -->|No| K[Rollback]
    J -->|Yes| L[Deploy to Production]
    
    L --> M[Health Checks]
    M --> N{Health OK?}
    N -->|No| O[Auto Rollback]
    N -->|Yes| P[Deployment Success]
```

## 9. Error Handling Flow

```mermaid
flowchart TD
    A[Error Occurs] --> B[Error Classification]
    B --> C{Error Type?}
    
    C -->|System Error| D[Log to Database]
    C -->|User Error| E[Return User Message]
    C -->|Security Error| F[Block IP & Alert]
    
    D --> G[Send Alert]
    E --> H[Continue Processing]
    F --> I[Security Log]
    
    G --> J[Monitor Dashboard]
    H --> K[User Feedback]
    I --> L[Admin Notification]
```

## 10. Data Flow Architecture

```mermaid
graph TB
    subgraph "Input Sources"
        A[Voice Input] --> B[Audio Processing]
        C[User Input] --> D[Text Processing]
        E[System Events] --> F[Event Processing]
    end
    
    subgraph "Processing Layer"
        B --> G[STT Service]
        D --> H[NLP Service]
        F --> I[Event Service]
    end
    
    subgraph "AI Layer"
        G --> J[Emotion Detection]
        H --> J
        J --> K[RAG Generation]
    end
    
    subgraph "Storage Layer"
        K --> L[PostgreSQL]
        L --> M[ClickHouse]
        K --> N[ChromaDB]
    end
    
    subgraph "Output Layer"
        L --> O[User Interface]
        M --> P[Analytics Dashboard]
        N --> Q[Knowledge Base]
    end
```
