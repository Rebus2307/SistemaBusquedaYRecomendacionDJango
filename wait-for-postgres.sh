#!/bin/sh

set -e

host="$1"

echo "⏳ Esperando a que PostgreSQL esté listo en $host..."

until PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "$host" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c '\q' 2>/dev/null; do
  sleep 2
done

echo "✅ PostgreSQL está listo. Ejecutando comandos Django..."

# Ejecutar el resto del comando
shift
exec "$@"
