from hierarchical_index import HierarchicalCodebaseIndex

indexer = HierarchicalCodebaseIndex()
indexer.ingest_repository(".")
print("Test ingestion successful.")
