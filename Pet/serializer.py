from rest_framework import serializers
from .models import Pet_info


class PetSerializers(serializers.ModelSerializer):
    pet_image = serializers.ImageField()

    class Meta:
        model = Pet_info
        fields = ["register_number", "register_date", "pet_date", "pet_name", "pet_gender", "pet_image", "pet_breed", "pet_lost"]

class RegPetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pet_info
        fields = ["user_id", "register_number", "pet_date", "pet_name", "pet_gender", "pet_image", "pet_breed","pet_size"]

