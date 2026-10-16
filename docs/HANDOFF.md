# SOC Platform

## Project Overview 1

The SOC Platform is a production-quality Security Operations Center (SOC) simulation built in Python. Rather than focusing on a simple CRUD application or isolated security tools, the project models the complete lifecycle of security event processing as it occurs within a modern Security Operations Center.

The platform accepts normalized security events, applies detection logic, enriches events with additional context, correlates related activity, generates alerts, creates investigation cases, persists operational data, and exposes the system through a REST API.

The primary objective is not only to build a functioning application, but to demonstrate software engineering practices suitable for large, maintainable systems. Every component is designed to emphasize clear separation of responsibilities, extensibility, strong domain modeling, and long-term maintainability.

The architecture intentionally follows enterprise software design principles including Domain-Driven Design (DDD), Clean Architecture, and Hexagonal Architecture. Business logic remains independent of infrastructure concerns, allowing persistence technologies, APIs, and external integrations to evolve without affecting the core domain.

The long-term vision is a modular SOC platform capable of supporting additional detection rules, enrichment providers, correlation logic, alerting strategies, case management workflows, threat intelligence integrations, and multiple persistence backends while maintaining a stable and testable architecture.         


# Project Goals 2

## Primary Goal

The primary objective of the SOC Platform is to build a production-quality Security Operations Center (SOC) backend that models the complete security investigation lifecycle while demonstrating modern software engineering principles.

The project is intended to serve both as a realistic security application and as a long-term software engineering portfolio project.

## Technical Objectives

The platform is designed to achieve the following objectives:

- Model the end-to-end processing of security events from ingestion through case creation.
- Maintain a clear separation between business logic, application services, infrastructure, and external interfaces.
- Follow Domain-Driven Design (DDD), Clean Architecture, and Hexagonal Architecture.
- Build highly cohesive, loosely coupled components that can evolve independently.
- Support future expansion without requiring architectural redesign.
- Emphasize strong typing and rich domain models over generic dictionaries and metadata.
- Keep business rules isolated from orchestration logic.
- Ensure infrastructure components can be replaced without affecting the domain layer.
- Achieve comprehensive automated test coverage across the application.

## Architectural Goals

The architecture is intentionally designed so that:

- Engines coordinate workflows rather than implement business rules.
- Rules perform a single business operation.
- Processors perform one post-processing responsibility.
- Application services orchestrate use cases without containing business logic.
- Repositories abstract persistence from the domain model.
- The Unit of Work manages transactional consistency.
- Infrastructure dependencies remain isolated from the core business domain.

## Long-Term Vision

The current implementation represents the foundation of a modular SOC platform capable of supporting future enhancements, including:

- Additional event sources and normalization pipelines.
- Expanded detection and correlation rule libraries.
- Threat intelligence integrations.
- Advanced enrichment providers.
- Multiple persistence backends.
- Authentication and authorization.
- Dashboards and operational metrics.
- AI-assisted investigations and analyst workflows.
- Horizontal scalability and distributed processing.

Every architectural decision should support these long-term goals while preserving maintainability, extensibility, and testability.


# Design Principles 3

The SOC Platform is designed around a set of architectural principles intended to maximize maintainability, extensibility, testability, and separation of concerns. Every module within the system follows these principles.

## Domain-Driven Design (DDD)

The domain model represents the core of the application. Business concepts such as Events, Detections, Correlations, Alerts, and Cases are modeled as rich domain objects rather than simple data containers.

Business rules operate on these domain models while remaining independent of infrastructure, APIs, and persistence technologies.

## Clean Architecture

The application follows Clean Architecture by organizing code into layers with one-way dependencies.

The dependency direction always points toward the domain.

```
API
    ↓
Application
    ↓
Domain
    ↑
Infrastructure
```

Business logic never depends on frameworks, databases, or external services.

## Hexagonal Architecture

Infrastructure components are treated as interchangeable adapters connected through interfaces.

Repositories, databases, APIs, message queues, and external integrations communicate with the application through well-defined ports, allowing implementations to be replaced without affecting business logic.

## Separation of Responsibilities

Each component has a single, clearly defined responsibility.

### Engines

Engines coordinate workflows.

They do not contain business rules.

Examples include:

- DetectionEngine
- EnrichmentEngine
- CorrelationEngine
- AlertEngine
- AlertProcessingEngine
- CaseProcessingEngine

Their responsibility is to execute registered components in the correct order.

### Rules

Rules perform a single business operation.

Each rule determines one specific security condition and returns its results without knowledge of other rules.

Examples include:

- FailedLoginRule
- FailedLoginBurstRule
- ImpossibleTravelRule
- ImmediateDetectionAlertRule
- CorrelationAlertRule

