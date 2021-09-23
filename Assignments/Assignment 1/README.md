# Assignment 1: DB Replicator

### Problem Statement
Create a DB replicator which replicates data changes from Postgres to MongoDB. Use GRPC with [gprc requests](https://github.com/spaceone-dev/grpc_requests) wrapper as a communication protocol. It should be one-way replication and expects to be near realtime aside from the GRPC latency.

## Pre-Requisites:

  - [ ] **PostgreSQL v13.4** is used as a relational database. Choose your installer type depending on the host operating system over which server is expected to be installed [here](https://www.postgresql.org/download/).

  - [ ] **Mongo DB v5.0.2** is a source-available cross-platform document-oriented database program. Choose your installer type depending on the host operating system over which server is expected to be installed [here](https://www.mongodb.com/try/download/community/).
  
  - [ ] **Wal2Json** is an output plugin for logical decoding. Follow steps mentioned for particular host operating system [here](https://github.com/eulerto/wal2json/).

## Run Project:
- Run below commands from ***assignment_root*** directory for various tasks.

  * **Run Wal2Json Plugin**: This will create test_slot which will listen to postgres server for DB changes. Provide password for the given username. The data changes would be written in json format in wal_log.txt file.

    ```
    pg_recvlogical -d postgres --username=postgres --slot test_slot --start -o pretty-print=1 -o add-msg-prefixes=wal2json -f wal_log.txt
    ```

  * **Run Server**: This will run server on localhost:50051

    ```
    python3 server_repl.py
    ```
    
  * **Run Client**: This will run client which will read wal_log.txt file.

    ```
    python3 client_repl.py
    ```

  * **Execute sql queries for postgres db.**: This will create students table and insert student data into db.
    
    ```
    CREATE TABLE IF NOT EXISTS public.students (
      id bigint NOT NULL,
      first_name character varying(255) COLLATE pg_catalog."default",
      last_name character varying(255) COLLATE pg_catalog."default",
      email character varying(255) COLLATE pg_catalog."default",
      sjsu_id character varying(20) COLLATE pg_catalog."default",
      create_timestamp timestamp with time zone,
      update_timestamp timestamp with time zone,
      CONSTRAINT student_pkey PRIMARY KEY (id)
    );
    ```
    ```
    INSERT INTO public.students(id, first_name, last_name, email, sjsu_id, create_timestamp, update_timestamp)
    VALUES (1000, 'John', 'Doe', 'john.doe@sjsu.edu', '1456990',current_timestamp , current_timestamp);
    ```
  * **Read Mongo DB to verify changes**: This will choose college as database and run find query on students collection.

    ```
    use college
    db.students.find()
    ```