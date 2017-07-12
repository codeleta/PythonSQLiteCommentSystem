from controllers import routes

url_routes = {
    '/': routes.index,
    '/comment/': routes.add_comment,
    '/view/': routes.list_comments,
    '/stat/': routes.stat_comments,
    '/get_cities/': routes.get_cities_json,
}
