"""MOTO_DOCKER_LAMBDA_IMAGE, and its per-runtime variant."""

from moto import settings


def test_no_override_returns_none(monkeypatch):
    monkeypatch.delenv("MOTO_DOCKER_LAMBDA_IMAGE", raising=False)
    assert settings.moto_lambda_image() is None
    assert settings.moto_lambda_image("python3.12") is None


def test_global_override_applies_to_every_runtime(monkeypatch):
    monkeypatch.setenv("MOTO_DOCKER_LAMBDA_IMAGE", "mlupin/docker-lambda")
    assert settings.moto_lambda_image() == "mlupin/docker-lambda"
    assert settings.moto_lambda_image("python3.12") == "mlupin/docker-lambda"
    assert settings.moto_lambda_image("nodejs22.x") == "mlupin/docker-lambda"


def test_runtime_specific_override_wins(monkeypatch):
    monkeypatch.setenv("MOTO_DOCKER_LAMBDA_IMAGE", "fallback/image")
    monkeypatch.setenv("MOTO_DOCKER_LAMBDA_IMAGE_PYTHON3_12", "mine/python:3.12")
    monkeypatch.setenv("MOTO_DOCKER_LAMBDA_IMAGE_NODEJS22_X", "mine/nodejs:22.x")

    assert settings.moto_lambda_image("python3.12") == "mine/python:3.12"
    assert settings.moto_lambda_image("nodejs22.x") == "mine/nodejs:22.x"
    # A runtime with no variable of its own still gets the global one.
    assert settings.moto_lambda_image("python3.13") == "fallback/image"
    # And the plain lookup is unchanged.
    assert settings.moto_lambda_image() == "fallback/image"


def test_runtime_specific_override_without_a_global_one(monkeypatch):
    monkeypatch.delenv("MOTO_DOCKER_LAMBDA_IMAGE", raising=False)
    monkeypatch.setenv(
        "MOTO_DOCKER_LAMBDA_IMAGE_PROVIDED_AL2023", "mine/provided:al2023"
    )
    assert settings.moto_lambda_image("provided.al2023") == "mine/provided:al2023"
    assert settings.moto_lambda_image("python3.12") is None
