
const { Pool } = require('pg')
const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'far_api',
    password: 'peer',
    port: 5432,
})

pool.query('SELECT NOW()', (err, res) => {
    console.log(err, res) 
    pool.end() 
})


