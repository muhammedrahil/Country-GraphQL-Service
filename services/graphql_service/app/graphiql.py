from fastapi.responses import HTMLResponse


def graphiql_html():
    return HTMLResponse(
        """
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8" />
                <title>GraphiQL</title>
                <link rel="stylesheet"
                href="https://cdn.jsdelivr.net/npm/graphiql@2.0.9/graphiql.min.css" />
                <script crossorigin
                src="https://cdn.jsdelivr.net/npm/react@18/umd/react.development.js"></script>
                <script crossorigin
                src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.development.js"></script>
                <script
                src="https://cdn.jsdelivr.net/npm/graphiql@2.0.9/graphiql.min.js"></script>
            </head>

            <body style="margin:0;">
                <div id="graphiql" style="height:100vh;"></div>

                <script>
                    const fetcher = GraphiQL.createFetcher({ url: "/graphql" });
                    ReactDOM.render(
                        React.createElement(GraphiQL, { fetcher: fetcher }),
                        document.getElementById("graphiql")
                    );
                </script>
            </body>

            </html>
            """
    )
