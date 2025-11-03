# API Testing

API (Application Programming Interfaces) cho phép các hệ thống và ứng dụng phần mềm giao tiếp và chia sẻ dữ liệu với nhau. Việc kiểm thử API rất quan trọng vì các lỗ hổng trong API có thể làm suy yếu các khía cạnh cốt lõi của một trang web.


### Mối liên hệ giữa API và các lỗ hổng web truyền thống

- Tất cả các **trang web động** đều được cấu thành từ các API.
- Vì vậy, các lỗ hổng web kinh điển như **SQL Injection** cũng có thể được xem như là một phần của **kiểm thử API**.

---

## API recon

### Xác định các API Endpoint

**API endpoint** là các vị trí (đường dẫn) mà API nhận yêu cầu về một tài nguyên cụ thể trên máy chủ.

**Ví dụ:**
```
GET /api/books HTTP/1.1
Host: example.com
```


- API endpoint trong ví dụ trên là **`/api/books`**.
- Yêu cầu này sẽ **tương tác với API để lấy danh sách sách trong thư viện**.

Một endpoint khác có thể là **`/api/books/mystery`**, để **lấy danh sách các sách thể loại trinh thám**.

Sau khi đã xác định được các endpoint, bạn cần tìm hiểu **cách tương tác** với chúng. Điều này giúp ta có thể **xây dựng các yêu cầu HTTP hợp lệ để kiểm thử API**.

- **Dữ liệu đầu vào** mà API xử lý: Các tham số **bắt buộc** và **tùy chọn**.
- **Loại yêu cầu (request)** mà API chấp nhận:
  - Các **phương thức HTTP** được hỗ trợ (GET, POST, PUT, DELETE, …)
  - Các **định dạng media** được hỗ trợ (JSON, XML, …)
- **Giới hạn tần suất truy cập (rate limit)** và **cơ chế xác thực (authentication)**.

Ngay cả khi **tài liệu API không được công khai**, bạn vẫn có thể **truy cập hoặc khám phá chúng thông qua các ứng dụng đang sử dụng API**.

---

## API documentation

### Sử dụng Burp Suite để thu thập thông tin

- Dùng **Burp Scanner** để **thu thập (crawl)** toàn bộ API.
- Hoặc **duyệt ứng dụng thủ công bằng Burp's browser** để quan sát các yêu cầu.

---

### Tìm kiếm các endpoint chứa tài liệu API

Trong quá trình duyệt, hãy chú ý các endpoint có thể chứa tài liệu API, ví dụ:
```
/api
/swagger/index.html
/openapi.json
```
Nếu bạn phát hiện endpoint tài nguyên như:`/api/swagger/v1/users/123`
thì hãy **kiểm tra các đường dẫn gốc liên quan**, chẳng hạn:
```
/api/swagger/v1
/api/swagger
/api
```
Bạn cũng có thể **sử dụng danh sách các đường dẫn phổ biến trong Intruder** để **tìm tài liệu API ẩn hoặc chưa được công khai**.

### Using machine-readable documentation

**API thường được cung cấp tài liệu** để các lập trình viên biết cách sử dụng và tích hợp chúng.
#### Hai dạng tài liệu API

- **Tài liệu dành cho con người đọc (human-readable)**  
  - Dành cho lập trình viên để hiểu cách sử dụng API.  
  - Có thể bao gồm **các giải thích chi tiết, ví dụ minh họa và các tình huống sử dụng**.

- **Tài liệu dành cho máy đọc (machine-readable)**  
  - Dành cho phần mềm xử lý tự động để **tự động hóa các tác vụ như tích hợp và xác thực API**.  
  - Được viết dưới **các định dạng có cấu trúc như JSON hoặc XML**.

**Tài liệu API thường được công khai**, đặc biệt nếu API được thiết kế để sử dụng cho các lập trình viên bên ngoài. Trong trường hợp này, **hãy luôn bắt đầu quá trình thu thập thông tin bằng cách xem tài liệu API trước**.

## Xác định API endpoints

Bạn có thể dùng **Burp Scanner** để **thu thập (crawl)** ứng dụng, sau đó **thủ công điều tra các bề mặt tấn công tiềm năng bằng trình duyệt tích hợp của Burp**.

---

### Khi duyệt ứng dụng, hãy chú ý:

- **Tìm các mẫu URL gợi ý điểm cuối API (endpoint)**, chẳng hạn như: `api`


