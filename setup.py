from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "PIPRELEASEDOC.md").read_text()

setup(name="lag-sdk",
      version="0.3.0",
      author="DanielJiangCloud",
      author_email="daniel.jiang@nbai.io",
      install_requires=["web3==5.31.1", "requests==2.28.1", "requests_toolbelt==0.10.1"],
      packages=["swan_lag","swan_lag.common","swan_lag.api"],
      license="MIT",
      include_package_data=True,
      description="A python software development kit for Lagrange services",
      long_description=long_description,
      long_description_content_type='text/markdown',
      )
