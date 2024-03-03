const sql = require('mssql');

const config = {
    user: 'sa',
    password: 'Open6736',
    server: '190.210.182.24',
    port: 1433,
    database: 'Pisos',
    options: {
        instanceName: 'sqlexpress',
        encrypt: false
    }
};


// Ejecución de la consulta
async function executeQuery() {
    try {
        await sql.connect(config);
        const result = await sql.query`EXEC SP_PresupuestosPendientes 1, '2024-02-06', '2024-02-07'`;
        console.log(result);
    } catch (err) {
        console.error('Error al ejecutar la consulta:', err);
    } finally {
        sql.close();
    }
}

executeQuery();