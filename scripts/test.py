from services.search_service import search_query

results = search_query("compiler design optimization")

for r in results:
    print(r)
