# PostgreSQL to Power BI Export
Export all tables from a PostgreSQL database to CSV files in a SharePoint or OneDrive folder for consumption by Power BI Service — **without requiring an on-premises data gateway or admin rights.**

## Why This Exists
Power BI Service cannot connect directly to on-premises PostgreSQL databases without a data gateway.
This project provides a **gateway-free workaround** by using Python to extract data and publish it to a cloud-accessible location supported by Power BI Service.

## How it works
```
PostgreSQL Database
        ↓
Python Export Script
        ↓
SharePoint / OneDrive (CSV files)
        ↓
Power BI Service (Scheduled Refresh)
```
Power BI never connects to PostgreSQL — it only reads exported files.
