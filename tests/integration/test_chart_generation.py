import unittest
import os
import shutil
from helmgen.main import create_helm_chart

class TestChartGeneration(unittest.TestCase):
    def setUp(self):
        self.test_chart_name = "test-integration-chart"

    def tearDown(self):
        if os.path.exists(self.test_chart_name):
            shutil.rmtree(self.test_chart_name)

    def test_chart_generation(self):
        create_helm_chart(self.test_chart_name)
        
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
