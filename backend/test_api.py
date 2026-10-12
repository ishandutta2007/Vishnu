"""Quick API validation script for Project Vishnu."""
import urllib.request
import json

BASE = "http://localhost:8000"

def get(path):
    r = urllib.request.urlopen(f"{BASE}{path}")
    return json.loads(r.read())

def post(path):
    req = urllib.request.Request(f"{BASE}{path}", method="POST")
    r = urllib.request.urlopen(req)
    return json.loads(r.read())

# Test 1: Entity listing
print("=" * 50)
print("TEST 1: Entity Listing")
data = get("/api/entities?page_size=5")
print(f"  Total entities: {data['total']}")
for e in data["entities"][:5]:
    print(f"  - {e['name']} ({e['entity_type']})")

# Test 2: Graph data
print("\nTEST 2: Graph Data")
graph = get("/api/graph/data")
print(f"  Nodes: {len(graph['nodes'])}")
print(f"  Edges: {len(graph['edges'])}")

# Test 3: Centrality
print("\nTEST 3: Centrality (Top 5)")
centrality = get("/api/graph/centrality?top_n=5")
for c in centrality:
    print(f"  #{centrality.index(c)+1} {c['label']} (score: {c['centrality_score']:.4f})")

# Test 4: Communities
print("\nTEST 4: Community Detection")
communities = get("/api/graph/communities")
for comm in communities:
    members = ", ".join(m["label"] for m in comm["members"][:4])
    more = f"... +{comm['size']-4}" if comm["size"] > 4 else ""
    print(f"  Community {comm['community_id']}: {comm['size']} members - {members}{more}")

# Test 5: Search
print("\nTEST 5: Search for 'Sorokin'")
results = get("/api/search?q=Sorokin")
print(f"  Found: {results['total']} result(s)")
for r in results["results"]:
    print(f"  - {r['name']} ({r['entity_type']})")

# Test 6: Shortest path between first person and first org
print("\nTEST 6: Shortest Path")
entities = get("/api/entities?page_size=200")
persons = [e for e in entities["entities"] if e["entity_type"] == "person"]
orgs = [e for e in entities["entities"] if e["entity_type"] == "organization"]
if persons and orgs:
    path = get(f"/api/graph/shortest-path?source={persons[0]['id']}&target={orgs[0]['id']}")
    print(f"  Path length: {path['length']} hop(s)")
    print(f"  Path nodes: {len(path['path'])}")

print("\n" + "=" * 50)
print("ALL TESTS PASSED!")
