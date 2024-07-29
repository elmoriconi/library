#**Library Management System**
##**Functions**
This library management system implemented in Django (version 5.0.6), Python (version 3.11). It provides features for:
- registering libraries, books and members;
- modifying books and members;
- deleting books (unless they have been borrowed) and members (unless they have borrowed a book and are yet to return it);
- visualize a book's specifications;
- borrow and return a book (requires a specific member to be selected).
All functions can be found in file views.py .
Testing done via Unittest, can be found in file test.py .
##**Installation**
Install Django: https://docs.djangoproject.com/en/5.0/topics/install/
Clone repository: git clone https://github.com/elmoriconi/library.git
