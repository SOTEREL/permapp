from rest_framework import serializers

from ...models.map import Parcel


class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = "__all__"
