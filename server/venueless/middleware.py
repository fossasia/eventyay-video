from django.utils.deprecation import MiddlewareMixin

REFERRER_POLICY = "strict-origin-when-cross-origin"


class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        has_xfo = response.get("X-Frame-Options")
        is_exempt = getattr(response, "xframe_options_exempt", False)
        is_zoom = request.path.startswith("/zoom")

        if has_xfo is None and not is_exempt and not is_zoom:
            response["X-Frame-Options"] = "DENY"

        if "Referrer-Policy" not in response:
            response["Referrer-Policy"] = REFERRER_POLICY
        return response
