from rest_framework import serializers
from .models import Product, ProductPhoto

class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ('image_url',)

class ProductSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'photos')

    def get_photos(self, obj):
        """
        Возвращает список ссылок на фото в соответствии с бизнес-логикой:
        - Если для данного товара есть фото, привязанные к city_id, равному городу из хедера,
          то показываем только их.
        - Иначе, если нет фото для конкретного города, то показываем фото без city_id (универсальные).
        """
        request = self.context.get('request')
        if request is None:
            return []

        city_id = request.headers.get('X-City-Id')  # Или любое другое название хедера

        if city_id is not None:
            try:
                city_id = int(city_id)
            except ValueError:
                city_id = None

        city_photos = obj.photos.filter(city_id=city_id)
        if city_photos.exists():
            return ProductPhotoSerializer(city_photos, many=True).data

        universal_photos = obj.photos.filter(city_id__isnull=True)
        return ProductPhotoSerializer(universal_photos, many=True).data
