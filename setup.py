from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

cython_directives = {
    'embedsignature': True,
}

extensions = cythonize([
    Extension(name="config.aircraft_spec_sheet",
              sources=["config/aircraft_spec_sheet.pyx"],
              include_dirs=[]),
    Extension(name="config.coordinates",
              sources=["config/coordinates.pyx"],
              include_dirs=[]),
    Extension(name="src.simulator.app",
              sources=["src/simulator/app.pyx"],
              include_dirs=[]),
    Extension(name="src.simulator.api.api_resolver",
              sources=["src/simulator/api/api_resolver.pyx"],
              include_dirs=[]),
    Extension(name="src.simulator.api.con_connector",
              sources=["src/simulator/api/con_connector.pyx"],
              include_dirs=[]),
    Extension(name="src.simulator.display.components",
              sources=["src/simulator/display/components.pyx"],
              include_dirs=[]),
    Extension(name="src.simulator.display.entities",
              sources=["src/simulator/display/entities.pyx"],
              include_dirs=[]),
    Extension(name="src.simulator.round.operation",
              sources=["src/simulator/round/operation.pyx"],
              include_dirs=[]),
    Extension(name="src.simulator.round.scenario",
              sources=["src/simulator/round/scenario.pyx"],
              include_dirs=[]),
    Extension(name="src.simulator.unit.aircraft",
              sources=["src/simulator/unit/aircraft.pyx"],
              include_dirs=[]),
    Extension(name="src.simulator.unit.locations",
              sources=["src/simulator/unit/locations.pyx"],
              include_dirs=[]),
    Extension(name="src.simulator.unit.unit_table",
              sources=["src/simulator/unit/unit_table.pyx"],
              include_dirs=[])
], compiler_directives=cython_directives)

setup(name="fos_simulator",
      version="1.0.0.0",
      zip_safe=False,             # Without these two options
      include_package_data=True,  # PyInstaller may not find your C-Extensions
      packages=find_packages(),
      ext_modules=extensions)
