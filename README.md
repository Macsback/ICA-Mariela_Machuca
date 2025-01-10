# SPOT Necessary code

Sadly the aws domain can only show the login page and do the google login. But can't go further than that because of an SQL connection issue. To see the whole app please run the files locally. 

# AWS Domain
http://maciotca.online/

# Run The app

``` In terminal
cd ICA-Mariela_Machuca
python -m Spot.app

```

# SQL Tables and Sample Data

This document contains the SQL code to create the required tables and insert the needed data into the database.

## Create Tables

### `food_items` Table
```sql
CREATE TABLE food_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    temperature FLOAT NOT NULL,
    cookingTime INT NOT NULL,
    humidity FLOAT NOT NULL
);
```

### `users` Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    google_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    isAdmin BOOLEAN DEFAULT FALSE
);
```

## Data

### Insert Data into `food_items`
```sql
INSERT INTO food_items (name, temperature, cookingTime, humidity)
VALUES 
    ('chocolate', 45.0, 10, 45.0),
    ('caramel', 185.0, 15, 50.0),
    ('chicken', 73.9, 20, 60.0),
    ('rice', 90.0, 20, 85.0);
```


