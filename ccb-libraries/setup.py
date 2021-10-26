import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ccb_toolbox',
    version='0.0.2',
    author='Eduardo Yanez',
    author_email='con_eyanez@credicorpbank.com',
    description='CCB Python Toolkit',
    long_description='Bibliotecas de rutinas en Python para las funciones Lambda de CCB.',
    long_description_content_type="text/markdown",
    url='https://github.com/ccb-ejyanezp/ccb-libraries.git',
    project_urls = {
        "Bug Tracker": "https://github.com/ccb-ejyanezp/ccb-libraries/issues"
    },
    license='MIT',
    packages=['ccb_toolbox'],
    install_requires=[]
)