- **Chú ý các tệp JavaScript (JS)** chúng có thể chứa **tham chiếu đến các endpoint API mà bạn chưa trực tiếp gọi qua trình duyệt web**.
- **Burp Scanner sẽ tự động trích xuất một số endpoint** trong quá trình crawl. Nếu muốn **trích xuất chuyên sâu hơn**, bạn có thể dùng **JS Link Finder BApp**. Ngoài ra, bạn cũng có thể **xem thủ công các tệp JavaScript trong Burp** để tìm thêm thông tin.

---

### Tương tác với API endpoints
Sau khi đã xác định được các **API endpoint**, hãy **tương tác với chúng bằng Burp Repeater và Burp Intruder**.  
Điều này cho phép bạn **quan sát hành vi của API và phát hiện thêm các bề mặt tấn công tiềm năng**.

#### 📌 Xác định các phương thức HTTP được hỗ trợ
**Phương thức HTTP (HTTP method)** xác định **hành động sẽ được thực hiện trên một tài nguyên**.

- **GET** – Lấy dữ liệu từ một tài nguyên.
- **PATCH** – Áp dụng các thay đổi một phần cho tài nguyên.
- **OPTIONS** – Lấy thông tin về các phương thức yêu cầu có thể sử dụng trên tài nguyên đó.


Một **API endpoint có thể hỗ trợ nhiều phương thức HTTP khác nhau**. Vì vậy, **cần kiểm thử tất cả các phương thức có thể** khi điều tra endpoint. Điều này giúp bạn **phát hiện thêm chức năng ẩn và mở rộng bề mặt tấn công**.

**Ví dụ,** Endpoint **`/api/tasks`** có thể hỗ trợ:
```
GET /api/tasks -> Lấy danh sách công việc
POST /api/tasks -> Tạo một công việc mới
DELETE /api/tasks/1 -> Xóa công việc có ID = 1
```
Bạn có thể dùng **danh sách HTTP verbs tích hợp trong Burp Intruder** để **tự động thử nhiều phương thức khác nhau**.

#### 📌 Xác định các loại nội dung được hỗ trợ

Các **API endpoint thường yêu cầu dữ liệu theo một định dạng cụ thể**. Vì vậy, chúng có thể **hoạt động khác nhau tùy theo kiểu nội dung (content type)** của dữ liệu được gửi trong yêu cầu.

Việc thay đổi định dạng dữ liệu có thể giúp bạn:

- **Kích hoạt lỗi tiết lộ thông tin hữu ích**.
- **Vượt qua các cơ chế phòng thủ bị lỗi**.
- **Khai thác sự khác biệt trong logic xử lý dữ liệu**  
> Ví dụ: API có thể an toàn với dữ liệu **JSON**, nhưng lại dễ bị **tấn công injection** khi xử lý **XML**.

**Để thay đổi `content type`**
- **Sửa giá trị của header** `Content-Type` trong yêu cầu.
- **Định dạng lại phần thân (body) của yêu cầu** sao cho phù hợp với loại nội dung mới.

Bạn có thể dùng **Content type converter BApp** để **tự động chuyển đổi dữ liệu trong yêu cầu giữa XML và JSON.**

---

### Sử dụng Intruder để tìm endpoints
Sau khi đã xác định được một số **API endpoint ban đầu**, bạn có thể dùng **Burp Intruder để tìm ra các endpoint ẩn**.

Giả sử bạn đã phát hiện endpoint:
```
PUT /api/user/update
```
Bạn có thể **dò tìm các endpoint khác cùng cấu trúc** bằng cách:

- Dùng **Burp Intruder** và thêm **payload vào vị trí `/update`** với danh sách các chức năng phổ biến khác, chẳng hạn: `delete`, `add`, `create`, `list`, `info`, v.v.

#### Mẹo khi tìm endpoint ẩn
- Dùng **wordlist chứa các tên API phổ biến và thuật ngữ trong ngành**.
- Đồng thời thêm **các thuật ngữ liên quan đến ứng dụng** mà bạn đã thu thập được từ quá trình **recon ban đầu**.

---

## Tìm các tham số ẩn của API

Khi thực hiện **API recon**, bạn có thể phát hiện **các tham số mà API hỗ trợ nhưng không được tài liệu hóa**.  
Bạn có thể thử **sử dụng các tham số này để thay đổi hành vi của ứng dụng**.

