from src.app import app, hashtags_counts_table


@app.page('/{hashtag}/count')
@app.table_route(table=hashtags_counts_table, match_info='hashtag')
async def hashtag_count(self, request, hashtag):
    return self.json({
        'hashtag': hashtag,
        'count': hashtags_counts_table[hashtag],
    })


@app.page('/hashtags')
async def hashtags(self, request):
    return self.json({'hashtags': list(hashtags_counts_table.keys())})
