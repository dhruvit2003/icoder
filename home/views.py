from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# HTML pages
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content= content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")

def search(request):
    if 'query' in request.GET:
        query = request.GET['query']
    else:
        query = False 

    if len(query)>78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)  
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent,allPostsAuthor)

    if allPosts.count() == 0:
        messages.warning(request, "No search results found. please refine your search.")  
    # print(query) 
    # query = request.POST['query']
    # allPosts = Post.objects.all()
    
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)
    # return HttpResponse("This Is Search Page")

# Authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        # get the post parameter
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # checks for errorneous
        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers.")
            return redirect('home')  
    
        if len(username) > 10:
            messages.error(request, "Username must be under 10 character")
            return redirect('home')  
    
        if (pass2 != pass1):
            messages.error(request, "Passwords do not match")
            return redirect('home')  


        # create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Icoder account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse('404 - not found')

def handleLogin(request):
    if request.method == 'POST':
        # get the post parameter
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In ")
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials, Please try again')
            return redirect('home') 
    else:
        return HttpResponse('404 - not found')
    # return HttpResponse('login')

def handleLogout(request):
    
    if request.method == 'GET':
        print(request)
        logout(request)
        messages.success(request, "Successfully Logged Out ")
        return redirect('home') 

    else:
        return HttpResponse('404 - not found')

    # return HttpResponse('logout')

def addBlog(request):
    if request.method == "POST":
        title = request.POST['blogtitle']
        content = request.POST['blogcontent']
        author = request.POST['blogauthor']
        slug = request.POST['blogslug']
        post = Post(title=title, content=content, author=author, slug=slug)
        post.save()
        messages.success(request, "Your post has been successfully added")
        return render(request, 'blog/blogHome.html')
    else:
        messages.error(request, "Please fill the form correctly")
        return render(request, 'blog/blogHome.html')
