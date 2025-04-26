import uuid
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from typing_extensions import Any, Dict, AnyStr, List
from .utils import create_new_jwt_token, decode_jwt_token

# Create your views here.


@csrf_exempt
def user(request: Any) -> JsonResponse:
    """
    List user/users or create a new user
    :param request:
    :return:
    """
    method: str = request.method

    if method == 'GET':
        users: List[dict] = User.objects.all()

        serializer: UserSerializer = UserSerializer(users, many=True)

        return JsonResponse(serializer.data, safe=False)

    elif method == 'POST':
        data: dict = JSONParser().parse(request)

        data["user_id"]: str = uuid.uuid1()
        data["created_at"]: Any = timezone.now()
        data["password"]: str = make_password(password=data["password"])
        data["role"]: str = "user"

        serializer: UserSerializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def login(request: Any) -> JsonResponse:
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        data: dict = JSONParser().parse(request)
        email: str = data.get("email", "")
        password: str = data.get("password", "")
        user_data: dict = dict()
        hashed_password: str = ""

        try:
            user_doc: Any = User.objects.get(email=email)
            serializer: UserSerializer = UserSerializer(user_doc)
            if not serializer.data:
                return JsonResponse({"error": f"{email} not present in our records"}, status=404)

            user_data = serializer.data
            hashed_password: str = user_data.get("password", "")
            user_data.pop("password")
        except Exception as e:
            if not isinstance(e, str):
                e = e.args[0]
            return JsonResponse({"error": e}, status=404)

        if not check_password(password, encoded=hashed_password):
            return JsonResponse({"error": "Wrong Password"}, status=400)

        token = create_new_jwt_token(user_data)

        decode_jwt_token(token)

        return JsonResponse({"Success": "User Logged In Successfully"}, status=200, headers={"x-jwt": token})