Rules remain small, focused, and independently testable.

### Processors

Processors perform one post-processing responsibility after domain objects have been created.

Examples include:

- DeduplicationProcessor
- AlertGroupingProcessor
- AlertRoutingProcessor
- CaseAssignmentProcessor
- CaseSLAProcessor
- CaseSLABreachProcessor
- CaseEscalationProcessor

Each processor performs exactly one operation.

## Rich Domain Models

The platform favors explicit domain models with strongly typed fields over generic dictionaries whenever practical.

Objects validate themselves using Pydantic models, reducing invalid application state and improving readability.

## Dependency Injection

Application services receive their dependencies through constructor injection rather than creating them internally.

This approach improves modularity, simplifies testing, and allows implementations to be replaced without modifying business logic.

## Repository Pattern

Persistence is abstracted through repository interfaces.

Application services never interact directly with SQLite or any database implementation.

Repositories provide a stable abstraction that allows future migration to PostgreSQL or other storage technologies with minimal impact on the application layer.

## Unit of Work Pattern

Database operations are coordinated through a Unit of Work.

A Unit of Work defines the transactional boundary for each application use case by:

- Managing repository instances
- Coordinating database transactions
- Committing successful operations
- Rolling back failed operations

This ensures consistency across multiple repository operations.

## Strong Typing

The project emphasizes explicit types throughout the codebase.

Enums, domain models, request/response DTOs, and repository interfaces are preferred over loosely typed structures to improve correctness, readability, and maintainability.

## Testability

Every business component is designed to be independently testable.

Business rules are isolated from infrastructure, enabling fast unit tests.

Application services are tested using repository abstractions and temporary SQLite databases.

The REST API is validated through integration tests using FastAPI's TestClient.

## Extensibility

The architecture is intentionally open for extension while remaining closed for modification.

New detection rules, enrichers, correlation rules, alert rules, processors, repositories, or persistence implementations can be introduced with minimal changes to existing code.

This design allows the SOC Platform to grow incrementally without requiring major architectural refactoring.


# High-Level Architecture 4

The SOC Platform is organized into multiple architectural layers, each with a clearly defined responsibility. Dependencies always flow toward the core business domain, ensuring that business logic remains independent of infrastructure and external technologies.

## Architectural Layers

```text
                            +----------------------+
                            |      REST API        |
                            |      (FastAPI)       |
                            +----------+-----------+
                                       |
                                       v
                            +----------------------+
                            |  Application Layer   |
                            |   Application        |
                            |   Services & DTOs    |
                            +----------+-----------+
                                       |
                                       v
+--------------------------------------------------------------------+
|                           Domain Layer                             |
|                                                                    |
|  Normalization                                                     |
|       ↓                                                            |
|  Detection Engine                                                  |
|       ↓                                                            |
|  Enrichment Engine                                                 |
|       ↓                                                            |
|  Correlation Engine                                                |
|       ↓                                                            |
|  Alert Engine                                                      |
|       ↓                                                            |
|  Alert Processing                                                  |
|       ↓                                                            |
|  Case Factory                                                      |
|       ↓                                                            |
|  Case Processing                                                   |
+--------------------------+-----------------------------------------+
                           |
                           v
                 +----------------------+
                 | Persistence Layer    |
                 | Repositories         |
                 | Unit of Work         |
                 | SQLite               |
                 +----------------------+
```

## API Layer

The REST API exposes the functionality of the platform through FastAPI.

Responsibilities include:

- Receiving HTTP requests
- Validating request models
- Calling application services
- Returning response models
- Converting domain exceptions into HTTP responses

The API layer contains no business logic.

## Application Layer

The application layer coordinates use cases.

Application services:

- Open a Unit of Work
- Coordinate domain engines
- Persist domain objects
- Return DTOs to the API

Application services orchestrate workflows but do not implement business rules.

## Domain Layer

The domain layer contains the core business logic of the SOC Platform.

It includes:

- Domain models
- Detection rules
- Enrichment providers
- Correlation rules
- Alert rules
- Processing engines
- Case processing logic

This layer has no knowledge of databases, web frameworks, or infrastructure.

## Persistence Layer

Persistence is abstracted through repository interfaces and coordinated by the Unit of Work.

The current implementation uses SQLite, but alternative implementations such as PostgreSQL can be introduced without modifying application or domain logic.

Responsibilities include:

- Persisting domain models
- Querying stored entities
- Managing transactions
- Mapping between domain objects and database records

## Dependency Direction

Dependencies always point inward.

```text
API
    ↓
Application
    ↓
Domain
    ↑
Infrastructure
```

This ensures that business logic remains stable even if infrastructure technologies change.

## Processing Flow

A security event moves through the following stages:

