#!/bin/bash

create_helm_chart() {
    chart_name=$1
    env_name=$2
    echo "Creating Helm chart: $chart_name for environment: $env_name"
    
    python3 $HELM_PLUGIN_DIR/src/helmgen/main.py $chart_name $env_name
}

if [ "$1" = "create" ]; then
    if [ -z "$2" ] || [ -z "$3" ]; then
        echo "Usage: helm helmgen create <chart-name> <environment>"
        exit 1
    fi
    create_helm_chart $2 $3
else
    echo "Usage: helm helmgen create <chart-name> <environment>"
    exit 1
fi
