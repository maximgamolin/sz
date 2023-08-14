from pathlib import Path

from py_md_doc import PyMdDoc

if __name__ == '__main__':
    md = PyMdDoc(input_directory=Path("./app/framework"), files=[
        "data_access_layer/repository.py",
    ])
    md.get_docs(output_directory=Path("./docs/framework/data_access_layer"))

    md = PyMdDoc(input_directory=Path("./app/framework/data_access_layer/order_object"), files=[
        "base.py",
        "values.py",
    ])
    md.get_docs(output_directory=Path("./docs/framework/data_access_layer/order_object"))
    md = PyMdDoc(input_directory=Path("./app/framework/data_access_layer/query_object"), files=[
        "base.py",
        "values.py",
    ])
    md.get_docs(output_directory=Path("./docs/framework/data_access_layer/query_object"))