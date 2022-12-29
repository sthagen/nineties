# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://git.sr.ht/~sthagen/nineties/blob/default/sbom.json) with SHA256 checksum ([6ea7aad1 ...](https://git.sr.ht/~sthagen/nineties/blob/default/sbom.json.sha256 "sha256:6ea7aad144264ef5553871367407bd83afdd79f7dd9c0a42e1d6d32c6c5a735a")).
<!--[[[end]]] (checksum: 94c0adee16f418aac4d44f45c466f8d5)-->
## Licenses 

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                     | Version                                          | License     | Author | Description (from packaging data)                           |
|:-----------------------------------------|:-------------------------------------------------|:------------|:-------|:------------------------------------------------------------|
| [Faker](https://github.com/joke2k/faker) | [15.3.4](https://pypi.org/project/Faker/15.3.4/) | MIT License | joke2k | Faker is a Python package that generates fake data for you. |
<!--[[[end]]] (checksum: d8723207997d9da475463d587f2b5c6e)-->

### Indirect Dependencies

<!--[[[fill indirect_dependencies_table()]]]-->
| Name                                                    | Version                                                  | License                              | Author            | Description (from packaging data)                 |
|:--------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------|:------------------|:--------------------------------------------------|
| [python-dateutil](https://github.com/dateutil/dateutil) | [2.8.2](https://pypi.org/project/python-dateutil/2.8.2/) | Apache Software License; BSD License | Gustavo Niemeyer  | Extensions to the standard Python datetime module |
| [six](https://github.com/benjaminp/six)                 | [1.16.0](https://pypi.org/project/six/1.16.0/)           | MIT License                          | Benjamin Peterson | Python 2 and 3 compatibility utilities            |
<!--[[[end]]] (checksum: 00a948c12430d4d365bb94e765e727f0)-->

## Dependency Tree(s)

JSON file with the complete package dependency tree info of: [the full dependency tree](package-dependency-tree.json)

### Rendered SVG

Base graphviz file in dot format: [Trees of the direct dependencies](package-dependency-tree.dot.txt)

<img src="./package-dependency-tree.svg" alt="Trees of the direct dependencies" title="Trees of the direct dependencies"/>

### Console Representation

<!--[[[fill dependency_tree_console_text()]]]-->
````console
Faker==15.3.4
  - python-dateutil [required: >=2.4, installed: 2.8.2]
    - six [required: >=1.5, installed: 1.16.0]
````
<!--[[[end]]] (checksum: d85a1bf42d766d295938fc19763abbd7)-->
