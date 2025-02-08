import os
import shutil
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def create_helm_chart(chart_name):
    """
    Create a new Helm chart based on pre-defined templates.
    
    :param chart_name: Name of the new Helm chart
    """
    project_root = Path(__file__).parent.parent.parent
    template_dir = project_root / "pre-defined-templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))

    new_chart_dir = Path.cwd() / chart_name
    os.makedirs(new_chart_dir, exist_ok=True)

    chart_yaml_template = env.get_template("Chart.yaml")
    chart_yaml_content = chart_yaml_template.render(chart_name=chart_name)
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
    
    chart_name = sys.argv[1]
    create_helm_chart(chart_name)
