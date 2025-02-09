#!/bin/bash

create_helm_chart() {
    chart_name=$1
    echo "Creating Helm chart: $chart_name"
    
    helm create $chart_name
}

if [ "$1" = "create" ]; then
    if [ -z "$2" ]; then
        echo "Error: Chart name is required"
        exit 1
    fi
    create_helm_chart $2
else
    echo "Usage: helm helmgen create <chart-name>"
    exit 1
fi
