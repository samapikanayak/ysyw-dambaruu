from rest_framework import serializers

class OrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField(max_length=20)
    standard_ids = serializers.ListField()