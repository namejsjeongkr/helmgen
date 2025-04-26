import os
import shutil
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template

def create_helm_chart(chart_name: str, env_name: str) -> None:
    """Create Helm chart for specified environment"""
    
    # 1. Validate environment directory
    project_root = Path(__file__).resolve().parent.parent.parent
    env_dir = project_root / "pre-defined-templates" / env_name
    
    if not env_dir.exists():
        print(f"Error: Environment '{env_name}' directory does not exist")
        print(f"Valid environments: {list_env_directories(project_root)}")
        sys.exit(1)

    # 2. Validate output directory
    output_dir = Path.cwd() / chart_name
    if output_dir.exists():
        print(f"Error: Output directory '{chart_name}' already exists")
        sys.exit(1)

    # 3. Copy environment templates
    try:
        shutil.copytree(env_dir, output_dir)
        post_process_chart(output_dir, chart_name, env_name)
    except Exception as e:
        if output_dir.exists():
            shutil.rmtree(output_dir)
        print(f"Error: Chart creation failed - {str(e)}")
        sys.exit(1)

    print(f"Success: Created chart '{chart_name}' for {env_name} environment")

def list_env_directories(project_root: Path) -> list:
    """List available environment directories"""
    template_dir = project_root / "pre-defined-templates"
    return [d.name for d in template_dir.iterdir() if d.is_dir()]

def post_process_chart(chart_dir: Path, chart_name: str, env_name: str) -> None:
    """Finalize chart metadata"""
    chart_file = chart_dir / "Chart.yaml"
    content = chart_file.read_text()
    
    # Replace placeholders (if any)
    content = content.replace("{{ chart_name }}", chart_name)
    content = content.replace("{{ env_name }}", env_name)
    
    chart_file.write_text(content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <CHART_NAME> <ENV_NAME>")
        sys.exit(1)
    
    create_helm_chart(sys.argv[1], sys.argv[2])
