import logging
import traceback
from flask_restplus import Api
import settings
from sqlalchemy.orm.exc import NoResultFound


log = logging.getLogger(__name__)

authorizations = {
    'basicAuth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(version='0.1', title='Rest UFMA API',
          description='Essa API retorna informações previamente armazenadas em um banco de dados',
          authorizations=authorizations
          )


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
