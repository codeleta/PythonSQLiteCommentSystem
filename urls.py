import views

url_routes = {
    '/comment/': views.add_comment,
    '/view/': views.list_comments,
    '/stat/': views.stat_comments,
    '/get_cities/': views.get_cities_json,
}