import os
import shutil
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template

def create_helm_chart(chart_name: str, env: str) -> None:
    """Create a Helm chart with environment-specific configuration."""
    
    # Get plugin root from Helm environment
    helm_plugin_dir = os.environ.get("HELM_PLUGIN_DIR")
    if not helm_plugin_dir:
        print("❌ HELM_PLUGIN_DIR environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Configure paths using Helm plugin directory
    template_dir = Path(helm_plugin_dir) / "pre-defined-templates"
    env_dir = template_dir / env

    # Debug output for path verification
    print(f"[DEBUG] Using template directory: {template_dir}")
    print(f"[DEBUG] Checking environment directory: {env_dir}")

    # Validate template structure
    if not template_dir.exists():
        print(f"❌ Template directory missing: {template_dir}", file=sys.stderr)
        sys.exit(1)
    if not env_dir.exists():
        print(f"❌ Invalid environment '{env}'. Valid options: dev, stg, prd", file=sys.stderr)
        sys.exit(1)

    # Initialize Jinja environment
    env_loader = FileSystemLoader(str(env_dir))
    jinja_env = Environment(loader=env_loader)

    # Create chart directory
    chart_dir = Path.cwd() / chart_name
    chart_dir.mkdir(exist_ok=True)

    # Generate Chart.yaml
    try:
        chart_template = jinja_env.get_template("Chart.yaml")
        chart_content = chart_template.render(chart_name=chart_name)
        (chart_dir / "Chart.yaml").write_text(chart_content)
    except Exception as e:
        print(f"❌ Failed to generate Chart.yaml: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Copy templates
    templates_src = env_dir / "templates"
    templates_dest = chart_dir / "templates"
    try:
        shutil.copytree(templates_src, templates_dest)
    except Exception as e:
        print(f"❌ Failed to copy templates: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Copy values.yaml
    values_file = env_dir / "values.yaml"
    try:
        shutil.copy(values_file, chart_dir / "values.yaml")
    except Exception as e:
        print(f"❌ Failed to copy values.yaml: {str(e)}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Successfully created '{chart_name}' chart for {env} environment")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <CHART_NAME> <ENV>", file=sys.stderr)
        sys.exit(1)
    
    create_helm_chart(sys.argv[1], sys.argv[2])
