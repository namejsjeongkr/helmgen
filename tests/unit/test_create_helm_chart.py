import unittest
from unittest.mock import patch, mock_open, call, Mock
from helmgen.main import create_helm_chart

class TestCreateHelmChart(unittest.TestCase):
    @patch('helmgen.main.os.makedirs')
    @patch('helmgen.main.shutil.copytree')
    @patch('helmgen.main.shutil.copy')
    @patch('builtins.open', new_callable=mock_open, read_data='template content')
    @patch('helmgen.main.Path')
    @patch('helmgen.main.Environment')
    def test_create_helm_chart(self, mock_env, mock_path_class, mock_file, mock_copy, mock_copytree, mock_makedirs):
        # Mock Jinja2 Environment
        mock_env_instance = Mock()
        mock_env.return_value = mock_env_instance
        mock_template = Mock()
        mock_env_instance.get_template.return_value = mock_template
        mock_template.render.return_value = "rendered content"

        # Mock Path
        mock_path = Mock()
        mock_path_class.return_value = mock_path
        mock_path.__truediv__ = Mock(return_value=mock_path)  # __truediv__ 메서드 모킹
        mock_path.parent = mock_path  # parent 속성도 모킹

        chart_name = "test-chart"
        create_helm_chart(chart_name)

        # Verify calls
        mock_makedirs.assert_called_once()
        mock_copytree.assert_called_once()
        mock_copy.assert_called_once()
        mock_env_instance.get_template.assert_called_once_with("Chart.yaml")
        mock_template.render.assert_called_once_with(chart_name=chart_name)
        mock_file.assert_called()
