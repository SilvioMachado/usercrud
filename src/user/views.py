from src.user.blueprint import blueprint


@blueprint.route('/')
def hello():
    return 'Hello World'


@blueprint.get('/<int:user_id>')
def user_get(user_id):
    return f'user_id: {user_id}'


@blueprint.post('/<int:user_id>')
def user_post(user_id):
    return f'user_id: {user_id}'


@blueprint.delete('/<int:user_id>')
def user_delete(user_id):
    return f'user_id: {user_id}'


@blueprint.put('/<int:user_id>')
def user_put(user_id):
    return f'user_id: {user_id}'

