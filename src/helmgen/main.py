import os
import shutil
import sys
from pathlib import Path
from typing import NoReturn
from jinja2 import Environment, FileSystemLoader, Template

def create_helm_chart(chart_name: str, env: str) -> None:
    """
    Create a new Helm chart with environment-specific configuration.

    :param chart_name: Name of the new Helm chart
    :param env: Target environment (dev/stg/prd)
    """
    
    project_root: Path = Path(__file__).parent.parent.parent
    template_dir: Path = project_root / "pre-defined-templates"

    if not template_dir.exists():
        print(f"[ERROR] Template directory not found: {template_dir}", file=sys.stderr)
        sys.exit(1)

    env_dir: Path = template_dir / env
    print(f"[DEBUG] Checking environment directory: {env_dir}")
    if not env_dir.exists():
        print(f"[ERROR] Invalid environment: {env} (Path: {env_dir})", file=sys.stderr)
        sys.exit(1)

    env_loader = FileSystemLoader(str(env_dir))
    env_jinja = Environment(loader=env_loader)

    new_chart_dir: Path = Path.cwd() / chart_name
    os.makedirs(new_chart_dir, exist_ok=True)

    try:
        chart_yaml_template: Template = env_jinja.get_template("Chart.yaml")
        chart_yaml_content: str = chart_yaml_template.render(chart_name=chart_name)
        with open(new_chart_dir / "Chart.yaml", "w") as f:
            f.write(chart_yaml_content)
    except Exception as e:
        print(f"[ERROR] Failed to render Chart.yaml: {e}", file=sys.stderr)
        sys.exit(1)

    env_template_dir: Path = env_dir / "templates"
    if not env_template_dir.exists():
        print(f"[ERROR] templates directory not found in {env_dir}", file=sys.stderr)
        sys.exit(1)
    try:
        shutil.copytree(env_template_dir, new_chart_dir / "templates")
    except Exception as e:
        print(f"[ERROR] Failed to copy templates: {e}", file=sys.stderr)
        sys.exit(1)

    env_values_path: Path = env_dir / "values.yaml"
    if not env_values_path.exists():
        print(f"[ERROR] values.yaml not found in {env_dir}", file=sys.stderr)
        sys.exit(1)
    try:
        shutil.copy(env_values_path, new_chart_dir / "values.yaml")
    except Exception as e:
        print(f"[ERROR] Failed to copy values.yaml: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[{env}] Helm Chart '{chart_name}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <CHART_NAME> <ENV>", file=sys.stderr)
        sys.exit(1)

    chart_name, env = sys.argv[1], sys.argv[2]
    create_helm_chart(chart_name, env)
