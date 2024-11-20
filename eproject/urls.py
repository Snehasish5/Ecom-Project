"""
URL configuration for eproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from eapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.first),
    path('contact',views.contact),
    path('cart',views.cart),
    path('product',views.product),
    path('login',views.login),
    path('logout',views.logout),
    path('signup',views.signup),
    path('about-us',views.about),
    path('blog',views.blog),
    path('blog-details',views.blog_details),
    path('testimonial',views.testimonial),
    path('terms',views.terms),
    path('insertdata',views.value),
    path('putdata',views.put),
    path('single_product_details/<iid>',views.single_details),
    path('single_values',views.carts),
    path('remove/<kslug>',views.remove_cart),
    path('checkout',views.payu_checkoutfun),
    path("callback", views.callback),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)