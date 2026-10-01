"""End-to-end UI tests using Streamlit's AppTest (no browser needed)."""
import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from tests.conftest import ROOT


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setenv("MATEIS_DB_PATH", str(tmp_path / "ui.db"))
    st.cache_resource.clear()
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=90).run()


def candidates(app):
    return [m.value for m in app.metric if m.label == "Candidates left"][0]


def test_app_starts_without_errors(app):
    assert not app.exception
    assert candidates(app) == "26 of 26"


def test_strength_filter_reduces_candidates(app):
    app.number_input(key="f_strength_min").set_value(200).run()
    assert not app.exception
    n = int(candidates(app).split()[0])
    assert 0 < n < 26


def test_min_greater_than_max_shows_error_not_crash(app):
    app.number_input(key="f_modulus_min").set_value(100).run()
    app.number_input(key="f_modulus_max").set_value(10).run()
    assert not app.exception
    assert any("greater than maximum" in e.value for e in app.sidebar.error)


def test_impossible_constraints_show_friendly_warning(app):
    app.number_input(key="f_strength_min").set_value(50_000).run()
    assert not app.exception
    assert any("No material meets every constraint" in w.value for w in app.warning)


def test_empty_class_selection_is_handled(app):
    app.multiselect(key="f_classes").set_value([]).run()
    assert not app.exception
    assert any("at least one material class" in e.value for e in app.sidebar.error)


def test_changing_objective_changes_formula(app):
    app.selectbox(key="index_key").set_value("cheap_strong_beam").run()
    assert not app.exception
    assert any("Cv" in m.value for m in app.markdown)


def test_custom_axes_work(app):
    app.radio(key="axes_mode").set_value("Custom axes").run()
    assert not app.exception