1. Event ingestion
2. Event normalization
3. Detection
4. Enrichment
5. Correlation
6. Alert generation
7. Alert processing
8. Case creation
9. Case processing
10. Persistence
11. API response

Each stage is responsible for a single part of the overall investigation lifecycle and produces the input required by the next stage.

## Benefits of the Architecture

This architecture provides several advantages:

- Clear separation of responsibilities
- High testability
- Low coupling between components
- Easy replacement of infrastructure
- Modular business logic
- Incremental feature development
- Support for future scalability and extensibility


# Project Structure 5

The SOC Platform is organized into feature-oriented packages that separate business capabilities from infrastructure concerns. Each package has a clearly defined responsibility and communicates with the rest of the application through well-defined interfaces.

```text
soc-platform/
│
├── alert/
├── api/
├── application/
├── case/
├── common/
├── correlation/
├── detection/
├── docs/
├── enrichment/
├── infrastructure/
├── normalization/
├── repositories/
├── tests/
│
├── pyproject.toml
├── README.md
└── .gitignore
```

## Package Responsibilities

### `alert/`

Contains the alert generation and alert processing domain.

Responsibilities include:

- Alert domain models
- Alert generation rules
- Alert generation engine
- Alert processing engine
- Alert processors
- Alert factory

Alerts represent actionable security findings produced from detections or correlation results.

---

### `api/`

Contains the REST API built with FastAPI.

Responsibilities include:

- Route definitions
- Dependency injection
- Request handling
- Response serialization
- Exception handlers

The API layer exposes the application without containing business logic.

---

### `application/`

Implements application use cases.

Responsibilities include:

- Application services
- Request DTOs
- Response DTOs
- Dependency composition

Application services orchestrate workflows but delegate business decisions to the domain layer.

---

### `case/`

Contains the case management domain.

Responsibilities include:

- Case domain models
- Case factory
- Case processing engine
- Case processors
- Case status management
- SLA management
- Escalation logic

Cases represent investigations created from alerts.

---

### `common/`

Contains shared domain objects used across multiple modules.

Examples include:

- Events
- Detections
- Event types
- Shared enums
- Common value objects

This package prevents duplication of fundamental domain concepts.

---

### `correlation/`

Implements security event correlation.

Responsibilities include:

- Correlation models
- Correlation engine
- Correlation rules

Correlation rules identify relationships between multiple enriched detections that indicate higher-level security activity.

---

### `detection/`

Contains detection logic.

Responsibilities include:

- Detection engine
- Detection rules

Detection rules analyze individual normalized events and identify suspicious activity.

---

### `docs/`

Contains project documentation.

Responsibilities include:

- Project handoff
- Architecture documentation
- Design decisions
- Development notes
- Future roadmap

This directory serves as the primary source of project documentation.

---

### `enrichment/`

Contains event enrichment logic.

Responsibilities include:

- Enrichment engine
- Enrichment models
- Enrichment providers

Enrichment adds contextual information to detections before correlation occurs.

---

### `infrastructure/`

Contains infrastructure-specific implementations.

Responsibilities include:

- SQLite repositories
- Database connection management
- Repository mappers
- Unit of Work implementation

Infrastructure components implement interfaces defined by the application while remaining isolated from business logic.

---

### `normalization/`

Contains log normalization logic.

Responsibilities include:

- Vendor-specific parsers
- Event normalization
- Canonical event creation

Normalization converts raw log formats into the platform's common event model.

---

### `repositories/`

Defines repository interfaces used throughout the application.

Responsibilities include:

- Repository abstractions
- Unit of Work interface

Concrete implementations reside within the infrastructure layer.

---

### `tests/`

Contains automated tests.

The project includes tests for:

- Domain models
- Business rules
- Engines
- Processors
- Application services
- Repository implementations
- REST API endpoints

Testing is organized to validate individual components as well as complete end-to-end workflows.

---

## Dependency Organization

The project follows a layered dependency model.

```text
REST API
    ↓
Application Services
    ↓
Domain
    ↑
Infrastructure
```

Each package communicates only with the layers it is intended to depend upon, preventing unnecessary coupling and preserving architectural boundaries.

## Project Organization Philosophy

The codebase is organized by business capability rather than technical framework.

Each package encapsulates a specific area of responsibility, making the platform easier to understand, maintain, test, and extend as new functionality is introduced.



# Section 6 Event Processing Pipeline 

The SOC Platform models the complete lifecycle of a security event, from ingestion through case creation. Each stage performs a single responsibility before passing its output to the next stage.

The pipeline is intentionally modular so that individual components can be extended, replaced, or enhanced without affecting the rest of the system.

## Pipeline Overview

