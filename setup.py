from setuptools import setup, find_packages

setup(
    name = "todo api test",
    version = "0.1.0",
    author = "Zhou Li",
    author_email = "zhoulijoe@gmail.com",
    description = ("api test against todo server"),
    license = "MIT",
    url = "https://github.com/zhoulijoe/python_todo_api_test.git",
    packages = find_packages(),
    setup_requires = ["requests"]
)