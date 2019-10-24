
columns = """
a!columnsLayout(
columns: {{
  {}
}}
)
"""

col = """a!columnLayout(
    contents: {{
        {}
    }}
)"""
def generateSail(groups):
    components = []
    for group in groups:
        if len(group) > 1:
            columnLayouts = [col.format(shape.to_sail_expression()) for shape in group]
            components.append(columns.format(",\n".join(columnLayouts)))
        if len(group) == 1:
            components.append(",\n".join([shape.to_sail_expression() for shape in group]))
    return "{{{}}}".format(",\n".join(components))
