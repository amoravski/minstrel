from flask_restful import reqparse

"""
    Contains all the different request parsers
"""

# The parser for any type of user, used for logins
user_parser = reqparse.RequestParser()
user_parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
user_parser.add_argument('username',
                        type=str,
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
performer_settings_parser.add_argument('username',
                        type=str,
                        )
performer_settings_parser.add_argument('password',
                        type=str,
                        )
performer_settings_parser.add_argument('categories',
                        action="append"
                        )
performer_settings_parser.add_argument('settings',
                        type=dict,
                        )
performer_settings_parser.add_argument('location',
                        type=str,
                        )
performer_settings_parser.add_argument('description',
                        type=str,
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
admirer_parser.add_argument('categories',
                        required=True,
                        help="This field cannot be left blank!",
                        action="append"
                        )

# The parser for admirer settings
admirer_settings_parser = reqparse.RequestParser()
admirer_settings_parser.add_argument('username',
                        type=str,
                        )
admirer_settings_parser.add_argument('password',
                        type=str,
                        )
admirer_settings_parser.add_argument('preferences',
                        action="append"
                        )
admirer_settings_parser.add_argument('settings',
                        type=dict,
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

# The parser for offer settings
offer_setting_parser = reqparse.RequestParser()
offer_setting_parser.add_argument('title',
                        type=str,
                        )
offer_setting_parser.add_argument('text',
                        type=str,
                        )
offer_setting_parser.add_argument('location',
                        type=str,
                        )
offer_setting_parser.add_argument('date',
                        type=str,
                        )
offer_setting_parser.add_argument('categories',
                        action="append"
                        )
offer_setting_parser.add_argument('type',
                        type=str,
                        )
offer_setting_parser.add_argument('requirements',
                        type=str,
                        )
offer_setting_parser.add_argument('compensation',
                        type=str,
                        )
offer_setting_parser.add_argument('size',
                        type=str,
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

# The parser for performance settings
performance_setting_parser = reqparse.RequestParser()
performance_setting_parser.add_argument('title',
                        type=str
                        )

performance_setting_parser.add_argument('text',
                        type=str
                        )
performance_setting_parser.add_argument('location',
                        type=str
                        )
performance_setting_parser.add_argument('date',
                        type=str
                        )

