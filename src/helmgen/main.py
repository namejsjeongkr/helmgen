import os
import shutil
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template

def create_helm_chart(chart_name: str, env: str) -> None:
    """Create a Helm chart using shared templates and environment-specific values."""

    # Validate Helm plugin environment
    helm_plugin_dir = os.environ.get("HELM_PLUGIN_DIR")
    if not helm_plugin_dir:
        print("Error: HELM_PLUGIN_DIR environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Configure template paths
    template_dir = Path(helm_plugin_dir) / "pre-defined-templates"
    values_file = template_dir / "values" / f"{env}.yaml"
    chart_template = template_dir / "Chart.yaml"

    # Validate required resources
    if not template_dir.exists():
        print(f"Error: Template directory not found at {template_dir}", file=sys.stderr)
        sys.exit(1)
        
    if not values_file.exists():
        valid_envs = [f.stem for f in (template_dir / "values").glob("*.yaml")]
        print(f"Error: Invalid environment '{env}'. Valid options: {valid_envs}", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    chart_dir = Path.cwd() / chart_name
    try:
        chart_dir.mkdir(exist_ok=False)
    except FileExistsError:
        print(f"Error: Output directory '{chart_name}' already exists", file=sys.stderr)
        sys.exit(1)

    # Initialize template engine
    jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))

    try:
        # Generate Chart.yaml from template
        chart_template = jinja_env.get_template("Chart.yaml")
        (chart_dir / "Chart.yaml").write_text(
            chart_template.render(chart_name=chart_name)
        )
        
        # Copy shared templates
        shutil.copytree(
            template_dir / "templates",
            chart_dir / "templates"
        )
        
        # Copy environment-specific values
        shutil.copy(values_file, chart_dir / "values.yaml")
        
    except Exception as e:
        # Cleanup on failure
        shutil.rmtree(chart_dir, ignore_errors=True)
        print(f"Error: Chart creation failed - {str(e)}", file=sys.stderr)
        sys.exit(1)

    print(f"Success: Created Helm chart '{chart_name}' for {env} environment")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <CHART_NAME> <ENVIRONMENT>", file=sys.stderr)
        sys.exit(1)
    
    create_helm_chart(sys.argv[1], sys.argv[2])
