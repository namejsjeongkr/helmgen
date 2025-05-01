import os
import shutil
import sys
from pathlib import Path
from typing import NoReturn
from jinja2 import Environment, FileSystemLoader, Template

def create_helm_chart(chart_name: str, env: str) -> None:
    """
    :param chart_name: chart name
    :param env: (dev/stg/prd)
    """
    project_root: Path = Path(__file__).parent.parent.parent
    template_dir: Path = project_root / "pre-defined-templates"
    
    env_dir: Path = template_dir / env
    if not env_dir.exists():
        raise ValueError(f"Invalid environment: {env}")
    
    env_loader = FileSystemLoader(str(env_dir))
    env_jinja = Environment(loader=env_loader)
    
    new_chart_dir: Path = Path.cwd() / chart_name
    os.makedirs(new_chart_dir, exist_ok=True)

    chart_yaml_template: Template = env_jinja.get_template("Chart.yaml")
    chart_yaml_content: str = chart_yaml_template.render(chart_name=chart_name)
    with open(new_chart_dir / "Chart.yaml", "w") as f:
        f.write(chart_yaml_content)

    env_template_dir: Path = env_dir / "templates"
    shutil.copytree(env_template_dir, new_chart_dir / "templates")

    shutil.copy(env_dir / "values.yaml", new_chart_dir / "values.yaml")

    print(f"[{env}] Helm Chart '{chart_name}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <CHART_NAME> <ENV>")
        sys.exit(1)
    
    chart_name, env = sys.argv[1], sys.argv[2]
    create_helm_chart(chart_name, env)
