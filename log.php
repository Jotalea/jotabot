<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="5">  <!-- Recargar cada 5 segundos -->
    <title>Registro de Comandos</title>
</head>
<body>
    <h1>Registro de Comandos</h1>

    <?php
    // Conectar a la base de datos
    $conn = new SQLite3('database.db');

    // Obtener registros de la base de datos
    $result = $conn->query('SELECT * FROM command_logs');

    // Mostrar registros en una tabla
    echo '<table border="1">';
    echo '<tr><th>ID</th><th>Comando</th><th>Usuario</th><th>Timestamp</th></tr>';

    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        echo '<tr>';
        echo '<td>' . $row['id'] . '</td>';
        echo '<td>' . $row['command'] . '</td>';
        echo '<td>' . $row['user'] . '</td>';
        echo '<td>' . $row['timestamp'] . '</td>';
        echo '</tr>';
    }

    echo '</table>';

    // Cerrar la conexión a la base de datos
    $conn->close();
    ?>

</body>
</html>
