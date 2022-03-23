const { Client } = require("pg");

const client = new Client({
    host: process.env.HOSTNAME,
    user: process.env.DB_USER,
    port: process.env.PORT,
    password: process.env.PASSWORD,
    databse: process.env.DATABASE
});

client.connect();
