import os
import shutil
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template

def create_helm_chart(chart_name: str, env: str) -> None:
    """Create Helm chart using project-relative paths"""
    try:
        # Calculate paths relative to script location
        script_dir = Path(__file__).resolve().parent
        project_root = script_dir.parent.parent
        template_dir = project_root / "pre-defined-templates"
        
        # Validate environment
        values_dir = template_dir / "values"
        values_file = values_dir / f"{env}.yaml"
        
        if not values_file.exists():
            valid_envs = [f.stem for f in values_dir.glob("*.yaml")]
            raise ValueError(f"Invalid environment '{env}'. Valid options: {valid_envs}")

        # Create output directory
        chart_dir = Path.cwd() / chart_name
        chart_dir.mkdir(exist_ok=False)
        
        # Generate chart
        env_loader = Environment(loader=FileSystemLoader(str(template_dir)))
        
        # 1. Render Chart.yaml
        chart_content = env_loader.get_template("Chart.yaml").render(
            chart_name=chart_name,
            env=env
        )
        (chart_dir / "Chart.yaml").write_text(chart_content)
        
        # 2. Copy templates
        shutil.copytree(template_dir / "templates", chart_dir / "templates")
        
        # 3. Copy values
        shutil.copy(values_file, chart_dir / "values.yaml")
        
        print(f"Chart created: {chart_dir}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        if chart_dir.exists():
            shutil.rmtree(chart_dir)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <CHART_NAME> <ENVIRONMENT>", file=sys.stderr)
        sys.exit(1)
    
    create_helm_chart(sys.argv[1], sys.argv[2])
