import os
import shutil
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template

def create_helm_chart(chart_name: str, env_name: str) -> None:
    """
    Create a new Helm chart based on pre-defined templates for a specific environment.
    
    :param chart_name: Name of the new Helm chart
    :param env_name: Name of the environment (dev, stg, prd)
    """
    project_root = Path(__file__).parent.parent.parent
    template_dir = project_root / "pre-defined-templates"
    env_dir = template_dir / env_name

    if not env_dir.exists() or not env_dir.is_dir():
        print(f"[ERROR] Environment '{env_name}' not found in pre-defined templates.")
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(str(env_dir)))
    new_chart_dir = Path.cwd() / chart_name
    os.makedirs(new_chart_dir, exist_ok=True)

    shutil.copytree(env_dir, new_chart_dir, dirs_exist_ok=True)

    chart_yaml_template = env.get_template("Chart.yaml")
    chart_yaml_content = chart_yaml_template.render(
        chart_name=chart_name,
        env_name=env_name
    )
    with open(new_chart_dir / "Chart.yaml", "w") as f:
        f.write(chart_yaml_content)

    print(f"Helm Chart '{chart_name}' for environment '{env_name}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python main.py <new_chart_name> <environment>\n"
            "Supported environments: dev, stg, prd"
        )
        sys.exit(1)
    
    chart_name = sys.argv[1]
    env_name = sys.argv[2]
    create_helm_chart(chart_name, env_name)
