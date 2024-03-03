const { exec } = require('child_process');

// Función para instalar mssql
function installMssql() {
    return new Promise((resolve, reject) => {
        exec('npm install mssql', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error al instalar mssql: ${error.message}`);
                reject(error);
            }
            if (stderr) {
                console.error(`Error de stderr al instalar mssql: ${stderr}`);
                reject(stderr);
            }
            console.log(`mssql se instaló correctamente: ${stdout}`);
            resolve();
        });
    });
}

// Ejecuta la función de instalación y luego ejecuta la consulta
async function start() {
    try {
        await installMssql();
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
        try {
            await sql.connect(config);
            const result = await sql.query`EXEC SP_PresupuestosPendientes 1, '2024-02-06', '2024-02-07'`;
            console.log(result);
        } catch (err) {
            console.error('Error al ejecutar la consulta:', err);
        } finally {
            sql.close();
        }
    } catch (error) {
        console.error('Error al iniciar:', error);
    }
}

start();
