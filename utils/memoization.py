from functools import lru_cache


def memoize_lists(func):
    """
    Mémoïse une méthode d’instance, transforme automatiquement les listes en tuples.
    Ignore self pour le cache.
    """
    # Création d’un cache séparé
    # La vraie fonction appelée inclut self, mais le cache ignore self
    cached = lru_cache(maxsize=1000)(
        lambda *args, **kwargs: func(*args, **kwargs)
    )

    def wrapper(self, *args, **kwargs):
        # transforme les listes en tuples dans args
        hashable_args = tuple(tuple(a) if isinstance(a, list) else a for a in args)
        # transforme les listes en tuples dans kwargs et trie pour ordre stable
        hashable_kwargs = tuple(
            (k, tuple(v) if isinstance(v, list) else v)
            for k, v in sorted(kwargs.items())
        )
        # Appelle la vraie fonction en incluant self
        return cached(self, *hashable_args, **dict(hashable_kwargs))

    return wrapper
