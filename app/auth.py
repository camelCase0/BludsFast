# from functools import wraps
# from urllib import request
#
# from fastapi import Depends, HTTPException
# from starlette import status
#
# from app.models import AuthToken, connect_db
#
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.args.get('token')
#
#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 403
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#         except:
#             return jsonify({'message': 'Token is invalid!'}), 403
#         return f(*args, **kwargs)
#
#     return decorated
# #
# # def check_auth_token(token: str, database = Depends(connect_db)):
# #     auth_token = database.query(AuthToken).filter(AuthToken.token == token).one_or_none()
# #     if auth_token:
# #         return auth_token
# #
# #     raise HTTPException(
# #         status_code=status.HTTP_403_FORBIDDEN,
# #         detail="Auth is failed"
# #     )