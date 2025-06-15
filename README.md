# helmgen | Helm Generator

helmgen is a Helm plugin designed to simplify and accelerate the creation of Helm charts.

## Prerequisites

Ensure you have Helm installed. See the [official Helm installation guide](https://helm.sh/docs/intro/install/) for details.


## Python Dependencies

helmgen requires the `jinja2` library for template rendering.  
If you see an error like `ModuleNotFoundError: No module named 'jinja2'`,  
you need to install it for the Python environment used by Helm.

**On macOS or other systems with "externally managed" Python environments (PEP 668), you may need to use the following command:**
```bash
python3 -m pip install --break-system-packages jinja2==3.1.6
```

- If you are using a requirements file:
```bash
python3 -m pip install --break-system-packages -r requirements.txt
```


> **Warning:**  
> The `--break-system-packages` option allows pip to install packages into the system Python environment, which may risk breaking system tools.  
> Use this option only if you understand the risks.  
> For more information, see [PEP 668](https://peps.python.org/pep-0668/).

Alternatively, you can use a [virtual environment](https://docs.python.org/3/library/venv.html):
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```


## Installation

1.  Install the helmgen plugin by running:
```bash
helm plugin install https://github.com/namejsjeongkr/helmgen
```
2.  Verify the installation by running `helm plugin list`. You should see `helmgen` in the list of installed plugins.


## Usage

1.  To create a new Helm chart, execute the following command (replace `my-app` with your desired chart name):
```bash
helm helmgen create <my-app> <ENV>
```
2.  The generated chart will be saved in the `my-app` folder within your current directory.
3.  Review the chart structure and modify it as needed:
```bash
<my-app>/
├── Chart.yaml
├── values.yaml
└── templates/
└── ...
```
4.  To deploy your application using the chart:
```bash
helm install <release-name> <my-app>
```


## Key Features
1.  Automated generation of basic Helm chart structure
2.  Custom template support: Place your custom templates in the `templates/` directory. helmgen supports `.yaml`, `.tpl`, and `.txt` files.
3.  Chart validation

For more detailed usage information and options, use the command `helm helmgen --help`.


## Troubleshooting

### ModuleNotFoundError: No module named 'jinja2'

If you encounter this error on macOS or Ubuntu, your Python environment may be "externally managed."
To fix this, install dependencies with:

```bash
python3 -m pip install --break-system-packages -r requirements.txt
```

If you encounter issues, try the following:

1.  Ensure you have the required Helm version installed.
2.  Verify that the `helmgen.sh` script has execute permissions (`chmod +x helmgen.sh`).
3.  Check the output of `helm plugin install --debug https://github.com/namejsjeongkr/helmgen` for more detailed error messages.


## Customization

helmgen allows you to customize the generated Helm charts to fit your specific deployment needs:

1.  Pre-defined Templates: 
    The `pre-defined-templates` folder contains base templates for various Kubernetes objects. You can modify these templates or add new ones to suit your environment.

2.  Custom Values:
    The `values.yaml` file in the `pre-defined-templates` folder can be customized to set default values for your charts. These values can be overridden during chart installation.

3.  Template Customization:
    In the `pre-defined-templates/templates` directory, you can add or modify Kubernetes object definitions (like Deployments, Services, ConfigMaps, etc.) to match your  application's requirements.

To use your customized templates:

1.  Fork the helmgen repository
2.  Modify the templates in the `pre-defined-templates` folder
3.  Update the `helmgen.sh` script to use your forked repository

This way, you can create Helm charts that are tailored to your specific deployment environment and application needs.
