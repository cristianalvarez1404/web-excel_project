from django.shortcuts import render
from .serializer import ArticleSerializer
from .models import Article,Category,Function,Shortcut
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ArticleView(APIView):

  # permission_classes = [IsAuthenticated]

  def get_permissions(self):
    if self.request.method in ['POST','PUT','DELETE']:
      return [IsAuthenticated()]
    return []

  def get(self,request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles,many=True)
    
    return Response(serializer.data)
  
  def post(self,request):
    if not request.user.is_authenticated:
        return Response({"message":"You must be logged in"},status=status.HTTP_401_UNAUTHORIZED)
      
    if request.user.type_user.type not in ['admin','editor']:
        return Response({"message":"You do not have permissions"},status=status.HTTP_401_UNAUTHORIZED)
      
    title = request.data.get("title")
    short_desc = request.data.get("short_desc")
    explanation = request.data.get("explanation")
    category = request.data.get("category")
    image = request.data.get("image")
    function = request.data.get("function")
    shortcut = request.data.get("shortcut")
    
    if not title or not short_desc or not explanation or not category:
      return Response({"message":"Incomplete fields"},status=status.HTTP_400_BAD_REQUEST)
  
    if not all(isinstance(field,str) for field in (title,short_desc,explanation,)) or not all(isinstance(field,list) for field in (category,function,shortcut)):
      return Response({"message":"Type error in fields"},status=status.HTTP_400_BAD_REQUEST)
    
    if not all(isinstance(i,int) for i in category + function + shortcut):
      return Response({"message":"IDs must be int"},status=status.HTTP_400_BAD_REQUEST)
    
    try:
      categories = Category.objects.filter(pk__in=category)
      functions = Function.objects.filter(pk__in=function)
      shortcuts = Shortcut.objects.filter(pk__in=shortcut)
      
     
      new_article = Article.objects.create(
        title=title,
        short_desc = short_desc,
        explanation = explanation,
      )
      new_article.category.set(categories)
      new_article.function.set(functions)
      new_article.shortcut.set(shortcuts)
    
      
      serializer = ArticleSerializer(new_article)
      
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    except Exception as e:
      return Response({"error",str(e)},status=status.HTTP_400_BAD_REQUEST)
  
    
class ArticleById(APIView):
  def get(self, request,id):
    try:
      article = Article.objects.get(id=id)
      
      serializer = ArticleSerializer(article)
      
      return Response(serializer.data)
    except Article.DoesNotExist as e:
      return Response({'message':str(e)},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
      return Response({'message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
  def put(self,request,id):
    if not request.user.is_authenticated:
        return Response({"message":"You must be logged in"},status=status.HTTP_401_UNAUTHORIZED)
      
    if request.user.type_user.type not in ['admin','editor']:
        return Response({"message":"You do not have permissions"},status=status.HTTP_401_UNAUTHORIZED)
      
    try:
      article = Article.objects.get(id=id)
    
      title = request.data.get('title')
      short_desc = request.data.get('short_desc')
      explanation = request.data.get('explanation')
      shortcut = request.data.get('shortcut')
      function = request.data.get('function')
      category = request.data.get('category')
      
      fields = {
        "title":title,
        "short_desc":short_desc,
        "explanation":explanation,
        "shortcut":shortcut,
        "function":function,
        "category":category
      }
      
      new_info_article = {key: value for key, value in fields.items() if value is not None}

      for key,value in new_info_article.items():
        if key in ['category','shortcut','function']:
          getattr(article,key).set(value if isinstance(value,list) else [value])
        else:
          setattr(article,key,value)
        
      article.save()

      serializer = ArticleSerializer(article)
      
      return Response(serializer.data)
    except Article.DoesNotExist as e:
      return Response({'message':str(e)},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
      return Response({'message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
  def delete(self,request,id):
    try:
      if not request.user.is_authenticated:
        return Response({"message":"You must be logged in"},status=status.HTTP_401_UNAUTHORIZED)
      
      if request.user.type_user.type not in ['admin','editor']:
        return Response({"message":"You do not have permissions"},status=status.HTTP_401_UNAUTHORIZED)

      article = Article.objects.get(id=id)

      article.delete()

      return Response({'message':f'Article with id {id} has been deleted!'})
    except Article.DoesNotExist as e:
      return Response({'message':str(e)},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
      return Response({'message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)