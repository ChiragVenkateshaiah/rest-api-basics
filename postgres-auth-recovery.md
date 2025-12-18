# PostgreSQL Password Recovery & Secure Credential Rotation (Windows)

## Overview

During local FastAPI development, I encountered a common real-world issue:
**forgotten PostgreSQL credentials** while connecting FastAPI (SQLAlchemy) and pgAdmin to a local PostgreSQL instance on Windows.

This document explains the **safe, developer-approved recovery process** I followed to regain access, reset credentials, and restore secure authentication.

---


## Problem Statement

- PostgreSQL was running locally on Windows
- pgAdmin and FastAPI failed to connect due to:
**FATAL: Password authentication failed for user "Postgres"**

- The original database password was forgotten
> PostgreSQL does **not** allow password recovery, only **password rotation**.

---

## Key Learnings

- PostgreSQL passwords are **not stored in plaintext**
- Forgotten passwords must be **rest**, not retrieved
- Authentication rules are controlled via `pg_hba.conf`
- Security must be temporarily relaxed **only for recovery**
- Proper authentication myst be restored immediately

---

## Recovery Strategy (Local Windows)

### 1. Locate PostgreSQL Authentication Config

On Windows, the authentication rules are defined in:

```text
C:\program Files\PostgreSQL\<version>\data\pg_hba.conf
```
This file controls how clients authenticate to PostgreSQL

### 2. Temporarily Allow Local Trust Authentication

For local recovery only, the authentication method was changed:

Before

```text

host    all     all     127.0.0.1/32    scram-sha-256
host    all     all     ::1/128         scram-sha-256
```

Temporary Change

```text

host    all     all     127.0.0.1/32    trust
host    all     all     ::1/128         trust
```

> **trust allows password-less local access and must never be left enabled**

### 3. Restart PostgreSQL Service

PostgreSQL was restarted using Windows Services:
```text
services.msc
-> postgresql-x64-xx
-> restart
```

### 4. Login without Password (psql)

Using SQL Shell (psql):
```text

server : localhost
Database : postgres
Port : 5432
Username : postgres
```

Successful Login Confirmation:
```text
postgres=#
```

### 5. Reset PostgreSQL Password
Once authenticated, the password was safely rotated:

```sql
ALTER USER postgres WITH PASSWORD 'NewStrongPassword';
```

### 6. Restore Secure Authentication (CRITICAL)

Authentication rules were reverted to secure mode:
```text
host    all     all     127.0.0.1/32 scram-sha-256
host    all     all     ::1/128      scram-sha-256
```
> **PostgreSQL service was restarted again**.

## FastAPI / SQLAlchemy Configuration
After password rotation, the FastAPI database connection was updated:

```python

DATABASE_URL = "postgresql+psycopg2://postgres:<password>@localhost:5432/postgres"
```
Best practice:
- Use environment variables
- Avoid hard-coded credentials


