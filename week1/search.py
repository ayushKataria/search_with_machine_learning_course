#
# The main search hooks for the Search Flask application.
#
from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from week1.opensearch import get_opensearch

bp = Blueprint('search', __name__, url_prefix='/search')


# Process the filters requested by the user and return a tuple that is appropriate for use in: the query, URLs displaying the filter and the display of the applied filters
# filters -- convert the URL GET structure into an OpenSearch filter query
# display_filters -- return an array of filters that are applied that is appropriate for display
# applied_filters -- return a String that is appropriate for inclusion in a URL as part of a query string.  This is basically the same as the input query string
def process_filters(filters_input):
    # Filters look like: &filter.name=regularPrice&regularPrice.key={{ agg.key }}&regularPrice.from={{ agg.from }}&regularPrice.to={{ agg.to }}
    filters = []
    display_filters = []  # Also create the text we will use to display the filters that are applied
    applied_filters = ""
    for filter in filters_input:
        type = request.args.get(filter + ".type")
        display_name = request.args.get(filter + ".displayName", filter)
        key = request.args.get(filter + ".key")
        #
        # We need to capture and return what filters are already applied so they can be automatically added to any existing links we display in aggregations.jinja2
        applied_filters += "&filter.name={}&{}.type={}&{}.displayName={}&{}.key={}".format(filter, filter, type, filter,
                                                                                 display_name, filter, key)
        #TODO: IMPLEMENT AND SET filters, display_filters and applied_filters.
        # filters get used in create_query below.  display_filters gets used by display_filters.jinja2 and applied_filters gets used by aggregations.jinja2 (and any other links that would execute a search.)
        if type == "range":
            to_filter = request.args.get(filter + ".to") if request.args.get(filter + ".to") else None
            from_filter = request.args.get(filter + ".from") if request.args.get(filter + ".from") else 0
            if to_filter is None:
                filters.append({
                    "range": {
                        filter: {
                            "gte": from_filter
                        }
                    }
                })
            else:
                filters.append({
                    "range": {
                        filter: {
                            "lt": to_filter,
                            "gte": from_filter
                        }
                    }
                })
            display_filters.append(f"Fetching all with {filter} in range from {from_filter} to {to_filter}")
            applied_filters += f"&{filter}.to={to_filter}&{filter}.from={from_filter}"
        elif type == "term":
            filters.append({
                "term": {
                    filter: key
                }
            })
            display_filters.append(f"Fetching all with {filter} as {key}")#TODO: IMPLEMENT
    print("Filters: {}".format(filters))

    return filters, display_filters, applied_filters


# Our main query route.  Accepts POST (via the Search box) and GETs via the clicks on aggregations/facets
@bp.route('/query', methods=['GET', 'POST'])
def query():
    opensearch = get_opensearch() # Load up our OpenSearch client from the opensearch.py file.
    # Put in your code to query opensearch.  Set error as appropriate.
    error = None
    user_query = None
    query_obj = None
    display_filters = None
    applied_filters = ""
    filters = None
    sort = "_score"
    sortDir = "desc"
    pageNo = int(request.args.get("pageNo")) if request.args.get("pageNo") else 0
    pageSize = int(request.args.get("pageSize")) if request.args.get("pageSize") else 10
    if request.method == 'POST':  # a query has been submitted
        user_query = request.form['query']
        if not user_query:
            user_query = "*"
        sort = request.form["sort"]
        if not sort:
            sort = "_score"
        sortDir = request.form["sortDir"]
        if not sortDir:
            sortDir = "desc"
        query_obj = create_query(user_query, [], sort, sortDir)
    elif request.method == 'GET':  # Handle the case where there is no query or just loading the page
        user_query = request.args.get("query", "*")
        sort = request.args.get("sort", sort)
        sortDir = request.args.get("sortDir", sortDir)
    filters_input = request.args.getlist("filter.name")
    if filters_input:
        (filters, display_filters, applied_filters) = process_filters(filters_input)

    query_obj = create_query(user_query, filters, sort, sortDir, pageSize, pageNo)

    print("query obj: {}".format(query_obj))
    response = opensearch.search(index="bbuy_products",body=query_obj)
    # Postprocess results here if you so desire

    #print(response)
    if error is None:
        return render_template("search_results.jinja2", query=user_query, search_response=response,
                               display_filters=display_filters, applied_filters=applied_filters,
                               sort=sort, sortDir=sortDir, pageNo=pageNo, pageSize=pageSize)
    else:
        redirect(url_for("index"))

def create_query(user_query, filters, sort="_score", sortDir="desc", pageSize = 10, pageNo = 0):
    print("Query: {} Filters: {} Sort: {}".format(user_query, filters, sort))
    query_obj = {
        'size': pageSize,
        "from": pageSize * pageNo,
        "track_total_hits": True,
        "sort": {
            sort: sortDir
        },
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "simple_query_string": {
                                    "fields": ["name^10", "description^5", "longDescription", "shortDescription^2", "tags", "features"],
                                    "query": user_query
                                }
                            }
                        ],
                        "filter": filters
                    }
                },
                "boost_mode": "multiply",
                "score_mode": "avg",
                "functions": [
                    {
                        "field_value_factor": {
                            "field": "salesRankLongTerm",
                            "missing": 100000000,
                            "modifier": "reciprocal"
                        }
                    },
                    {
                        "field_value_factor": {
                            "field": "salesRankMediumTerm",
                            "missing": 100000000,
                            "modifier": "reciprocal"
                        }
                    },
                    {
                        "field_value_factor": {
                            "field": "salesRankShortTerm",
                            "missing": 100000000,
                            "modifier": "reciprocal"
                        }
                    }
                ]
            }
        },
        "aggs": {
            "regularPrice": {
                "range": { 
                    "field": "regularPrice",
                    "ranges": [
                        {
                            "to": "100",
                            "key": "$"
                        },
                        {
                            "to": "200",
                            "from": "100",
                            "key": "$$"
                        },
                        {
                            "to": "300",
                            "from": "200",
                            "key": "$$$"
                        },
                        {
                            "to": "400",
                            "from": "300",
                            "key": "$$$$"
                        },
                        {
                            "from": "400",
                            "key": "$$$$$"
                        }
                    ]
                }
            },
            "missing_images": {
                "missing": { "field": "image" }
            }
            ,
            "department": {
                "terms": { "field": "department" }
            }
            #TODO: FILL ME IN
        }
    }
    return query_obj
