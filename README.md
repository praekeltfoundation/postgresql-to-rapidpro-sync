# PostgreSQL to RapidPro sync
A task, that can be run once off or periodically, that looks up a specific table in a PostgreSQL data.

It expects a specific column in that table to be the way to identify the contact, and the other columns in that table to be the contact fields that we want to update.

It will go through every row in the table, and use RapidPro's API to update each contact.

## Configuration
Configuration is handled using environment variables

**DATABASE_DSN** - How to connect to the database, eg. `postgresql://user:pass@host:port/db`

**DATABASE_TABLE** - The database table to pull data from, eg. `contacts`

**RAPIDPRO_HOST** - The hostname of the rapidpro instance, eg. `textit.in`

**RAPIDPRO_TOKEN** - The token to use to authenticate to the RapidPro API, eg. `b50c919959954e5a8c5476c2b9d671e2`

**CONCURRENCY** - How many requests to make to the RapidPro API in parallel. Defaults to 1
