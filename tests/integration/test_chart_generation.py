import unittest
import os
import shutil
from typing import NoReturn
from helmgen.main import create_helm_chart

class TestChartGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.test_chart_name: str = "test-integration-chart"
        self.test_env_name: str = "dev"

    def tearDown(self) -> None:
        if os.path.exists(self.test_chart_name):
            shutil.rmtree(self.test_chart_name)

    def test_chart_generation(self) -> None:
        create_helm_chart(self.test_chart_name, self.test_env_name)
        
        # Check if the chart directory was created
        self.assertTrue(os.path.isdir(self.test_chart_name))
        
        # Check if Chart.yaml was created
        self.assertTrue(os.path.isfile(f"{self.test_chart_name}/Chart.yaml"))
        
        # Check if templates directory was created
        self.assertTrue(os.path.isdir(f"{self.test_chart_name}/templates"))
        
        # Check if values.yaml was created
        self.assertTrue(os.path.isfile(f"{self.test_chart_name}/values.yaml"))

if __name__ == '__main__':
    unittest.main()
