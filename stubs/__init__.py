"""Local stubs to satisfy heavy external dependencies for offline testing.

This package intentionally keeps the top-level __init__ minimal to avoid
circular import problems. Individual stubs are imported by name when needed
(e.g. `import transformers` will resolve to the top-level proxy which in
turn imports `stubs.transformers`).
"""