---

### Công cụ hỗ trợ trong Burp

- **Burp Intruder**  
  - Tự động dò tìm các tham số ẩn bằng **wordlist chứa tên tham số phổ biến**.  
  - Có thể **thay thế tham số hiện có hoặc thêm tham số mới** vào request.  
  - Nên **bổ sung các tên tham số liên quan đến ứng dụng** dựa trên quá trình **recon ban đầu**.

- **Param Miner BApp**  
  - Tự động **đoán tới 65.536 tên tham số cho mỗi request**.  
  - **Tự động ưu tiên các tên tham số liên quan đến ứng dụng** dựa trên thông tin trong phạm vi (scope).

- **Content Discovery Tool**  
  - Giúp **phát hiện các nội dung không được liên kết công khai**,  
    bao gồm cả **các tham số ẩn** không thể truy cập trực tiếp qua giao diện.

---

### Lỗ hổng Mass Assignment

**Mass assignment** (còn gọi là **auto-binding**) là một lỗ hổng xảy ra khi **framework tự động ánh xạ (bind) các tham số trong request vào các trường của một đối tượng nội bộ**.  
Điều này có thể **vô tình tạo ra các tham số ẩn** mà **nhà phát triển không hề dự định xử lý**.

---

### Cách xác định các tham số ẩn do Mass Assignment

Vì mass assignment **tạo tham số từ các trường của đối tượng**, nên bạn có thể **xác định chúng bằng cách thủ công kiểm tra dữ liệu của các đối tượng được trả về từ API**.


**Ví dụ,** API có endpoint để cập nhật thông tin người dùng: `PATCH /api/users/`. Với request gửi dữ liệu:

```json
{
    "username": "wiener",
    "email": "wiener@example.com"
}
```
Trong khi đó, một yêu cầu khác: `GET /api/users/123` Trả về:
```json
{
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "isAdmin": "false"
}
```

Việc này **gợi ý rằng các tham số ẩn `id` và `isAdmin` có thể đang được ánh xạ vào đối tượng người dùng nội bộ**, cùng với các tham số hợp lệ `username` và `email`.

→ Do đó, nếu **thử thêm `"isAdmin": true` vào PATCH request**, bạn **có thể chiếm được quyền quản trị** nếu ứng dụng **không có cơ chế kiểm soát hợp lệ**.

### Kiểm tra lỗ hổng Mass Assignment

Để kiểm tra xem bạn có thể **chỉnh sửa giá trị tham số `isAdmin`** hay không, hãy thử gửi các request PATCH sau:

### 1. Gửi với giá trị hợp lệ `false`

```json
PATCH /api/users/123
Content-Type: application/json

{
    "username": "wiener",
    "email": "wiener@example.com",
    "isAdmin": false
}
```
→ **Mục đích**: Xem ứng dụng có phản hồi khác với bình thường không.

### 2. Gửi với giá trị không hợp lệ "foo"
```json
PATCH /api/users/123
Content-Type: application/json

{
    "username": "wiener",
    "email": "wiener@example.com",
    "isAdmin": "foo"
}
```


→ Nếu **ứng dụng phản hồi khác biệt khi giá trị không hợp lệ**,  nhưng **không phản hồi gì đặc biệt khi giá trị hợp lệ**, điều này **gợi ý rằng tham số `isAdmin` đang ảnh hưởng đến logic xử lý**  → có thể **cập nhật được**.

### 3. Gửi với giá trị true để khai thác
```json
PATCH /api/users/123
Content-Type: application/json

{
    "username": "wiener",
    "email": "wiener@example.com",
    "isAdmin": true
}
```
- Nếu ứng dụng không xác thực và lọc giá trị `isAdmin` đúng cách, thì người dùng `wiener` có thể được **cấp quyền admin** trái phép.

## Ngăn chặn lỗ hổng trong APIs

Khi thiết kế API, cần **đảm bảo yếu tố bảo mật được xem xét ngay từ đầu**.  
Cụ thể, hãy đảm bảo các điểm sau:

- **Bảo mật tài liệu API** nếu bạn **không muốn API được truy cập công khai**.

- **Giữ cho tài liệu luôn được cập nhật** để **người kiểm thử hợp pháp có thể nhìn thấy đầy đủ bề mặt tấn công của API**.

