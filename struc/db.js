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

/**
  Returns an Array of dictionaries
 * @param {string} sql - The SQL query to run.
 * @param {Array} binds - The values to bind to the query.
*/
async function fetch(sql, binds = undefined) {
  let returned_fetch;
  if (binds === undefined) {
    returned_fetch = await pool.query(sql);
  } else if (binds !== undefined) {
    returned_fetch = await pool.query(sql, binds);
  }
  return returned_fetch.rows;
}
/**
 * @param  {string} sql - The SQL query to run.
 * @param  {Array<Object>} binds - The values to bind to the query.
 */
async function modify(sql, binds = undefined) {
  await pool.query("BEGIN;");
  if (binds === undefined) {
    await pool.query(sql);
  } else if (binds !== undefined) {
    await pool.query(sql, binds);
  }

  await pool.query("COMMIT;");
}
/**
 * 
 * @param {string} table - The table to create.
 * @param {string} columns - The columns to create under the table. 
 */
async function create(table, columns) {
  await pool.query("BEGIN;");
  await pool.query(`CREATE TABLE IF NOT EXISTS ${table}(${columns});`);
  await pool.query("COMMIT;");
}

module.exports = { fetch, modify, create };
