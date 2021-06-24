from rest_framework import serializers

from blog.models import Post


class PostListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='blog-api:post-detail',
        lookup_field='slug'
    )
    delete_url  = serializers.HyperlinkedIdentityField(
        view_name='blog-api:post-delete',
        lookup_field='slug'
    )
    author = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['url','title', 'author','delete_url', 'image']

    def get_author(self, obj):
        return str(obj.author)

    def get_image(self, obj):
        try:
            image = obj.author.pp.url
        except:
            image = None
        return image


class PostDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['title', 'content','author','category','tags','pub_date',]

class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['title', 'content','category','tags','pub_date',]


    