- **Áp dụng danh sách cho phép (allowlist) các phương thức HTTP hợp lệ**.
- **Xác thực `Content-Type`** để đảm bảo **đúng định dạng mong đợi** cho mỗi request hoặc response.
- Sử dụng **thông báo lỗi chung chung**, **tránh tiết lộ thông tin nhạy cảm** cho kẻ tấn công.

- **Áp dụng các biện pháp bảo mật trên tất cả các phiên bản API**, không chỉ bản đang chạy production.

#### Ngăn chặn lỗ hổng Mass Assignment
- **Allowlist các thuộc tính (properties) được phép cập nhật** bởi người dùng.
- **Blocklist các thuộc tính nhạy cảm** không được phép cập nhật bởi người dùng.

<br>


# Server-side parameter pollution

Một số hệ thống có chứa **API nội bộ (internal API)** không thể truy cập trực tiếp từ Internet.   **Server-side Parameter Pollution (SSPP)** xảy ra khi **trang web chèn đầu vào của người dùng vào một request phía máy chủ tới API nội bộ mà không mã hóa đúng cách**.

Kẻ tấn công có thể **can thiệp hoặc chèn tham số độc hại**, từ đó:

- **Ghi đè các tham số hiện có**
- **Thay đổi hành vi của ứng dụng**
- **Truy cập vào dữ liệu trái phép**

Bạn có thể thử kiểm tra SSPP với **bất kỳ loại đầu vào người dùng nào**, ví dụ:
- **Query parameters** (tham số truy vấn trên URL)
- **Form fields** (trường biểu mẫu)
- **Headers** (tiêu đề HTTP)
- **URL path parameters** (tham số trong đường dẫn URL)

> ⚠️ Nếu khi chèn thêm hoặc sửa tham số mà ứng dụng có hành vi bất thường, có thể đây là dấu hiệu của lỗ hổng SSPP.

## Kiểm tra server-side parameter pollution trong chuỗi truy vấn

Để kiểm thử **server-side parameter pollution (SSPP)** trong **query string**, bạn có thể:

- **Chèn các ký tự cú pháp truy vấn** như `#`, `&`, và `=` vào đầu vào của người dùng.
- Sau đó **quan sát phản hồi của ứng dụng** để xem có hành vi bất thường hay không.

#### Ví dụ:
Giả sử ứng dụng có chức năng **tìm kiếm người dùng theo tên**, Khi bạn tìm người dùng `peter`, trình duyệt sẽ gửi yêu cầu:

```http
GET /userSearch?name=peter&back=/home
```

Phía máy chủ, ứng dụng sẽ dùng đầu vào `name` để gọi API nội bộ như sau:

```
GET /users/search?name=peter&publicProfile=true
```

### Ý tưởng khai thác
Nếu đầu vào `name` không được mã hóa đúng cách trước khi chèn vào request nội bộ,
kẻ tấn công có thể chèn thêm tham số độc hại, ví dụ:
```http
peter&publicProfile=false
```
để ghi đè giá trị `publicProfile` trong request nội bộ và truy cập dữ liệu không công khai.
```http
GET /users/search?name=peter&publicProfile=false&publicProfile=true
```

### Truncating query strings
---
Bạn có thể **dùng ký tự `#` đã được mã hóa URL (`%23`)** để **cố gắng cắt ngắn (truncate) request phía máy chủ**. Để dễ phân tích phản hồi, bạn cũng có thể **thêm một chuỗi bất kỳ sau ký tự `#`**.
#### Ví dụ
Thay vì gửi yêu cầu gốc:
```
GET /userSearch?name=peter&back=/home
```
bạn thử gửi:
```
GET /userSearch?name=peter%23foo&back=/home
```
Phía front-end sẽ tạo request đến API nội bộ như sau:
```
GET /users/search?name=peter#foo&publicProfile=true
```

Phần sau `#foo` sẽ **không được gửi đến máy chủ**, khiến phần `&publicProfile=true` **bị bỏ qua**.

→ Điều này có thể **thay đổi hành vi của request nội bộ** và **vô hiệu hóa các tham số bảo vệ**,  
từ đó **tạo cơ hội khai thác lỗ hổng Server-side Parameter Pollution (SSPP)**.

Sau khi chèn ký tự `#` (hoặc `%23`) để thử **cắt ngắn (truncate) request phía máy chủ**, hãy **xem xét phản hồi** để tìm dấu hiệu:

- Nếu phản hồi trả về **người dùng `peter`**  
  → Có thể **truy vấn phía máy chủ đã bị cắt ngắn**, chỉ còn phần `name=peter`.
- Nếu phản hồi trả về **lỗi `Invalid name`**  
  → Có thể ứng dụng đã **xem `foo` là một phần của tên người dùng**, nghĩa là **truy vấn không bị cắt**.

Nếu bạn **cắt được request phía máy chủ thành công**, phần `&publicProfile=true` sẽ bị bỏ qua. Điều này giúp **bỏ qua điều kiện yêu cầu hồ sơ phải công khai (publicProfile)**. Có thể **khai thác để truy xuất các hồ sơ người dùng không công khai**.

### Injecting invalid parameters
---
Bạn có thể **dùng ký tự `&` đã được mã hóa (`%26`)** để **thử chèn thêm một tham số mới** vào request phía máy chủ.

Thay vì gửi yêu cầu gốc:
```
GET /userSearch?name=peter&back=/home
```
bạn thử gửi:
```http
GET /userSearch?name=peter%26foo=xyz&back=/home
```
Request phía máy chủ sẽ trở thành:
```
GET /users/search?name=peter&foo=xyz&publicProfile=true
```

Quan sát phản hồi để xem tham số foo mới được xử lý như thế nào. Nếu phản hồi không thay đổi, điều này có thể nghĩa là tham số đã được chèn thành công nhưng bị ứng dụng bỏ qua.

### Injecting valid parameters
---
Nếu bạn có thể **chỉnh sửa được query string**, hãy thử **chèn thêm một tham số hợp lệ khác** vào request phía máy chủ.

Giả sử bạn đã xác định được tham số `email`, hãy thêm nó vào query string như sau:

```http
GET /userSearch?name=peter%26email=foo&back=/home
```
Phía server có thể ghép lại thành:
```http
GET /users/search?name=peter&email=foo&publicProfile=true
```

- Nếu phản hồi thay đổi (ví dụ trả về dữ liệu của người có email=foo hoặc báo lỗi khác lạ), có thể tham số email đã được xử lý → tiềm năng chèn thành công.
- Nếu phản hồi không đổi, có thể tham số được chèn thành công nhưng bị bỏ qua.

### Overriding existing parameters
---

Để xác nhận ứng dụng có **dễ bị tấn công SSPP (Server-side Parameter Pollution)** hay không,  
bạn có thể **thử ghi đè tham số gốc bằng cách chèn thêm một tham số trùng tên**.

Gửi request:
```
GET /userSearch?name=peter%26name=carlos&back=/home
```
Phía server có thể ghép lại thành:
```
GET /users/search?name=peter&name=carlos&publicProfile=true
```
Lúc này **API nội bộ sẽ nhận 2 tham số `name`**. **Cách xử lý sẽ khác nhau tùy vào công nghệ web**:

- **PHP**: đọc **tham số cuối** → tìm người dùng `carlos`
- **ASP.NET**: **kết hợp cả hai giá trị** → tìm `peter,carlos` → có thể báo lỗi `Invalid username`
- **Node.js / Express**: đọc **tham số đầu** → vẫn tìm `peter` → phản hồi không đổi

#### ⚡ Khai thác tiềm năng
Nếu bạn ghi đè được tham số gốc, bạn có thể lợi dụng để đăng nhập với tài khoản đặc quyền, ví dụ:
```http
GET /userSearch?name=peter%26name=administrator&back=/home
```
→ Nếu server dùng tham số cuối (administrator) để xử lý, bạn có thể truy cập tài khoản quản trị.

## Kiểm tra SSPP (Server-Side Parameter Pollution) trong REST paths
**RESTful API** có thể **đặt tên và giá trị tham số trong đường dẫn URL (URL path)** thay vì trong query string. 

**Ví dụ:**
```http
/api/users/123
```
- `/api` → endpoint gốc  
- `/users` → tài nguyên (resource), ở đây là **người dùng**  
- `/123` → tham số (parameter), ở đây là **ID của người dùng**

Ứng dụng cho phép chỉnh sửa hồ sơ người dùng dựa trên `username`:

**Request phía client:**
```http
GET /edit_profile.php?name=peter
```
**Request phía máy chủ:**
```http
GET /api/private/users/peter
```
#### Cách tấn công
Kẻ tấn công có thể **chèn chuỗi Path Traversal** để **thay đổi giá trị tham số trong URL path.**