```text
                    Raw Security Logs
                           │
                           ▼
                  Normalization Layer
                           │
                           ▼
                 Canonical Event Model
                           │
                           ▼
                  Detection Engine
                           │
                           ▼
                    Detections
                           │
                           ▼
                  Enrichment Engine
                           │
                           ▼
               Enriched Detections
                           │
                           ▼
                 Correlation Engine
                           │
                           ▼
               Correlation Results
                           │
                           ▼
                    Alert Engine
                           │
                           ▼
               Alert Processing Engine
                           │
                           ▼
                        Alerts
                           │
                           ▼
                     Case Factory
                           │
                           ▼
               Case Processing Engine
                           │
                           ▼
                         Cases
                           │
                           ▼
                     Persistence
                           │
                           ▼
                     REST Response
```

## 1. Event Ingestion

The pipeline begins when a security event is received by the REST API.

Currently, events are submitted through the `/events` endpoint using the platform's canonical event format.

In future versions, additional ingestion mechanisms may include:

- Windows Event Forwarding
- Syslog
- Microsoft Sentinel
- Splunk
- Elastic
- Kafka
- Message queues
- Streaming pipelines

The ingestion layer is responsible only for accepting events and passing them into the application.

---

## 2. Normalization

Raw vendor-specific logs are converted into the platform's canonical `Event` model.

Normalization removes vendor-specific differences and produces a consistent representation for downstream processing.

This allows detection rules to operate independently of the original log source.

Example:

```text
Windows Event
Linux Syslog
Firewall Log
Cloud Audit Log
        │
        ▼
Canonical Event
```

---

## 3. Detection

The Detection Engine evaluates the normalized event against every registered detection rule.

Each rule determines whether its specific security condition has been met.

Rules execute independently.

One event may produce:

- No detections
- One detection
- Multiple detections

The Detection Engine simply coordinates rule execution and aggregates the results.

---

## 4. Enrichment

Each detection is enriched with additional contextual information.

Examples include:

- IP geolocation
- Organization ownership
- Private/public IP classification
- Threat intelligence
- Asset information
- User information

Enrichment improves the quality of later correlation decisions without modifying the original detection.

---

## 5. Correlation

The Correlation Engine analyzes relationships between enriched detections.

Unlike detection, which evaluates a single event, correlation identifies higher-level security patterns across multiple detections.

Examples include:

- Failed login bursts
- Impossible travel
- Lateral movement
- Privilege escalation

Correlation rules produce `CorrelationResult` objects describing the identified activity.

---

## 6. Alert Generation

The Alert Engine transforms significant security findings into alerts.

Alert generation currently occurs from two sources:

- Individual detections
- Correlation results

Different alert rules determine which findings should become analyst-visible alerts.

This allows alert creation policies to evolve independently of detection and correlation logic.

---

## 7. Alert Processing

Generated alerts pass through a processing pipeline before persistence.

Current processors include:

- Deduplication
- Alert grouping
- Routing

Additional processors can be introduced without modifying existing logic.

Examples include:

- Suppression
- Priority adjustment
- Risk scoring
- Notification
- Escalation

Each processor performs one independent operation.

---

## 8. Case Creation

After alert processing, alerts are transformed into investigation cases.

The Case Factory converts alerts into case aggregates while preserving the alert's context.

Not every future alert must necessarily become a case.

Case creation policies can evolve independently through the factory.

---

## 9. Case Processing

Cases undergo additional business processing before persistence.

Current processors include:

- Assignment
- SLA calculation
- SLA breach detection
- Escalation

Future processors may include:

- Playbook assignment
- Analyst workload balancing
- Automatic closure
- Risk prioritization

Case processors operate independently and execute sequentially.

---

## 10. Persistence

After processing completes, domain objects are persisted through repositories managed by the Unit of Work.

The current persistence sequence is:

- Event
- Detection
- Alert
- Case

The Unit of Work coordinates the transaction and commits all changes as a single operation.

If processing fails before completion, the transaction is rolled back.

---

## 11. API Response

After persistence succeeds, the application service returns a response DTO containing the complete processing results.

The response includes:

- Event
- Detections
- Enriched detections
- Correlations
- Alerts
- Cases

This allows clients to inspect the complete processing pipeline from a single request.

## Pipeline Characteristics

The processing pipeline has several important architectural characteristics:

- Each stage has a single responsibility.
- Components communicate using strongly typed domain models.
- Engines coordinate workflows but do not implement business rules.
- Rules remain independent and composable.
- Processors perform isolated post-processing operations.
- Infrastructure concerns remain outside the business domain.
- New stages can be introduced without redesigning the overall architecture.

This modular pipeline enables the SOC Platform to evolve incrementally while maintaining clear architectural boundaries and high testability.


# Section 7 Domain Models 

