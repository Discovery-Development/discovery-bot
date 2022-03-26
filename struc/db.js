const { Pool } = require("pg");
require("dotenv").config("../.env");

const pool = new Pool({
  host: process.env.HOSTNAME,
  user: process.env.DB_USER,
  port: process.env.PORT,
  password: process.env.PASSWORD,
  database: process.env.DATABASE,
  max: 10,
  connectionTimeoutMillis: 0,
  idleTimeoutMillis: 0,
});

async function fetch(sql, binds = undefined) { // Will return an array of dictionaries which contain the requested data
  if (binds === undefined) {
    fetch = await pool.query(sql);
  } else if (binds !== undefined) {
    fetch = await pool.query(sql, binds);
  }
  return fetch.rows;
}

async function modify(sql, binds = undefined) {
  await pool.query("BEGIN;");
  if (binds === undefined) {
    await pool.query(sql);
  } else if (binds !== undefined) {
    await pool.query(sql, binds);
  }

  await pool.query("COMMIT;");
}

async function create(table, columns) {
  await pool.query("BEGIN;");
  await pool.query(`CREATE TABLE IF NOT EXISTS ${table}(${columns});`);
  await pool.query("COMMIT;");
}

module.exports = { fetch, modify, create };