**Request thử nghiệm:**
```
GET /edit_profile.php?name=peter%2f..%2fadmin
```
**Request phía máy chủ sẽ thành:**
```
GET /api/private/users/peter/../admin
```
→ Nếu **máy khách phía máy chủ hoặc API backend chuẩn hóa (normalize) đường dẫn**, nó có thể được diễn giải thành:
```swift
/api/private/users/admin
```
→ cho phép **truy cập trái phép vào tài nguyên của user `admin`.**

## Kiểm tra SSPP trong dữ liệu có cấu trúc (structured data formats)
Kẻ tấn công có thể **lợi dụng các tham số đầu vào để chèn dữ liệu có cấu trúc (structured data)** như **JSON hoặc XML**, nhằm khai thác **cách máy chủ xử lý dữ liệu** nếu không được kiểm tra kỹ.

### Ví dụ 1 – Đầu vào dạng form data
Ứng dụng cho phép chỉnh sửa hồ sơ người dùng. 

**Trình duyệt gửi request:**
```http
POST /myaccount
name=peter
```
**Máy chủ sẽ gọi API:**
```http
PATCH /users/7312/update
{"name":"peter"}
```
**Thử chèn thêm tham số `access_level`:**
```http
POST /myaccount
name=peter","access_level":"administrator
```
→ Nếu dữ liệu không được kiểm tra và mã hóa đúng cách, request phía máy chủ sẽ trở thành:
```http
PATCH /users/7312/update
{"name":"peter","access_level":"administrator"}
```
⇒ Người dùng `peter` có thể được cấp quyền **administrator**.

### Ví dụ 2 – Đầu vào dạng JSON
**Trình duyệt gửi request:**
```http
POST /myaccount
{"name": "peter"}
```
**Máy chủ sẽ gọi API:**
```http
PATCH /users/7312/update
{"name":"peter"}
```
**Thử chèn tham số `access_level`:**
```http
POST /myaccount
{"name": "peter\",\"access_level\":\"administrator"}
```
→ Nếu máy chủ **giải mã và chèn trực tiếp vào JSON** mà không kiểm tra/mã hóa đúng cách, request phía máy chủ sẽ thành:
```http
PATCH /users/7312/update
{"name":"peter","access_level":"administrator"}
```

⇒ `peter` có thể được cấp quyền **administrator**.

## Kiểm tra bằng các công cụ tự động
**Burp Suite** cung cấp một số công cụ tự động giúp **phát hiện lỗ hổng Server-side Parameter Pollution (SSPP)**.
### Burp Scanner

- **Tự động phát hiện các biến đổi đầu vào đáng ngờ (suspicious input transformations)** khi thực hiện audit.
- Điều này xảy ra khi:
  - Ứng dụng nhận đầu vào từ người dùng
  - Biến đổi đầu vào theo một cách nào đó
  - Sau đó tiếp tục xử lý kết quả đã biến đổi
- ⚠️ **Hành vi này không nhất thiết là lỗ hổng**, nên bạn cần **kiểm thử thủ công** như các kỹ thuật đã nêu ở trên.


### Backslash Powered Scanner BApp

- Dùng để **phát hiện các lỗ hổng injection phía máy chủ (server-side injection)**.
- Scanner sẽ phân loại đầu vào thành:
  - **boring** (không quan trọng)
  - **interesting** (đáng chú ý)
  - **vulnerable** (dễ bị tấn công)
- Với các đầu vào **interesting**, bạn cần **kiểm thử thủ công tiếp** như hướng dẫn ở trên.

## Ngăn chặn Server-side Parameter Pollution (SSPP)

Để **ngăn chặn SSPP**, cần thực hiện các biện pháp sau:

- **Dùng allowlist để xác định các ký tự không cần mã hóa**.  
  → Giúp hạn chế những ký tự đặc biệt có thể gây lỗi hoặc bị lợi dụng.

- **Mã hóa (encode) toàn bộ đầu vào của người dùng**  
  → trước khi **chèn chúng vào các request phía máy chủ**.

- **Xác thực đầu vào** để đảm bảo:
  - **Đúng định dạng mong đợi**
  - **Đúng cấu trúc yêu cầu**  

> ✅ Nhờ vậy, bạn có thể ngăn chặn việc kẻ tấn công chèn hoặc thao túng tham số độc hại vào request nội bộ.
