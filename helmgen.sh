#!/bin/bash

create_helm_chart() {
    chart_name=$1
    env_name=$2
    echo "Creating Helm chart: $chart_name for environment: $env_name"
    
    python_script_path="$HELM_PLUGIN_DIR/src/helmgen/main.py"
    if [ ! -f "$python_script_path" ]; then
        echo "CRITICAL ERROR: Python script not found at $python_script_path"
        exit 1
    fi

    if ! python3 "$python_script_path" "$chart_name" "$env_name"; then
        echo "Error: Chart creation failed for environment '$env_name'"
        exit 1
    fi
}

if [ "$#" -ne 3 ] || [ "$1" != "create" ]; then
    echo "Usage: helm helmgen create <CHART_NAME> <ENVIRONMENT>"
    exit 1
fi

create_helm_chart "$2" "$3"
