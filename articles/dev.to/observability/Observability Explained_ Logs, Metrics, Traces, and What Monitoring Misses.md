# Observability Explained: Logs, Metrics, Traces, and What Monitoring Misses

## Table of Contents

  - [📡 1. The Three Observability Pillars (and the "Fourth")](#-1-the-three-observability-pillars-and-the-fourth)
    - [1️⃣ Logs — What happened?](#1-logs--what-happened)
    - [2️⃣ Metrics — How much, how often, and how fast?](#2-metrics--how-much-how-often-and-how-fast)
    - [3️⃣ Traces — Where did the request go?](#3-traces--where-did-the-request-go)
    - [4️⃣ Events (the unofficial pillar) — What changed?](#4-events--what-changed)
    - [What about profiles?](#what-about-profiles)
  - [2. Monitoring, Security, and Observability](#2-monitoring-security-and-observability)
    - [🖥️ Infrastructure monitoring](#-infrastructure-monitoring)
    - [📈 Application monitoring](#-application-monitoring)
    - [🔐 Security monitoring](#-security-monitoring)
  - [3. Following a Request Through a LAMP Stack (Example)](#3-following-a-request-through-a-lamp-stack-example)
  - [4. Where Common Observability Tools Fit](#4-where-common-observability-tools-fit)
  - [🧠 The Mental Model to Remember](#-the-mental-model-to-remember)

## Introduction

You check the monitoring dashboard.

The web server is up. PHP is running. MariaDB accepts connections. CPU and memory look fine. The application returns `HTTP 200 OK`.

Yet users are still reporting that the application is slow.

So where is the problem?

Traditional monitoring is excellent at answering questions we already know to ask:

- Is the server reachable?
- Is the filesystem nearly full?
- Is CPU utilisation too high?
- Is the service running?
- Does the website return HTTP 200?

But modern systems often fail in ways that cannot be understood from a single health check or dashboard.

This is where **observability** becomes useful.

Observability is the ability to understand what is happening inside a system from the telemetry it produces. Rather than simply asking whether a component is up or down, it helps us investigate **why the system is behaving the way it is**.

A useful mental model is:

> **Telemetry + context + correlation = observability**

Monitoring and observability are not competitors. Monitoring remains essential. Observability gives us the context when the answer is not obvious.

---

## 📡 1. The Three Observability Pillars (and the "Fourth")

Observability is traditionally described using three pillars:

1. **Logs**
2. **Metrics**
3. **Traces**

You will also increasingly encounter **events** as an additional signal, while **profiles** are becoming more important in modern observability platforms.

The terminology is not completely rigid. For example, OpenTelemetry currently treats events as a specialised form of log data and is developing support for profiles. The three-pillar model remains useful because it gives us a simple way to understand the main types of telemetry.

### 1️⃣ Logs — What happened?

Logs are records of events produced by applications, operating systems, network devices, security tools and services.

Examples include:

```text
nginx:
Path: /var/log/nginx/access.log

GET /users HTTP/1.1 200
```

```text
php:
Path: /var/log/php-fpm/www-error.log

User request completed successfully
```

```text
mariadb:
Path: /var/log/mariadb/mariadb.log

Slow query detected: query_time=0.412 seconds
```

Logs can include:

- application logs (e.g. NGINX);
- Linux and Windows system logs;
- authentication logs;
- audit trails;
- database logs;
- Kubernetes container logs;
- security events.

Logs are particularly useful when we need detailed information about a specific event.

A metric might tell us that errors increased at 14:05.

A log may tell us **what the error actually was**.

### 2️⃣ Metrics — How much, how often, and how fast?

Metrics are numerical measurements, normally recorded over time.

Examples include:

```text
CPU utilisation:        62%
Memory utilisation:     71%
HTTP request rate:      240 requests/sec
HTTP p95 latency:       430 ms
Database connections:   87
HTTP 5xx error rate:    2.4%
```

Metrics are excellent for:

- dashboards;
- alerting;
- capacity planning;
- trend analysis;
- service-level indicators;
- identifying abnormal behaviour.

Prometheus is a commonly used metrics platform. It stores metrics as time-series data and is frequently used for application monitoring.

For an application, useful metrics might include:

```text
http_requests_total
http_request_duration_seconds
http_errors_total
active_sessions
database_connection_pool_usage
```

Metrics are very good at showing that **something has changed**.

They do not always tell us why.

### 3️⃣ Traces — Where did the request go?

Tracing follows a request as it passes through different parts of an application.

Imagine a request to:

```text
GET /users
```

The request may actually travel through several components:

```text
User
 ↓
Nginx
 ↓
PHP
 ↓
MariaDB
```

A distributed trace could show:

```text
GET /users                    428 ms
│
├── Nginx                       3 ms
├── PHP routing                17 ms
├── Authentication              8 ms
└── MariaDB                   400 ms
     └── SELECT username, email
         FROM users
         WHERE id = ?;
```

The overall request took 428 ms, but the trace immediately shows that approximately 400 ms was spent waiting for MariaDB.

A trace is normally made up of **spans**, where each span represents an operation within the wider request.

Tracing therefore helps answer:

> **Where did the time go?**

This becomes increasingly valuable in distributed systems, where a single user request may pass through load balancers, APIs, containers, databases, queues and external services.

OpenTelemetry is one of the most important technologies in this area. It provides a vendor-neutral framework for instrumenting applications and collecting and exporting telemetry such as traces, metrics and logs.

### 4️⃣ Events — What changed?

> Events - the unofficial pillar

Events represent meaningful changes that occurred at a particular point in time.

Examples include:

```text
14:00  Application v2.4 deployed
14:03  Database latency increased
14:04  Kubernetes pod restarted
14:05  Terraform apply completed
14:06  Privileged account modified
```

These can be incredibly useful during incident investigation.

If application latency suddenly rises, one of the first questions is often:

> **What changed?**

Deployment events, configuration changes, scaling actions, CI/CD runs and security events provide valuable context alongside logs, metrics and traces.

---

## 2. Monitoring, Security, and Observability

One of the easiest ways to make observability confusing is to treat every monitoring product as though it performs the same job.

It does not.

A real environment will often use different tools for different layers.

### 🖥️ Infrastructure monitoring

Infrastructure monitoring focuses on the health of the systems that applications depend on.

A platform such as **Checkmk** or **Zabbix** might monitor:

```text
Server
├── Availability
├── CPU
├── Memory
├── Filesystems
├── Network interfaces
├── Processes
└── Services
```

It can also perform active checks against network services, allowing us to monitor whether a service is externally reachable and how long it takes to respond.

The question is primarily:

> **Is the infrastructure healthy?**

---

### 📈 Application monitoring

Application monitoring focuses on how the application itself behaves.

**Prometheus** is commonly used to collect application and service metrics such as:

```text
Request rate
Error rate
Request duration
Queue depth
Active sessions
Database connection usage
```

The question becomes:

> **Is the application behaving normally?**

📌 Prometheus is not limited to applications; it is also heavily used for infrastructure and Kubernetes metrics. The distinction here is about the **type of monitoring we are performing**, rather than a hard boundary around a particular product.

---

### 🔐 Security monitoring

Security monitoring asks a different set of questions.

A platform such as **Wazuh** can provide SIEM capabilities around areas such as:

```text
Authentication activity
File integrity
Endpoint activity
Privilege changes
Security alerts
Vulnerability information
Suspicious behaviour
```

The question becomes:

> **Is something suspicious, unauthorised, or security-relevant happening?**

💡 Security monitoring often consumes logs from other monitoring tools:

```text
Infrastructure logs ───────────┐
                               │
Application logs ──────────────┤
                               │
Identity / authentication ─────┤
                               ├──→ Security Monitoring / SIEM
Network telemetry ─────────────┤
                               │
Endpoint telemetry ────────────┘
```

That does not mean a SIEM necessarily ingests every raw infrastructure metric or every distributed trace.

It means security analysis benefits from context across infrastructure, applications, identity, networks, endpoints and cloud platforms.

👉 The important point is that these disciplines overlap:

```text
                   Observability
                         │
          ┌──────────────┼──────────────┐
          │              │              │
   Infrastructure     Application     Security
    Monitoring         Monitoring     Monitoring
    👉Checkmk👈       👉Prometheus👈    👉Wazuh👈
```

They are different views of the same environment.

---

## 3. Following a Request Through a LAMP Stack (Example)

Let's make this concrete with a deliberately simple LAMP-style application.

Our application consists of:

```text
User
 ↓
Nginx
 ↓
PHP
 ↓
MariaDB
```

Users are reporting that the website feels slow.

### Start with basic monitoring

We might already have several health checks:

```text
Nginx
GET /
HTTP 200
Response time: 18 ms
```

PHP might expose a simple health endpoint:

```text
GET /health.php

HTTP 200
Response time: 27 ms
```

And the application could expose a database health check:

```text
GET /db_health.php

Database connection: successful
Response time: 410 ms
```

Everything is technically **up**.

But something is clearly wrong.

The database health check taking 410 ms is our first useful clue.

### Infrastructure monitoring adds context

Checkmk might show:

```text
MariaDB server

Host:          UP
MariaDB:       RUNNING
CPU:           88%
Memory:        71%
Disk latency:  Normal
```

We now know that the database host is available, but its CPU utilisation is unusually high.

That is useful.

It still does not tell us exactly what the application is doing.

### Application metrics show the pattern

Prometheus might show:

```text
HTTP request rate:       Normal
HTTP error rate:         Low
p95 request latency:     440 ms
DB query latency:        Increasing
```

Now the picture is becoming clearer.

The application is not receiving unusual traffic and it is not producing large numbers of errors.

Instead, request latency appears to be correlated with database latency.

### Tracing shows where the time goes

Now imagine the application has been instrumented using OpenTelemetry.

A trace for a slow request might show:

```text
GET /users                    428 ms
│
├── Nginx                       3 ms
├── PHP routing                17 ms
├── Authentication              8 ms
└── MariaDB                   400 ms
     └── SELECT username, email
         FROM users
         WHERE id = ?;
```

We no longer just know that the application is slow.

We know where most of the request time is being spent.

### Logs explain what happened

MariaDB's slow query log might then show something like:

```text
Query_time: 0.397
Rows_examined: 180432
```

Now we have several signals telling the same story:

```text
Checkmk
Database CPU is rising
        │
        ▼
Prometheus
Database latency is increasing
        │
        ▼
OpenTelemetry trace
~400 ms spent inside the database operation
        │
        ▼
MariaDB logs
Slow query identified
```

This is the value of correlation.

No single tool is "observability".

The useful result comes from combining signals and context to understand what is actually happening.

### Security adds another dimension

Imagine that Wazuh also reports repeated failed authentication attempts against the application server during the same period.

That does **not** automatically mean the performance problem is a security incident.

But it is useful context.

Perhaps the two events are unrelated.

Perhaps they are part of the same incident.

Observability gives engineers the information required to investigate rather than guess.

A wider incident timeline might look like:

```text
14:00  New application release deployed
14:03  Database latency begins increasing
14:04  MariaDB CPU rises
14:05  Slow queries appear
14:06  Failed authentication activity detected
```

At that point we can start asking much better questions.

Was a code change responsible for the slow query?

Did a configuration change affect the database?

Is unusual authentication activity relevant or coincidental?

That is a much richer operational picture than simply knowing that the website still returns HTTP 200.

---

## 4. Where Common Observability Tools Fit

There is no requirement for one platform to perform every observability function.

In fact, many environments deliberately use specialised tools for different layers.

| Tool              | Primary role                           | Typical use                                                                  |
| ----------------- | -------------------------------------- | ---------------------------------------------------------------------------- |
| **Checkmk**       | **Infrastructure** and service monitoring| Hosts, services, CPU, memory, storage, networks and availability             |
| **Prometheus**    | Metrics collection and **application** monitoring  | Application, infrastructure and Kubernetes time-series metrics               |
| **Wazuh**         | **Security** monitoring / SIEM / XDR   | Authentication, endpoint activity, file integrity and security events        |
| **OpenTelemetry** | Instrumentation and telemetry pipeline | Generating, collecting, processing and exporting logs, metrics and traces    |
| **Loki**          | Log aggregation                        | Application, system and container logs                                       |
| **Tempo / Jaeger**| Distributed tracing                    | Traces and spans across services                                             |
| **Grafana**       | Visualisation and exploration          | Dashboards and correlation across multiple telemetry sources                 |
| **Fluent Bit**    | Telemetry/log forwarding               | Collecting and forwarding logs from hosts and containers                     |

A simplified open-source observability architecture might look like this:

```text

1. Infrastructure ──────────→ Checkmk

                    2. Application
                            │
                     OpenTelemetry
                            │
             ┌──────────────┼──────────────┐
             │              │              │
           Metrics         Logs          Traces
             │              │              │
        Prometheus         Loki       Tempo / Jaeger
             │              │              │
             └──────────────┼──────────────┘
                            │
                         Grafana


3. Security ─────────────→ Wazuh
                              ↑
                       security context
                       from many layers
```

The exact architecture will vary.

A Kubernetes platform may lean heavily on Prometheus, OpenTelemetry, Loki and Tempo.

A traditional enterprise environment may already have mature infrastructure monitoring in Checkmk and security monitoring in Wazuh or another SIEM.

Both can still form part of a wider observability strategy.

OpenTelemetry is especially important because it provides a vendor-neutral way to instrument applications and move telemetry between systems rather than tightly coupling application code to one observability vendor.

---

## References

- OpenTelemetry — Documentation: https://opentelemetry.io/docs/
- OpenTelemetry — Signals: https://opentelemetry.io/docs/concepts/signals/
- Prometheus — Overview: https://prometheus.io/docs/introduction/overview/
- Checkmk — User Guide: https://docs.checkmk.com/latest/en/
- Checkmk — Active checks: https://docs.checkmk.com/latest/en/active_checks.html
- Wazuh — Getting Started: https://documentation.wazuh.com/current/getting-started/index.html
- Grafana Tempo — Documentation: https://grafana.com/docs/tempo/latest/
