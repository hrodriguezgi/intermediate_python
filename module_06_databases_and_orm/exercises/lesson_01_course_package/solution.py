from module_06_packages_and_sqlite.shared.text_tools import slugify


def build_module_names(names: list[str]) -> list[str]:
    return [slugify(name) for name in names]


if __name__ == "__main__":
    print(build_module_names(["Python Foundations", "Files and JSON"]))
