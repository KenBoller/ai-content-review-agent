from graph.workflow import graph

article = """
WordPress is a powerfull website platform.
It are used by many companys around the world.
"""

result = graph.invoke({
    "article": article
})

print(result)