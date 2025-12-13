#!/bin/bash
set -e

echo "Starting creation of tables"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    \c $POSTGRES_DB $POSTGRES_USER;
          
    CREATE TABLE IF NOT EXISTS test_results (
        id SERIAL PRIMARY KEY,
        session_id UUID,
        times JSONB,
        average_time DOUBLE PRECISION,
        workability_index DOUBLE PRECISION,
        mental_stability_index DOUBLE PRECISION,
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_session_id ON test_results(session_id);
    
    CREATE INDEX IF NOT EXISTS idx_created_at ON test_results(created_at);
    
EOSQL

echo "Creation of tables completed successfully!"