from django.utils.deprecation import MiddlewareMixin

REFERRER_POLICY = "strict-origin-when-cross-origin"


class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Don't set it if it's already in the response
        if response.get("X-Frame-Options") is None:
            # Don't set it if they used @xframe_options_exempt
            if not getattr(response, "xframe_options_exempt", False) and not request.path.startswith(
                "/zoom"
            ):
                response["X-Frame-Options"] = "DENY"

        if "Referrer-Policy" not in response:
            response["Referrer-Policy"] = REFERRER_POLICY
        return response
