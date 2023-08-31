from glob import glob
from helpers.stat_to_json import stat_to_json
from helpers.stack import Stack
from helpers.file import File


def cataloguer(searches: list) -> Stack:

    # Create a list of filenames/paths from provided search terms
    paths: list[str] = []
    for search in searches:
        results: list[str] = glob(search, recursive=True)
        for result in results:
            if result[-1] != "/":
                paths.append(result)

    for i in paths:
        print(i)
    print(len(paths))

    # Get metadata for each file in files and add to suitable data structure
    catalogue = Stack()
    for path in paths:
        file = File(
            path=path,
            metadata=stat_to_json(path)
        )
        catalogue.push(file)

    return catalogue