The domain model represents the core business concepts of the SOC Platform. Every stage of the event processing pipeline operates on strongly typed domain objects rather than generic dictionaries or loosely structured data.

These models form the common language shared across the application and remain independent of infrastructure, APIs, and persistence technologies.

## Domain Model Flow

```text
Event
   │
   ▼
Detection
   │
   ▼
EnrichedDetection
   │
   ▼
CorrelationResult
   │
   ▼
Alert
   │
   ▼
Case
```

Each model represents a progressively higher level of abstraction during a security investigation.

---

## Event

The `Event` model represents a normalized security event.

It is the canonical representation used throughout the platform regardless of the original log source.

Typical information includes:

- Event identifier
- Timestamp
- Event type
- Log source
- Message
- Hostname
- Username
- Source IP
- Destination IP
- Process information
- Original raw message

Every event entering the platform is converted into this format before further processing.

---

## Detection

A `Detection` represents suspicious activity identified from a single event.

Detections are produced by detection rules executed by the Detection Engine.

Each detection contains information such as:

- Detection identifier
- Rule identifier
- Detection title
- Severity
- Source event
- Match timestamp
- Detection metadata

Multiple detections may originate from a single event.

Each detection remains independent of all others.

---

## Enriched Detection

An `EnrichedDetection` combines a detection with additional contextual information.

Rather than modifying the original detection, enrichment creates a new object that preserves the original detection while attaching enrichment results.

Typical enrichment includes:

- IP geolocation
- Organization ownership
- IP classification
- Threat intelligence
- Asset information
- User context

This separation keeps detections immutable while allowing additional context to be added over time.

---

## Correlation Result

A `CorrelationResult` represents suspicious activity identified across multiple enriched detections.

Unlike detections, which analyze individual events, correlation identifies relationships spanning multiple events.

Each correlation result contains:

- Correlation identifier
- Rule identifier
- Correlation title
- Severity
- Match timestamp
- Related enriched detections
- Correlation metadata

Correlation results represent higher-level security findings suitable for alert generation.

---

## Alert

An `Alert` represents an actionable security finding that should be presented to analysts.

Alerts are generated from either:

- Individual detections
- Correlation results

Each alert includes:

- Alert identifier
- Title
- Severity
- Status
- Source object
- Creation timestamp

Alerts may undergo additional processing before being persisted.

Examples include deduplication, grouping, and routing.

---

## Case

A `Case` represents an investigation created from one or more alerts.

Cases track the operational lifecycle of an investigation rather than the technical detection itself.

A case includes information such as:

- Case identifier
- Title
- Priority
- Status
- Assigned analyst
- Evidence
- Comments
- Timeline
- SLA information
- Resolution details

Cases continue evolving after creation as analysts investigate security incidents.

---

## Relationship Between Models

Each domain model builds upon the previous stage of the pipeline.

```text
Raw Log
    │
    ▼
Event
    │
    ▼
Detection
    │
    ▼
Enriched Detection
    │
    ▼
Correlation Result
    │
    ▼
Alert
    │
    ▼
Case
```

Each transformation increases the level of abstraction while preserving the information produced by earlier stages.

---

## Design Characteristics

The domain models share several common design principles.

### Strong Typing

Models use explicit field definitions rather than loosely structured dictionaries wherever practical.

This improves readability, validation, and correctness.

---

### Validation

Domain models validate their own data using Pydantic.

Invalid application state is rejected as early as possible before business logic executes.

---

### Immutability of Business Facts

Business facts are preserved as they move through the pipeline.

For example:

- An Event is never modified by detection.
- A Detection is never modified by enrichment.
- Enrichment produces an `EnrichedDetection`.
- Correlation consumes enriched detections without changing them.

This approach makes the processing pipeline easier to reason about and reduces unintended side effects.

---

### Clear Business Language

Each model corresponds directly to a real-world SOC concept.

The codebase intentionally avoids generic names in favor of terminology familiar to security analysts, including:

- Event
- Detection
- Correlation
- Alert
- Case

Using domain terminology consistently improves readability and makes the architecture easier to understand.

## Summary

The domain models form the foundation of the SOC Platform.

Every engine, rule, processor, repository, and application service operates on these shared business objects, ensuring consistency throughout the system while maintaining a clear separation between business logic and infrastructure.



# Detection Module

The Detection Module is responsible for identifying suspicious activity from individual normalized security events.

It is the first stage of the security analytics pipeline and transforms normalized events into one or more detections based on independently executable detection rules.

The module is designed to support incremental growth by allowing new detection rules to be added without modifying existing logic.

## Purpose

The objective of the Detection Module is to answer a single question:

> **Does this individual event indicate suspicious activity?**

Each rule evaluates the event independently and produces zero or more detections.




## Section 8 Detection Module

Unlike correlation, detection never attempts to relate multiple events together.

