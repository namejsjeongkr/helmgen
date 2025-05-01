import os
import shutil
import sys
from pathlib import Path
from typing import NoReturn
from jinja2 import Environment, FileSystemLoader, Template

def create_helm_chart(chart_name: str) -> None:
    """
    Create a new Helm chart based on pre-defined templates.
    
    :param chart_name: Name of the new Helm chart
    """
    project_root: Path = Path(__file__).parent.parent.parent
    template_dir: Path = project_root / "pre-defined-templates"
    env: Environment = Environment(loader=FileSystemLoader(str(template_dir)))

    new_chart_dir: Path = Path.cwd() / chart_name
    os.makedirs(new_chart_dir, exist_ok=True)

    chart_yaml_template: Template = env.get_template("Chart.yaml")
    chart_yaml_content: str = chart_yaml_template.render(chart_name=chart_name)
    with open(new_chart_dir / "Chart.yaml", "w") as f:
        f.write(chart_yaml_content)

    shutil.copytree(template_dir / "templates", new_chart_dir / "templates")
    shutil.copy(template_dir / "values.yaml", new_chart_dir / "values.yaml")

    print(f"Helm Chart '{chart_name}' creation completed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python main.py <new_chart_name>\n"
            "Please provide the name for the new Helm chart."
        )
        sys.exit(1)
    
    chart_name: str = sys.argv[1]
    create_helm_chart(chart_name)
