#!/usr/bin/env bash

SCHEMA_NAME="myio"
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -h|--help)
            echo "Usage: $0 [options]"
            echo "  -h, --help      Display help"
            echo "  -s, --schema  Set schema (requires value)"
            exit 0
            ;;
        -s|--schema)
            SCHEMA_NAME="$2"
            shift 2 # Shift past the flag and its value
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ -z "${SCHEMA_NAME}" ]; then
    echo "Schema name is required"
    return 1
fi

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="/tmp/${SCHEMA_NAME}_vacuum_${TIMESTAMP}.log"

pushd /usr/lib/postgresql/16/bin

./vacuumdb -h localhost -p 5432 \
    -U "postgres" -d "postgres" \
    --schema="${SCHEMA_NAME}" \
    -v -z 2>&1 | tee $REPORT_FILE

popd

echo "Report: ${REPORT_FILE}"