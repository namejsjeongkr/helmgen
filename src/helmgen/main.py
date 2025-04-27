import os
import shutil
import sys
from pathlib import Path

def create_helm_chart(chart_name: str, env_name: str) -> None:
    """Create Helm chart for specified environment"""
    
    # 1. Resolve absolute project root
    try:
        project_root = Path(__file__).resolve().parents[2]
    except Exception:
        project_root = Path(os.getcwd())
    
    # 2. Validate environment directory
    env_dir = project_root / "pre-defined-templates" / env_name
    if not (env_dir.exists() and env_dir.is_dir()):
        valid_envs = [d.name for d in (project_root/"pre-defined-templates").iterdir() if d.is_dir()]
        print(f"Error: Invalid environment '{env_name}'\nValid environments: {valid_envs}")
        sys.exit(1)

    # 3. Validate output directory
    output_dir = Path.cwd() / chart_name
    if output_dir.exists():
        print(f"Error: Output directory '{output_dir}' already exists")
        sys.exit(1)

    # 4. Copy templates
    try:
        shutil.copytree(env_dir, output_dir)
        print(f"Created chart '{chart_name}' in {output_dir}")
    except Exception as e:
        print(f"Error: {str(e)}")
        if output_dir.exists():
            shutil.rmtree(output_dir)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <CHART_NAME> <ENVIRONMENT>")
        sys.exit(1)
        
    create_helm_chart(sys.argv[1], sys.argv[2])
