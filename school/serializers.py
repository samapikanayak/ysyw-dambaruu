from rest_framework import serializers

from user.models import Person

from .models import School


class SchoolSerializer(serializers.ModelSerializer):
    authorized_by = serializers.SerializerMethodField(
        "get_authorized_by_name", read_only=True
    )

    class Meta:
        model = School
        fields = [
            "id",
            "school_name",
            "school_head",
            "school_code",
            "classes",
            "address",
            "pin",
            "city",
            "contact_number",
            "email",
            "affiliation_no",
            "authorized_by",
            "is_active",
        ]
        extra_kwargs = {
            "school_code": {"read_only": True},
            "is_active": {"read_only": True},
        }

    def validate(self, data):
        if "authorized_by" in self.context:
            data["authorized_by"] = self.context[
                "authorized_by"
            ]  # self.context["authorized_by"]returned from school.views.SchoolViewSets.create()
        return data

    def get_authorized_by_name(self, obj):
        if (person := Person.objects.filter(id=obj.authorized_by)).exists():
            return person.first().name
        return ""


class SchoolUpdateSerializer(serializers.ModelSerializer):
    authorized_by = serializers.SerializerMethodField(
        "get_authorized_by_name", read_only=True
    )

    class Meta:
        model = School
        fields = [
            "id",
            "school_name",
            "school_head",
            "school_code",
            "classes",
            "address",
            "pin",
            "city",
            "contact_number",
            "email",
            "affiliation_no",
            "authorized_by",
            "is_active",
        ]
        extra_kwargs = {
            "school_code": {"read_only": True},
        }


    def get_authorized_by_name(self, obj):
        if (person := Person.objects.filter(id=obj.authorized_by)).exists():
            return person.first().name
        return ""
