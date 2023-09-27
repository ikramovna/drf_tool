# from rest_framework.renderers import JSONRenderer
#
# class CustomRenderer(JSONRenderer):
#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         status_code = renderer_context["response"].status_code
#         success = str(status_code).startswith("2")
#
#         response = {
#             "status": "success" if success else "error",
#             "message": None,
#             "data": data if success else None,
#         }
#
#         if not success:
#             error_messages = data.get("messages")
#             if not error_messages:
#                 errors = {}
#                 for key, value in data.items():
#                     if isinstance(value, (str, list)) and len(value) > 0:
#                         if isinstance(value, str):
#                             errors = value
#                             break
#                         else:
#                             errors[key] = [str(error) for error in value]
#
#                 response["message"] = list(errors.values())[0][0] if isinstance(errors, dict) else errors
#             elif error_messages[0] and error_messages[0].get("message"):
#                 response["message"] = error_messages[0]["message"]
#
#         return super().render(response, accepted_media_type, renderer_context)
from rest_framework.renderers import JSONRenderer

class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        resolver_match = renderer_context.get('request').resolver_match
        url_name = resolver_match.url_name if resolver_match else None

        response_data = {
            'message': None,
            'status': 'ok',
            'data': {
                url_name: data.get('results') if 'results' in data else data,
            },
        }

        # Check if pagination data is available
        if 'count' in data:
            paginator_data = {
                'count': data['count'],
                'next': data.get('next', None),
                'previous': data.get('previous', None),
            }

            if any(paginator_data.values()):
                response_data['paginator'] = paginator_data

        return super().render(response_data, accepted_media_type, renderer_context)