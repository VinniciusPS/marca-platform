from itertools import islice

class GoogleTrendsManager:
    def __init__(self, extractor, mapper, handler):
        self.extractor = extractor
        self.mapper = mapper
        self.handler = handler

    def run(self, query, keyword_groups, timeframe):
        raw_stream = self.extractor.fetch_stream(keyword_groups, timeframe)
        storage_stream = self.mapper.transform_stream(raw_stream)

        it = iter(storage_stream)
        total = 0
        while True:
            batch = [record.model_dump() for record in islice(it, self.handler.batch_size)]
            if not batch:
                break
            total += self.handler.execute_upsert(query, batch)
        return total