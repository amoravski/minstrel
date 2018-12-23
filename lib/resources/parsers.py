from flask_restful import reqparse

"""
    Contains all the different request parsers
"""

# The parser for any type of user
user_parser = reqparse.RequestParser()
user_parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
user_parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
user_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

# The parser for performer registration
performer_parser = reqparse.RequestParser()
performer_parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
performer_parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
performer_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
performer_parser.add_argument('location',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
performer_parser.add_argument('categories',
                        required=True,
                        help="You must at least choose one category",
                        action="append"
                        )
# The parser for performer settings
performer_settings_parser = reqparse.RequestParser()
performer_settings_parser.add_argument('settings',
                        type=dict,
                        required=True,
                        )


# The parser for admirer registration
admirer_parser = reqparse.RequestParser()
admirer_parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
admirer_parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
admirer_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
admirer_parser.add_argument('preferred_categories',
                        required=True,
                        help="This field cannot be left blank!",
                        action="append"
                        )


# The parser for performer settings
admirer_settings_parser = reqparse.RequestParser()
admirer_settings_parser.add_argument('settings',
                        type=dict,
                        required=True,
                        )


# The parser for events
event_parser = reqparse.RequestParser()
event_parser.add_argument('text',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

# The parser for offers
offer_parser = reqparse.RequestParser()
offer_parser.add_argument('text',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
offer_parser.add_argument('location',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
offer_parser.add_argument('date',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
offer_parser.add_argument('categories',
                        required=True,
                        help="This field cannot be left blank!",
                        action="append"
                        )
offer_parser.add_argument('type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
offer_parser.add_argument('requirements',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
offer_parser.add_argument('compensation',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
offer_parser.add_argument('size',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )



# The parser for performances
performance_parser = reqparse.RequestParser()
performance_parser.add_argument('text',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
performance_parser.add_argument('location',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
performance_parser.add_argument('date',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

