# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://git.sr.ht/~sthagen/nineties/blob/default/etc/sbom/cdx.json) with SHA256 checksum ([9910f0f6 ...](https://git.sr.ht/~sthagen/nineties/blob/default/etc/sbom/cdx.json.sha256 "sha256:9910f0f67ae7b000c1d4960268fd27eb31188b50cd5468c507c5cfe4033ffb30")).
<!--[[[end]]] (checksum: 3065400f44657d741701673e96b5a5a0)-->
## Licenses 

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                     | Version                                          | License     | Author | Description (from packaging data)                           |
|:-----------------------------------------|:-------------------------------------------------|:------------|:-------|:------------------------------------------------------------|
| [Faker](https://github.com/joke2k/faker) | [20.0.3](https://pypi.org/project/Faker/20.0.3/) | MIT License | joke2k | Faker is a Python package that generates fake data for you. |
<!--[[[end]]] (checksum: a5422a639e3bbb1b9a330008caa05a5e)-->

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
Faker==20.0.3
└── python-dateutil [required: >=2.4, installed: 2.8.2]
    └── six [required: >=1.5, installed: 1.16.0]
````
<!--[[[end]]] (checksum: d11885c258fa1ca57a63722e878c44b9)-->
