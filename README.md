# Packet Loss Monitor

This is a demo code to show how we can monitor a packet loss on grafana dashboard.

## Tools used

- Flask for Grafana App
- SQLite for storing data
- Grafana for viewing graphs

## Setup Components

### Setup SQLite Database

#### Create Database

Run the following command in your shell to create database.

```bash
sqlite3 monitor.db
```

This creates a file in your current directory.

#### Create Table

Now you will be inside sqlite prompt, copy the following to create a table `packet_latency`

```sql
CREATE TABLE packet_latency (
   epoc     INT PRIMARY KEY     NOT NULL,
   min      REAL    NOT NULL,
   avg      REAL    NOT NULL,
   max      REAL    NOT NULL,
   stddev   REAL    NOT NULL
);
```

### Setup Agent

- This is a simple bash script. Update the `SQLITE_DATABASE_PATH` to the database file created above.

> Tip: use absolute path for `SQLITE_DATABASE_PATH` to avoid any dir not found issues.

- Also update ping binary path in variable `PING_BIN_PATH`. This is generally required if you are on Mac. You can find it by running the command `which ping`. Keep `PING_BIN_PATH=ping` if that works for you.
- Use crontab or add entry to `/etc/cron.d/root_cron. Add the following entry

```bash
*/2 * * * * bash /PATH/TO/REPO/check_packetloss.sh
```

This cron runs every 2 minute. Update it as per your need.

### Setup Flask App

This is the backend server that will query SQLite and server data to Grafana SimpleJson plugin.

Install the required dependencies

```bash
pip3 install Flask==1.1.2 db-sqlite3==3 0.0.1
```

This should suffice, as everything else should be already part of python3.

Run the flask server

```bash
python3 app.py
```

This should start a flask server, verify it by running following commands in different shell

```bash
curl localhost:5000
> OK

curl -XPOST localhost:5000/search
> ["min_latency","avg_latency","max_latency","stddev_latency"]
```

where `localhost:5000` is your flask server endpoint.

### Setup Grafana

- Use the official docs to install grafana: [here](https://grafana.com/docs/grafana/latest/installation/)
- Install the Grafana plugin `SimpleJson`: [here](https://grafana.com/grafana/plugins/grafana-simple-json-datasource/installation)
- Make sure you restart the Grafana server after plugin is installed.
- Open grafana UI, mostly it runs on `localhost:3000`. The default login creds would be admin, admin.
- To setup DataSource, 
  - go to `http://localhost:3000/datasources`
  - Click `Add Datasource`
  - Search for SimpleJson and select it
  - `Name` it anything you like
  - In the `URL` field, add the URL of flask server, i.e. `localhost:5000`
  - Click `Save & Test`, There should be a green popup saying `Data source is working`.

- Done, you can now create Grafana dashboards.