## Architecture

```text
                     Event
                       │
                       ▼
              Detection Engine
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
 Rule 1           Rule 2           Rule N
      │                │                │
      └────────────────┼────────────────┘
                       ▼
                 Detections
```

The Detection Engine coordinates execution but delegates all business decisions to individual rules.

## Detection Engine

The `DetectionEngine` orchestrates the detection process.

Its responsibilities include:

- Executing every registered detection rule
- Collecting detections from each rule
- Returning a combined collection of detections

The engine deliberately contains no detection logic.

Its purpose is orchestration rather than analysis.

## Detection Rules

Each detection rule represents a single security detection.

A rule examines one normalized event and determines whether its specific condition has been satisfied.

Examples include:

- Failed Windows logins
- Successful administrative logins
- PowerShell execution
- Suspicious process creation
- Firewall deny events
- DNS anomalies

Every rule is independent of every other rule.

Adding a new rule does not require changes to the Detection Engine.

## Current Implementation

The current implementation includes:

- `FailedLoginRule`

This rule detects failed Windows authentication events and produces a medium-severity detection when the configured conditions are met.

The architecture allows additional rules to be registered simply by supplying them to the `DetectionEngine`.

## Detection Output

Each successful rule returns one or more `Detection` objects.

A detection contains information including:

- Detection identifier
- Rule identifier
- Detection title
- Severity
- Source event
- Match timestamp
- Detection metadata

These detections become the input for the Enrichment Module.

## Rule Independence

Detection rules are intentionally isolated from one another.

Rules:

- do not communicate
- do not share state
- do not depend on execution order
- do not know whether other rules matched

This isolation simplifies testing and allows rules to evolve independently.

## Registration

Detection rules are registered through dependency composition.

```text
DetectionEngine
    ├── FailedLoginRule
    ├── Rule 2
    ├── Rule 3
    └── Rule N
```

The engine requires no modification when additional rules are introduced.

## Design Principles

The Detection Module follows several architectural principles.

### Single Responsibility

Each rule detects exactly one security condition.

### Open/Closed Principle

New detection capabilities are added by introducing new rule implementations rather than modifying existing code.

### Loose Coupling

The Detection Engine depends only on the rule interface, not on concrete implementations.

### High Cohesion

Each rule encapsulates all logic required for one specific detection.

### Testability

Rules can be unit tested independently without requiring databases, APIs, or infrastructure components.

## Position Within the Pipeline

The Detection Module is the first analytical stage of the processing pipeline.

```text
Normalized Event
       │
       ▼
Detection
       │
       ▼
Enrichment
       │
       ▼
Correlation
```

Every subsequent stage operates on the detections produced here.

If no detection rules match an event, the remainder of the pipeline continues with an empty detection collection.

## Future Enhancements

The architecture supports the addition of many new detection capabilities, including:

- Process execution monitoring
- PowerShell detections
- Credential access
- Registry modifications
- File integrity monitoring
- Network anomaly detection
- Cloud audit detections
- Container security events
- Threat intelligence matching
- Behavioral analytics

These additions can be implemented as new detection rules without requiring changes to the engine or surrounding architecture.

## Summary

The Detection Module transforms normalized events into security detections through a collection of independent, composable detection rules.

By separating orchestration from business logic and enforcing one responsibility per rule, the module remains highly maintainable, testable, and extensible while providing the foundation for the remainder of the SOC investigation pipeline.




# Section 9 Enrichment Module

The Enrichment Module enhances detections with additional contextual information before they enter the correlation stage.

Rather than modifying the original detection, enrichment produces a new `EnrichedDetection` object that combines the original detection with supplemental intelligence.

This preserves the integrity of the original detection while providing downstream components with richer information for analysis.

## Purpose

The objective of the Enrichment Module is to answer the question:

> **What additional context can help explain this detection?**

Enrichment does not determine whether an event is suspicious.
Instead, it gathers supporting information that improves later decision-making during correlation, alert generation, and investigations.

## Architecture

```text
                  Detection
                      │
                      ▼
             Enrichment Engine
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 IP Context      IP Classification    Enricher N
      │               │               │
      └───────────────┼───────────────┘
                      ▼
            Enriched Detection
```

The Enrichment Engine coordinates execution while individual enrichers perform the actual enrichment.

## Enrichment Engine

The `EnrichmentEngine` is responsible for orchestrating all registered enrichers.

Its responsibilities include:

- Executing each registered enricher
- Collecting enrichment results
- Combining results into a single `EnrichedDetection`
- Returning the completed object

The engine contains no enrichment logic.

It simply coordinates the enrichers in sequence.

## Enrichers

Each enricher performs one independent enrichment operation.

Examples include:

