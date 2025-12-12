from fastapi.responses import HTMLResponse


def graphiql_html():
    return """
            <!DOCTYPE html>
                <html>
                <head>
                <style>
                    html, body {
                    height: 100%;
                    margin: 0;
                    overflow: hidden;
                    width: 100%;
                    }
                    #graphiql {
                    height: 100vh;
                    }
                </style>
                <link href="//cdn.jsdelivr.net/npm/graphiql@1.4.2/graphiql.css" rel="stylesheet"/>
                <script src="//cdn.jsdelivr.net/npm/react@16.14.0/umd/react.production.min.js"></script>
                <script src="//cdn.jsdelivr.net/npm/react-dom@16.14.0/umd/react-dom.production.min.js"></script>
                <script src="//cdn.jsdelivr.net/npm/subscriptions-transport-ws@0.9.19/browser/client.js"></script>
                <script src="//cdn.jsdelivr.net/npm/graphiql-subscriptions-fetcher@0.0.2/browser/client.js"></script>
                </head>
                <body>
                <script src="//cdn.jsdelivr.net/npm/graphiql@1.4.2/graphiql.min.js"></script>
                <script>
                    // Parse the cookie value for a CSRF token
                    var csrftoken;
                    var cookies = ('; ' + document.cookie).split('; csrftoken=');
                    if (cookies.length == 2)
                    csrftoken = cookies.pop().split(';').shift();

                    // Collect the URL parameters
                    var parameters = {};
                    window.location.search.substr(1).split('&').forEach(function (entry) {
                    var eq = entry.indexOf('=');
                    if (eq >= 0) {
                        parameters[decodeURIComponent(entry.slice(0, eq))] =
                        decodeURIComponent(entry.slice(eq + 1));
                    }
                    });

                    // Produce a Location query string from a parameter object.
                    var graphqlParamNames = {
                    query: true,
                    variables: true,
                    operationName: true
                    };
                    var otherParams = {};
                    for (var k in parameters) {
                    if (parameters.hasOwnProperty(k) && graphqlParamNames[k] !== true) {
                        otherParams[k] = parameters[k];
                    }
                    }
                    
                    function locationQuery(params) {
                    return '?' + Object.keys(params).map(function (key) {
                        return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
                    }).join('&');
                    }

                    var fetchURL = locationQuery(otherParams);

                    // Defines a GraphQL fetcher using the fetch API.
                    function graphQLFetcher(graphQLParams) {
                    var headers = {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    };
                    if (csrftoken) {
                        headers['X-CSRFToken'] = csrftoken;
                    }
                    return fetch(fetchURL, {
                        method: 'post',
                        headers: headers,
                        body: JSON.stringify(graphQLParams),
                        credentials: 'include',
                    }).then(function (response) {
                        return response.text();
                    }).then(function (responseBody) {
                        try {
                        return JSON.parse(responseBody);
                        } catch (error) {
                        return responseBody;
                        }
                    });
                    }

                    // if variables was provided, try to format it.
                    if (parameters.variables) {
                    try {
                        parameters.variables =
                        JSON.stringify(JSON.parse(parameters.variables), null, 2);
                    } catch (e) {
                        // Do nothing, we want to display the invalid JSON as a string, rather
                        // than present an error.
                    }
                    }

                    // When the query and variables string is edited, update the URL bar so
                    // that it can be easily shared
                    function onEditQuery(newQuery) {
                    parameters.query = newQuery;
                    updateURL();
                    }
                    function onEditVariables(newVariables) {
                    parameters.variables = newVariables;
                    updateURL();
                    }
                    function onEditOperationName(newOperationName) {
                    parameters.operationName = newOperationName;
                    updateURL();
                    }
                    function updateURL() {
                    history.replaceState(null, null, locationQuery(parameters));
                    }
                    var subscriptionsEndpoint = (location.protocol === 'http:' ? 'ws' : 'wss') + '://' + location.host + location.pathname;
                    var subscriptionsClient = new window.SubscriptionsTransportWs.SubscriptionClient(subscriptionsEndpoint, {
                    reconnect: true
                    });
                    var fetcher = window.GraphiQLSubscriptionsFetcher.graphQLFetcher(subscriptionsClient, graphQLFetcher);

                    // Render <GraphiQL /> into the body.
                    ReactDOM.render(
                    React.createElement(GraphiQL, {
                        fetcher: fetcher,
                        query: parameters.query,
                        variables: parameters.variables,
                        operationName: parameters.operationName,
                        onEditQuery: onEditQuery,
                        onEditVariables: onEditVariables,
                        onEditOperationName: onEditOperationName,
                    }),
                    document.body
                    );
                </script>
                </body>
                </html>
            """


def custom_graphiql_handler():
    def handler(request):
        return HTMLResponse(graphiql_html())

    return handler
