from setuptools import setup, find_packages
#from adept.globals import VERSION

# 

with open("README.md", "r") as fh:
    long_description = fh.read()

extras = {
    "profiler": ["pyinstrument>=2.0"],
}
test_deps = ["pytest"]

all_deps = []
for group_name in extras:
    all_deps += extras[group_name]
all_deps = all_deps + test_deps
extras["all"] = all_deps


setup(
    name="randomXML",
    #version=VERSION,
    author="heron",
    author_email="kristina.landino@heronsystems.com",
    description="XML Creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/heronsystems/kmland23",
    license="GNU",
    python_requires=">=3.7.6",
    packages=find_packages(),
    install_requires=[
        "mkl-random>=1.1.0",
    ],
    test_requires=test_deps,
    extras_require=extras,
    include_package_data=True,
)



