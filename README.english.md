[← Leer en Español](README.md)

---

# Enterprise RPA Intelligence & Scraping Suite

## Project Overview

This enterprise-grade Robotic Process Automation (RPA) solution demonstrates a modern hybrid architecture for bulk data extraction, ETL (Extract, Transform, Load) processing, automated target system loading, and integration with low-code orchestration workflows.

The system was engineered to address common challenges in enterprise environments: bulk extraction performance, resilience against DOM or UI element interceptions, structured data transformation, and real-time executive notifications.

---

## Solution Architecture

The workflow follows a multi-tiered architecture decoupled into four primary phases:

```text
+-------------------------------------------------------------------------------------+
| 1. BULK EXTRACTION            2. ETL & TRANSFORMATION        3. DATA PUBLISHING     |
|   (Playwright)                   (Pandas)                      (Selenium)           |
|                                                                                     |
|  Asynchronous scraping --->    Data cleansing          --->   Web Form Filling      |
|  across 50 pages               Rule-based filtering           DOM Element Handling  |
|  (~1,000 records)              Excel Report Generation        JS Click Interception |
+-------------------------------------------------------------------------------------+
                                                                   |
                                                                   v
                                                        4. ORCHESTRATION & ALERTS
                                                           (n8n & Webhooks)
                                                                   |
                                                                   v
                                                        Email Notifications /
                                                        Execution Monitoring