- IP geolocation
- IP ownership
- Private/public IP classification
- Threat intelligence lookups
- Asset inventory lookups
- User directory lookups
- GeoIP services
- Reputation services

Each enricher operates independently.

An enricher does not know about the existence of other enrichers.

## Current Implementation

The current implementation includes two enrichers.

### IPContextEnricher

Adds contextual information for known IP addresses.

Current information includes:

- Country
- Organization

Example:

```text
Source IP: 8.8.8.8

↓

Country:
United States

Organization:
Google
```

The current implementation uses an in-memory lookup table.

Future implementations may retrieve this information from:

- MaxMind GeoIP
- AbuseIPDB
- MISP
- OpenCTI
- Internal asset databases

without requiring changes to the enrichment engine.

---

### IPClassificationEnricher

Classifies IP addresses using Python's networking utilities.

Current classifications include:

- Private
- Public
- Loopback
- Link-local
- Global

Example:

```text
8.8.8.8

↓

is_private = False
is_global = True
is_loopback = False
```

This information is useful for downstream correlation rules and analyst investigations.

## Enriched Detection

Enrichment produces a new `EnrichedDetection` object.

```text
Detection
    +
Enrichment Data
        │
        ▼
EnrichedDetection
```

This object contains:

- Original detection
- All enrichment results

The original detection remains unchanged throughout the pipeline.

## Why Enrichment Creates a New Object

The platform intentionally avoids modifying existing business objects.

Instead of updating a `Detection`, enrichment wraps it inside an `EnrichedDetection`.

Benefits include:

- Preserving the original business fact
- Preventing accidental mutation
- Improving traceability
- Making the processing pipeline easier to understand
- Simplifying testing

Each stage of the pipeline produces a new business object rather than altering previous ones.

## Registration

Enrichers are registered through dependency composition.

```text
EnrichmentEngine
    ├── IPContextEnricher
    ├── IPClassificationEnricher
    ├── Enricher 3
    └── Enricher N
```

New enrichers can be introduced without modifying the engine.

## Design Principles

The Enrichment Module follows several architectural principles.

### Single Responsibility

Each enricher performs one enrichment operation.

### Open/Closed Principle

Additional enrichment capabilities are added by introducing new enrichers rather than modifying existing implementations.

### Loose Coupling

The Enrichment Engine depends only on the enricher interface.

Concrete enrichers remain independent.

### High Cohesion

Each enricher encapsulates one source of contextual information.

### Testability

Enrichers can be unit tested independently without requiring the remainder of the processing pipeline.

## Position Within the Pipeline

The Enrichment Module sits between detection and correlation.

```text
Event
   │
   ▼
Detection
   │
   ▼
Enrichment
   │
   ▼
Correlation
```

Correlation rules consume enriched detections rather than raw detections, allowing them to make more informed decisions.

## Future Enhancements

The architecture supports many additional enrichment providers, including:

- Threat intelligence platforms
- WHOIS lookups
- DNS enrichment
- Asset inventory databases
- Active Directory integration
- User risk scoring
- Vulnerability management systems
- Cloud asset inventories
- Endpoint management platforms
- Internal CMDB integration

Each provider can be implemented as a separate enricher and registered with the `EnrichmentEngine`.

## Summary

The Enrichment Module augments detections with contextual intelligence while preserving the original detection.

By separating enrichment into independent enrichers coordinated by the `EnrichmentEngine`, the platform remains modular, extensible, and easy to maintain as additional intelligence sources are introduced.




# Section 10 Current Status

Current Status
Overall Progress
The core SOC processing pipeline has been implemented end-to-end using Domain-Driven Design, Clean Architecture, and the Repository + Unit of Work patterns.
Current pipeline:
Event
    │
    ▼
Detection Engine
    │
    ▼
Enrichment Engine
    │
    ▼
Correlation Engine
    │
    ▼
Alert Engine
    │
    ▼
Alert Processing Engine
    │
    ▼
Case Factory
    │
    ▼
Case Processing Engine
    │
    ▼
SQLite Persistence
    │
    ▼
REST API

