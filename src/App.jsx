import { useEffect, useState } from "react";

function App() {
  const [facturas, setFacturas] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/facturas")
      .then((res) => {
        if (!res.ok) throw new Error("Error al obtener facturas");
        return res.json();
      })
      .then((data) => {
        setFacturas(data);
        setCargando(false);
      })
      .catch((err) => {
        setError(err.message);
        setCargando(false);
      });
  }, []);

  if (cargando) return <p>Cargando facturas...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Facturas</h1>
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Número</th>
            <th>Cliente</th>
            <th>Monto</th>
            <th>IVA</th>
          </tr>
        </thead>
        <tbody>
          {facturas.map((f) => (
            <tr key={f.numero}>
              <td>{f.numero}</td>
              <td>{f.cliente}</td>
              <td>${f.monto.toFixed(2)}</td>
              <td>{f.iva ? "Sí" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;