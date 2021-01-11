def app(env, start_response):
    d = env['QUERY_STRING']
    out = d.replace('&', '\n').encode('utf-8')
    start_response('200 OK', [('Content-Type', 'text/plain')])

    return [out]
