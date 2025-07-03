from rest_framework import serializers
from .models import Article,Category,Shortcut,Function

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id','category']

class FunctionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Function
    fields = ['id','function']

class ShortcutSerializer(serializers.ModelSerializer):
  class Meta:
    model = Shortcut
    fields = ['id','shortcut']


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(many=True,queryset=Category.objects.all(),write_only=True)
    
    function = FunctionSerializer(many=True, read_only=True)
    function_ids = serializers.PrimaryKeyRelatedField(many=True,queryset=Function.objects.all(),write_only=True)
    
    shortcut = ShortcutSerializer(many=True, read_only=True)
    shortcut_ids = serializers.PrimaryKeyRelatedField(many=True,queryset=Shortcut.objects.all(),write_only=True)
    
    class Meta:
      model = Article
      fields = [
        'id', 'title', 'short_desc', 'explanation', 'image',
        'category', 'category_ids',
        'function', 'function_ids',
        'shortcut', 'shortcut_ids',
        'created_at', 'updated_at'
      ]