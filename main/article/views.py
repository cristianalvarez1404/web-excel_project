from django.shortcuts import render
from .serializer import ArticleSerializer
from .models import Article,Category,Function,Shortcut
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ArticleView(APIView):
  
  def get(self,request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles,many=True)
    
    return Response(serializer.data)
  
  def get(self, request,id):
    try:
      article = Article.objects.get(id=id)
      
      serializer = ArticleSerializer(article)
      
      return Response(serializer.data)
    except Article.DoesNotExist as e:
      return Response({'message':str(e)},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
      return Response({'message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
  def post(self,request):
    #recibe data
    title = request.data.get("title")
    short_desc = request.data.get("short_desc")
    explanation = request.data.get("explanation")
    category = request.data.get("category")
    image = request.data.get("image")
    function = request.data.get("function")
    shortcut = request.data.get("shortcut")
    
    if not title or not short_desc or not explanation or not category:
      return Response({"message":"Incomplete fields"},status=status.HTTP_400_BAD_REQUEST)
  
    #validate data - they either can not empty nor different type
    if not all(isinstance(field,str) for field in (title,short_desc,explanation,)) or not all(isinstance(field,list) for field in (category,function,shortcut)):
      return Response({"message":"Type error in fields"},status=status.HTTP_400_BAD_REQUEST)
    
    if not all(isinstance(i,int) for i in category + function + shortcut):
      return Response({"message":"IDs must be int"},status=status.HTTP_400_BAD_REQUEST)
    
    try:
      #validate catalog entities
      categories = Category.objects.filter(pk__in=category)
      functions = Function.objects.filter(pk__in=function)
      shortcuts = Shortcut.objects.filter(pk__in=shortcut)
      
      #create article in database
      new_article = Article.objects.create(
        title=title,
        short_desc = short_desc,
        explanation = explanation,
      )
      new_article.category.set(categories)
      new_article.function.set(functions)
      new_article.shortcut.set(shortcuts)
    
      #serialize data
      serializer = ArticleSerializer(new_article)
      #return data serialized
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    except Exception as e:
      return Response({"error",str(e)},status=status.HTTP_400_BAD_REQUEST)
  
  def put(self,request,id):
    try:
      #get article from db - Check if article exists
      article = Article.objects.get(id=id)
    
      #get info from request. Validate field that are not empy and validate the type
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

      #update article with new info passed
      for key,value in new_info_article.items():
        if key in ['category','shortcut','function']:
          getattr(article,key).set(value if isinstance(value,list) else [value])
        else:
          setattr(article,key,value)
        
      article.save()
      #serialize article
      serializer = ArticleSerializer(article)
      
      #return article updated
      return Response(serializer.data)
    except Article.DoesNotExist as e:
      return Response({'message':str(e)},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
      return Response({'message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
  def delete(self,request,id):
    try:
      #get article from db
      article = Article.objects.get(id=id)
      #delete from db
      article.delete()
      #return message 
      return Response({'message':f'Article with id {id} has been deleted!'})
    except Article.DoesNotExist as e:
      return Response({'message':str(e)},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
      return Response({'message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)