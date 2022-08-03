from django.urls import include, path
from rest_framework import routers

from user.serializers import AdminSerializer

from . import views

router = routers.DefaultRouter()

router.register("admins", views.AdminViewSet, basename="admin")
router.register("tutors", views.TutorViewSet, basename="tutor")
router.register("students", views.StudentViewSet, basename="student")
router.register("contentManager", views.ContentManagerViewSet, basename="content_manager")
router.register("profileAvatar", views.profileAvatarViewset, basename="profile_avatar")

urlpatterns = [
    path("test-login/", views.TestLogin.as_view()),
    path("user-login/", views.UserSignIn.as_view(),name="user-login"),
    path("set-password/<str:id>/", views.PersonPasswordSetAPIView.as_view()),
    path("forgot-password/", views.ForgotPasswordEmail.as_view()),
    path("set-forgot-password/<str:token>/", views.ForgotPasswordResetAPIView.as_view()),
    path("change-password/", views.ChangePasswordAPIView.as_view()),
    # path("verify-otp/", views.VerifyOTP.as_view()),
    path("generate-otp/", views.GenerateOTP.as_view()),
    path("generate-txn-id/", views.GenerateTxnId.as_view()),
    path("confirm-otp/", views.ConfirmOTP.as_view()),
    path("get-user-profile/", views.GetProfileFromTxn.as_view()),
]

urlpatterns2 = [
    path("", include(router.urls)),
]

urlpatterns += urlpatterns2
