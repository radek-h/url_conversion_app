from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import URL as URLModel
from .utils import generate_url_key


def get_response_for_url(url: str) -> Response:
    domain_url = "http://localhost:8000/"
    url_obj = URLModel.objects.filter(Q(full_url=url) | Q(full_shorten_url=url)).first()

    if url_obj:
        if url_obj.full_url == url:
            return Response(url_obj.full_shorten_url)
        else:
            return Response(url_obj.full_url)
    else:
        if url.startswith(domain_url):
            return Response(
                {"error": "This shorten URL is not in our database."}, status=status.HTTP_404_NOT_FOUND)
        else:
            url_key = generate_url_key()
            url_obj = URLModel.objects.create(
                full_url=url,
                full_shorten_url=domain_url + url_key,
                url_shorten_key=url_key,
            )
            url_obj.save()
            return Response(url_obj.full_shorten_url)


@api_view(["GET"])
def convert_url(request) -> Response:
    url = request.GET.get("url")
    if not url:
        return Response({"error": "URL cannot be blank nor none"}, status=status.HTTP_400_BAD_REQUEST)
    response = get_response_for_url(url)
    return response
