# Server-side Template Injection (SSTI)

## Template Engine phổ biến
### Python
- Jinja2 (được dùng trong Flask)
- Django Template Language (Django Framework)

### JavaScript: 
- EJS, Pug (trước đây là Jade), Handlebars

### PHP
- Twig, Smarty, Blade (Laravel Framework)

### Java
- Thymeleaf, Freemarker (hay dùng với Spring Boot Framework)
- Velocity, Handlebars Java, Pebble

### NodeJS: 
- Marko

### Ruby: 
- ERB

## Template Engine Twig
### Hiển thị giá trị hoặc biểu thức cơ bản
    - Welcome {{ username }} → Welcome Hieu 
    - {{ 5 + 5 }} → 10

### Gọi hàm hoặc phương thức có sẵn
    - {{ "hello, world"|upper }} → upper là một filter có sẵn trong Twig Engine, dùng để in hoa chuỗi thành "HELLO, WORLD".
    - {{ user.getName() }} → Nếu object user có tồn tại phương thức getName(), nó sẽ được gọi và thực thi.

### Xử lý các điều kiện (if else) cơ bản
    {{ role == 'admin' ? 'Welcome, Admin' : 'Welcome, User' }} → Nếu biến role có giá trị là "admin", in ra "Welcome, Admin"; nếu không thì in ra chuỗi còn lại "Welcome, User".


#### Bài ví dụ:
    - Twig Playground
    - Hello Twig



## Template Engine Jinja2

### Hiển thị giá trị hoặc biểu thức cơ bản
    - Welcome {{ username }} → Welcome Hieu 
    - {{ 5 + 5 }} → 10

### Gọi hàm hoặc phương thức có sẵn
    - {{ "hello, world"|upper }} 
    - {{ user.getName() }} 

### Truy cập các biến Global của Framework
    - config

#### Lưu ý: Do syntax của Twig và Jinja2 giống nhau nên để phân biệt test payload `{{7*'7'}}` nếu ra `7777777` thì là Jinja2


## Tìm Kiếm Lỗ Hổng SSTI

### Step 1: Detect
Xác định các tham số mà giá trị của nó bị *reflected* trong response (JSON Response, HTML Front-end, Nội dung Email,...).  
Giống với việc tìm lỗi XSS.

### Step 2: Identify
Sử dụng payload đặc thù để xác định **template engine**.  
Giống như việc xác định **DBMS** trong lỗ hổng SQL Injection.

### Step 3: Exploit


#### Bài ví dụ:
    - What is your name?
    - I Known Your IP
    - Twig Playground
    - Twig basic
    - Jinja2 VCard Generator
    - Jinja2 basic