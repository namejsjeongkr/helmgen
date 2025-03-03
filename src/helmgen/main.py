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
    env = Environment(loader=FileSystemLoader(str(template_dir)))

    new_chart_dir = Path.cwd() / chart_name
    os.makedirs(new_chart_dir, exist_ok=True)

    # Copy environment-specific files
    env_dir = template_dir / env_name
    if env_dir.exists():
        shutil.copytree(env_dir, new_chart_dir, dirs_exist_ok=True)
    else:
        print(f"Environment '{env_name}' not found. Using default templates.")
        shutil.copytree(template_dir / "templates", new_chart_dir / "templates")
        shutil.copy(template_dir / "values.yaml", new_chart_dir / "values.yaml")

    # Render Chart.yaml
    chart_yaml_template = env.get_template("Chart.yaml")
    chart_yaml_content = chart_yaml_template.render(chart_name=chart_name, env_name=env_name)
    with open(new_chart_dir / "Chart.yaml", "w") as f:
        f.write(chart_yaml_content)

    print(f"Helm Chart '{chart_name}' for environment '{env_name}' creation completed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python main.py <new_chart_name> <environment>\n"
            "Please provide the name for the new Helm chart and the environment (dev, stg, prd)."
        )
        sys.exit(1)
    
    chart_name = sys.argv[1]
    env_name = sys.argv[2]
    create_helm_chart(chart_name, env_name)
