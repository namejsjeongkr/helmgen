import os
import shutil
import sys

from jinja2 import Environment, FileSystemLoader


def create_helm_chart(chart_name):
    """
    Create a new Helm chart based on pre-defined templates.
    
    :param chart_name: Name of the new Helm chart
    """
    template_dir = "./pre-defined-templates"
    env = Environment(loader=FileSystemLoader(template_dir))

    new_chart_dir = f"./{chart_name}"
    os.makedirs(new_chart_dir, exist_ok=True)

    chart_yaml_template = env.get_template("Chart.yaml")
    chart_yaml_content = chart_yaml_template.render(chart_name=chart_name)
    with open(f"{new_chart_dir}/Chart.yaml", "w") as f:
        f.write(chart_yaml_content)

    shutil.copytree(f"{template_dir}/templates", f"{new_chart_dir}/templates")
    shutil.copy(f"{template_dir}/values.yaml", f"{new_chart_dir}/values.yaml")

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
