# Create your views here.
from rest_framework import views
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import firestore
from .validators import validate_data


class CsrfExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PostListView(CsrfExemptMixin, views.APIView):
    def get(self, request, post_id=''):
        if post_id == '':
            posts = firestore.client().collection(u'posts').stream()
            posts_list = []
            for post in posts:
                post_dict = post.to_dict()
                post_dict['uid'] = post.id
                posts_list.append(post_dict)
            return Response(posts_list, status=200)
        else:
            post = firestore.client().collection(u'posts').document(str(post_id)).get()
            if post.exists:
                post = post.to_dict()
                return Response(post, status=200)
            else:
                return Response({"error": "Post not found"}, status=404)

    def post(self, request):
        token = request.headers.get('Bearer')
        data = request.data
        if not token:
            return Response({"error": "Token login is missing"}, status=400)
        try:
            validate_data(data)

            title = data.get("title")
            content = data.get("content")
            firestore.client().collection(u'posts').document().set({
                u'title': title,
                u'content': content
            })
            response = Response({"message": "Post created"}, status=201)
            response.set_cookie('token', token, secure=True)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def put(self, request, post_id):
        token = request.headers.get('Bearer')
        data = request.data
        if not token:
            return Response({"error": "Token login is missing"}, status=400)
        try:
            validate_data(data)

            title = data.get("title")
            content = data.get("content")
            post_ref = firestore.client().collection(u'posts').document(post_id)
            if not post_ref.get().exists:
                return Response({"error": "Post not found"}, status=404)
            post_ref.update({
                u'title': title,
                u'content': content
            })
            response = Response({"message": "Post updated"}, status=200)
            response.set_cookie('token', token, secure=True)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def delete(self, request, post_id):
        token = request.headers.get('Bearer')
        if not token:
            return Response({"error": "Token login is missing"}, status=400)

        post_ref = firestore.client().collection(u'posts').document(post_id)
        if not post_ref.get().exists:
            return Response({"error": "Post not found"}, status=404)
        post_ref.delete()
        response = Response({"message": "Post deleted"}, status=200)
        response.set_cookie('token', token, secure=True)
        return response
