# [[[fill git_describe()]]]
__version__ = '2022.7.24+parent.a35bd82d'
# [[[end]]] (checksum: 4b24cff310f022c94c50d2979b85c7d5)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
