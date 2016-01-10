from flask.ext.restful import reqparse

# GET request parser
post_get_parser = reqparse.RequestParser()

post_get_parser.add_argument(
        'page',
        type=int,
        location=['args', 'headers'],
        required=False
        )

post_get_parser.add_argument(
        'username',
        type=str,
        location=['json', 'args', 'headers']
        )

# POST request parser
post_post_parser = reqparse.RequestParser()

post_post_parser.add_argument(
        'username',
        type=str,
        required=True,
        help="Username is required"
        )

post_post_parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password is required"
        )

post_post_parser.add_argument(
        'title',
        type=str,
        required=True,
        help="Title is required"
        )

post_post_parser.add_argument(
        'text',
        type=str,
        required=True,
        help="Body Text is required"
        )

post_post_parser.add_argument(
        'tags',
        type=str,
        action='append'
        )

# PUT request parser
post_put_parser = reqparse.RequestParser()
post_put_parser.add_argument(
        'username',
        type=str,
        required=True,
        help="Username is required"
        )

post_put_parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password is required"
        )

post_put_parser.add_argument(
        'title',
        type=str
        )

post_put_parser.add_argument(
        'text',
        type=str
        )

post_put_parser.add_argument(
        'tags',
        type=str,
        action='append'
        )
