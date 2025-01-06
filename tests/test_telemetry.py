import pytest

from crewai.agent import Agent
from crewai.crew import Crew
from crewai.task import Task
from crewai.telemetry.telemetry import Telemetry
from unittest.mock import MagicMock, patch

class TestTelemetry:
    @patch('crewai.telemetry.telemetry.trace')
    def test_crew_creation(self, mock_trace):
        # Create a mock tracer and span
        mock_tracer = MagicMock()
        mock_span = MagicMock()
        mock_trace.get_tracer.return_value = mock_tracer
        mock_tracer.start_span.return_value = mock_span

        # Create a Telemetry instance
        telemetry = Telemetry()
        telemetry.ready = True
        telemetry.trace_set = True

        # Create a mock Crew
        mock_crew = MagicMock(spec=Crew)
        mock_crew.key = 'test_crew'
        mock_crew.id = '123'
        mock_crew.process = 'sequential'
        mock_crew.memory = True
        mock_crew.tasks = [MagicMock(spec=Task) for _ in range(3)]
        mock_crew.agents = [MagicMock(spec=Agent) for _ in range(2)]
        mock_crew.share_crew = False

        # Call the crew_creation method
        telemetry.crew_creation(mock_crew, {'input1': 'value1'})

        # Assert that the span was created and attributes were set
        mock_tracer.start_span.assert_called_once_with('Crew Created')
        mock_span.set_attribute.assert_any_call('crew_key', 'test_crew')
        mock_span.set_attribute.assert_any_call('crew_id', '123')
        mock_span.set_attribute.assert_any_call('crew_process', 'sequential')
        mock_span.set_attribute.assert_any_call('crew_memory', True)
        mock_span.set_attribute.assert_any_call('crew_number_of_tasks', 3)
        mock_span.set_attribute.assert_any_call('crew_number_of_agents', 2)

        # Assert that the span was ended
        mock_span.end.assert_called_once()