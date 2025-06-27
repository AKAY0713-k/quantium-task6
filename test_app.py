#quantium_task5
import pytest
from dash import Dash
from quantium_task4 import app  # your app must be accessible here


@pytest.mark.usefixtures("dash_duo")
def test_header_present(dash_duo):
    dash_duo.start_server(app)
    assert dash_duo.find_element("h1").text == " Pink Morsel Sales Dashboard"


@pytest.mark.usefixtures("dash_duo")
def test_visualisation_present(dash_duo):
    dash_duo.start_server(app)
    graph = dash_duo.find_element("#sales-line-chart")
    assert graph is not None  # if element with id is found, test passes


@pytest.mark.usefixtures("dash_duo")
def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    radio = dash_duo.find_element("#region-radio")
    assert radio is not None  # ensures the RadioItems component is present