The system is capable of:
- accepting security events through the REST API
- normalizing events into domain models
- generating detections
- enriching detections
- correlating related detections
- generating alerts
- processing alerts
- generating cases
- processing cases
- persisting all artifacts
- retrieving persisted data through API endpoints
Implemented Modules
Common
- Event
- EventType
- Detection
- Severity
- Shared domain models
Detection
- DetectionEngine
- FailedLoginRule
Enrichment
- EnrichmentEngine
- IPContextEnricher
- IPClassificationEnricher
Correlation
- CorrelationEngine
- FailedLoginBurstRule
- ImpossibleTravelRule
- LateralMovementRule
- PrivilegeEscalationRule
Alerts
- AlertEngine
- ImmediateDetectionAlertRule
- CorrelationAlertRule
- AlertProcessingEngine
- DeduplicationProcessor
- AlertGroupingProcessor
- AlertRoutingProcessor
Cases
- CaseFactory
- CaseProcessingEngine
- Assignment Processor
- SLA Processor
- SLA Breach Processor
- Escalation Processor
Persistence
SQLite repositories for:
- Events
- Detections
- Alerts
- Cases
including:
- mappers
- repositories
- UnitOfWork
- SQLiteConnectionFactory
Application Layer
Services implemented:
- ProcessSecurityEventService
- GetEventService
- ListEventsService
- GetAlertService
- ListAlertsService
- GetCaseService
- ListCasesService
REST API
Endpoints implemented:
POST /events
GET  /events
GET  /events/{id}

GET  /alerts
GET  /alerts/{id}

GET  /cases
GET  /cases/{id}

Custom exception handling is registered globally and returns proper HTTP responses for application exceptions.
Testing
Current test status:
165 passed
0 failed

Coverage currently includes:
- Domain models
- Detection
- Enrichment
- Correlation
- Alert generation
- Alert processing
- Case processing
- SQLite repositories
- Application services
- REST API
- Exception handling
All tests are passing successfully.



# Testing

Current status:
165
165 passed
0 failed


(.venv) PS C:\Users\mikey\Projects\soc-platform> pytest -q
............................................................................................................................ [ 75%]
.........................................                                                                                    [100%]
165 passed in 0.98s


(.venv) PS C:\Users\mikey\Projects\soc-platform> pytest tests/test_api_events.py -q
....                                                                                                                         [100%]
4 passed in 0.20s


(.venv) PS C:\Users\mikey\Projects\soc-platform> pytest tests/test_api_alerts.py -q
.                                                                                                                            [100%]
1 passed in 0.08s


(.venv) PS C:\Users\mikey\Projects\soc-platform> pytest tests/test_process_security_event_service.py -q
.                                                                                                                            [100%]
1 passed in 0.06s




# Design Principles
The project follows several architectural principles:
- Domain-Driven Design (DDD)
- Clean Architecture
- Hexagonal Architecture (Ports & Adapters)
- SOLID principles
- Dependency Injection
- Repository Pattern
- Unit of Work Pattern
- Strongly typed domain models
- Rich domain objects
- Engines orchestrate only
- Rules implement one business decision
- Processors perform one post-processing responsibility
- Infrastructure remains replaceable
Current Processing Pipeline
Event
        │
        ▼
Normalization
        │
        ▼
Detection Engine
        │
        ▼
Enrichment Engine
        │
        ▼
Correlation Engine
        │
        ▼
Alert Engine
        │
        ▼
Alert Processing Engine
        │
        ▼
Case Factory
        │
        ▼
Case Processing Engine
        │
        ▼
Persistence
        │
        ▼
REST API

# Current Project Status
Completed:
- Event normalization
- Detection engine
- Detection rules
- Enrichment engine
- Correlation engine
- Alert engine
- Alert processing
- Case generation
- Case processing
- SQLite persistence
- Repository implementations
- Unit of Work
- FastAPI
- Exception handling
- API integration tests
- Dependency composition
- OpenAPI documentation
Current test count:
165 passing

# Remaining Work
Planned next milestones:
REST API
- Alert endpoints
- Case endpoints
- Filtering
- Pagination
- Search
Frontend
Possible options:
- React
- Vue
- Svelte
Dashboard:
- Events
- Alerts
- Cases
- Investigation timeline
Persistence
Future improvements:
- PostgreSQL
- Alembic migrations
- Indexes
- Query optimization
Security
- Authentication
- Authorization
- RBAC
- API keys
- JWT
Observability
- Logging
- Metrics
- Tracing
- Health endpoints
Deployment
- Docker
- Docker Compose
- CI/CD
- GitHub Actions
Documentation
Still to add:
- Architecture diagrams
- Sequence diagrams
- Domain diagrams
- Contributor guide
- Deployment guide
Development Workflow
Recommended workflow:
1. Write failing tests.
2. Implement domain logic.
3. Pass tests.
4. Refactor.
5. Update documentation.
6. Commit.
7. Repeat.
Repository State
Current checkpoint:
165 passing tests

Events API completed

Alert API started

Architecture stable

Ready for continued feature development

# Notes for Future Development
Keep the following principles:
- Do not bypass application services.
- Do not let the API access repositories directly.
- Keep engines orchestration-only.
- Business logic belongs inside rules/processors.
- Infrastructure must remain replaceable.
- Preserve dependency inversion.
- Prefer composition over inheritance.
- Keep domain models framework-independent.
- Add tests for every new feature.
