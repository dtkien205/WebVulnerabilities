# File upload vulnerabilities

Lỗ hổng tải tệp lên xảy ra khi một máy chủ web cho phép người dùng tải tệp lên hệ thống tệp của nó mà không thực hiện đủ việc xác thực các yếu tố như tên, loại, nội dung hoặc kích thước của tệp. Việc không áp đặt đúng cách các hạn chế này có thể khiến ngay cả một chức năng tải ảnh cơ bản cũng bị lợi dụng để tải lên các tệp tùy ý và có khả năng gây hại. Điều này thậm chí có thể bao gồm các tệp script phía máy chủ, cho phép thực thi mã từ xa (remote code execution).

Trong một số trường hợp, hành động tải tệp lên bản thân nó đã đủ để gây ra thiệt hại. Các cuộc tấn công khác có thể liên quan đến việc gửi tiếp một yêu cầu HTTP cho tệp đó, thường nhằm kích hoạt việc thực thi nó bởi máy chủ.

# Tác động

Tác động của lỗ hổng tải tệp lên nhìn chung phụ thuộc vào hai yếu tố chính:

- Khía cạnh nào của tệp mà website không xác thực đúng cách, chẳng hạn như kích thước, loại, nội dung, v.v.
- Những hạn chế nào được áp đặt lên tệp sau khi nó đã được tải lên thành công.

Trong kịch bản xấu nhất, loại tệp không được xác thực đúng cách và cấu hình máy chủ cho phép một số loại tệp (chẳng hạn như `.php` và `.jsp`) được thực thi như mã. Trong trường hợp này, kẻ tấn công có thể tải lên một tệp mã phía máy chủ hoạt động như một web shell, về cơ bản cấp cho chúng toàn quyền kiểm soát máy chủ.

Nếu tên tệp không được xác thực đúng cách, điều này có thể cho phép kẻ tấn công ghi đè lên các tệp quan trọng chỉ bằng cách tải lên một tệp có cùng tên. Nếu máy chủ cũng tồn tại lỗ hổng Directory Traversal, điều này thậm chí có thể đồng nghĩa với việc kẻ tấn công có thể tải tệp lên các vị trí ngoài dự kiến.

Việc không đảm bảo rằng kích thước tệp nằm trong ngưỡng mong đợi cũng có thể tạo điều kiện cho một dạng tấn công từ chối dịch vụ (DoS), trong đó kẻ tấn công làm đầy dung lượng ổ đĩa khả dụng.

# Phát sinh

Xét đến những nguy hiểm khá rõ ràng, việc các website ngoài thực tế không có bất kỳ hạn chế nào về loại tệp mà người dùng được phép tải lên là điều hiếm gặp. Thông thường hơn, các lập trình viên triển khai những gì họ tin là cơ chế xác thực mạnh mẽ, nhưng thực chất lại có lỗi tiềm ẩn hoặc dễ dàng bị vượt qua.

Ví dụ, họ có thể cố gắng sử dụng blacklist để chặn các loại tệp nguy hiểm, nhưng lại không xử lý đúng các sai lệch trong quá trình phân tích khi kiểm tra phần mở rộng tệp. Như với bất kỳ blacklist nào, cũng rất dễ bỏ sót những loại tệp ít phổ biến hơn nhưng vẫn có khả năng nguy hiểm.

Trong các trường hợp khác, website có thể cố gắng kiểm tra loại tệp bằng cách xác minh các thuộc tính mà kẻ tấn công có thể dễ dàng thao túng bằng những công cụ như Burp Proxy hoặc Repeater.

Cuối cùng, ngay cả những biện pháp xác thực mạnh mẽ cũng có thể được áp dụng không nhất quán trên toàn bộ hệ thống host và thư mục tạo thành website, dẫn đến sự sai lệch mà kẻ tấn công có thể khai thác.

# Máy chủ web xử lý các yêu cầu cho tệp tĩnh như thế nào?

Trước khi tìm hiểu cách khai thác lỗ hổng tải tệp lên, điều quan trọng là bạn phải có hiểu biết cơ bản về cách máy chủ xử lý các yêu cầu đối với tệp tĩnh.

Trong lịch sử, các website gần như hoàn toàn bao gồm các tệp tĩnh, được phục vụ cho người dùng khi có yêu cầu. Do đó, đường dẫn của mỗi yêu cầu có thể ánh xạ 1:1 với hệ thống thư mục và tệp trên hệ thống tệp của máy chủ. Ngày nay, các website ngày càng trở nên động hơn và đường dẫn của một yêu cầu thường không còn mối quan hệ trực tiếp nào với hệ thống tệp nữa. Tuy nhiên, các máy chủ web vẫn xử lý các yêu cầu đối với một số tệp tĩnh, bao gồm stylesheet, hình ảnh, v.v.

Quy trình xử lý các tệp tĩnh này về cơ bản vẫn tương tự. Ở một thời điểm nào đó, máy chủ sẽ phân tích đường dẫn trong yêu cầu để xác định phần mở rộng của tệp. Sau đó, nó sử dụng thông tin này để xác định loại tệp được yêu cầu, thường bằng cách so sánh với một danh sách ánh xạ được cấu hình sẵn giữa phần mở rộng và MIME type. Những gì xảy ra tiếp theo sẽ phụ thuộc vào loại tệp và cấu hình của máy chủ.

- Nếu loại tệp là không thực thi, chẳng hạn như hình ảnh hoặc một trang HTML tĩnh, máy chủ có thể chỉ đơn giản gửi nội dung của tệp đến client trong phản hồi HTTP.
- Nếu loại tệp là thực thi, chẳng hạn như tệp PHP, và máy chủ được cấu hình để thực thi loại tệp này, nó sẽ gán các biến dựa trên header và tham số trong yêu cầu HTTP trước khi chạy script. Kết quả đầu ra sau đó có thể được gửi đến client trong phản hồi HTTP.
- Nếu loại tệp là thực thi, nhưng máy chủ không được cấu hình để thực thi loại tệp này, nó thường sẽ phản hồi bằng một lỗi. Tuy nhiên, trong một số trường hợp, nội dung của tệp vẫn có thể được trả về cho client dưới dạng plain text. Những lỗi cấu hình như vậy đôi khi có thể bị khai thác để rò rỉ mã nguồn và các thông tin nhạy cảm khác.
- Header phản hồi **Content-Type** có thể cung cấp manh mối về loại tệp mà máy chủ nghĩ rằng nó đã phục vụ. Nếu header này không được mã ứng dụng thiết lập một cách tường minh, nó thường chứa kết quả của việc ánh xạ phần mở rộng tệp/MIME type.
    

# Web shell

Từ góc độ bảo mật, kịch bản tồi tệ nhất là khi một website cho phép bạn tải lên các script phía máy chủ, chẳng hạn như tệp `PHP`, `Java` hoặc `Python`, và máy chủ cũng được cấu hình để thực thi chúng như mã. Điều này khiến việc tạo web shell của riêng bạn trên máy chủ trở nên dễ dàng.

> **Web shell**
Web shell là một script độc hại cho phép kẻ tấn công thực thi các lệnh tùy ý trên máy chủ web từ xa chỉ bằng cách gửi các yêu cầu HTTP đến đúng endpoint.
> 

Nếu bạn có thể tải web shell lên thành công, bạn gần như có toàn quyền kiểm soát máy chủ. Điều này có nghĩa là bạn có thể đọc và ghi các tệp tùy ý, trích xuất dữ liệu nhạy cảm, thậm chí sử dụng máy chủ để làm bàn đạp tấn công cả hạ tầng nội bộ lẫn các máy chủ khác bên ngoài mạng. Ví dụ, đoạn mã PHP một dòng sau có thể được dùng để đọc các tệp tùy ý từ hệ thống tệp của máy chủ:

```php
<?php echo file_get_contents('/path/to/target/file'); ?>
```

Sau khi được tải lên, chỉ cần gửi yêu cầu đến tệp độc hại này sẽ trả về nội dung của tệp mục tiêu trong phản hồi.

Một web shell linh hoạt hơn có thể trông như sau:

```php
<?php echo system($_GET['command']); ?>
```

Script này cho phép bạn truyền một lệnh hệ thống tùy ý thông qua tham số query như sau:

```bash
GET /example/exploit.php?command=id HTTP/1.1
```

# **Flawed validation**

Trên thực tế, việc bạn tìm thấy một website hoàn toàn không có biện pháp bảo vệ nào chống lại tấn công tải tệp, như trong lab trước, là điều khó xảy ra. Tuy nhiên, việc có cơ chế phòng thủ không đồng nghĩa rằng chúng đủ mạnh. Đôi khi bạn vẫn có thể khai thác các lỗ hổng trong những cơ chế này để chiếm được web shell nhằm thực thi mã từ xa (RCE).
Khi gửi các form HTML, trình duyệt thường gửi dữ liệu được cung cấp trong một yêu cầu **POST** với `Content-Type: **application/x-www-form-urlencoded**`. Cách này phù hợp để gửi các dữ liệu văn bản đơn giản như tên hoặc địa chỉ của bạn. Tuy nhiên, nó không thích hợp để gửi một lượng lớn dữ liệu nhị phân, chẳng hạn như một tệp hình ảnh hoặc tài liệu PDF. Trong trường hợp này, `Content-Type: **multipart/form-data**` được ưu tiên sử dụng.

Hãy xét một form chứa các trường để tải lên một hình ảnh, cung cấp mô tả cho nó, và nhập tên người dùng của bạn. Việc gửi form như vậy có thể tạo ra một yêu cầu trông như sau:

```
POST /images HTTP/1.1
Host: normal-website.com
Content-Length: 12345
Content-Type: multipart/form-data; boundary=---------------------------012345678901234567890123456------------------------012345678901234567890123456
Content-Disposition: form-data; name="image"; filename="example.jpg"
Content-Type: image/jpeg

[...binary content of example.jpg...]------------------------012345678901234567890123456
Content-Disposition: form-data; name="description"

This is an interesting description of my image.------------------------012345678901234567890123456
Content-Disposition: form-data; name="username"

wiene------------------------012345678901234567890123456--

```

Như bạn thấy, phần thân của thông điệp được chia thành nhiều phần riêng biệt cho từng input của form. Mỗi phần chứa một header **`Content-Disposition`**, cung cấp một số thông tin cơ bản về trường input mà nó liên quan đến. Các phần riêng lẻ này cũng có thể chứa header **`Content-Type`** của riêng chúng, cho máy chủ biết MIME type của dữ liệu được gửi bằng input đó.

Một cách mà các website có thể sử dụng để xác thực tệp tải lên là kiểm tra xem header **`Content-Type`** gắn với input này có khớp với MIME type mong đợi hay không. Ví dụ, nếu máy chủ chỉ cho phép tải lên các tệp hình ảnh, nó có thể chỉ chấp nhận các loại như **`image/jpeg`** và **`image/png`**.

Vấn đề phát sinh khi giá trị của header này được máy chủ tin tưởng một cách ngầm định. Nếu không có thêm bước xác thực nào để kiểm tra xem nội dung thực sự của tệp có khớp với MIME type được khai báo hay không, thì cơ chế phòng thủ này có thể dễ dàng bị vượt qua bằng các công cụ như **Burp Repeater**.

# Ngăn chặn

Mặc dù rõ ràng việc tốt nhất là ngăn chặn ngay từ đầu các loại tệp nguy hiểm bị tải lên, nhưng tuyến phòng thủ thứ hai là đảm bảo máy chủ không thực thi bất kỳ script nào có thể lọt qua.

Như một biện pháp phòng ngừa, các máy chủ thường chỉ chạy những script có `MIME type` mà chúng được cấu hình tường minh để thực thi. Nếu không, máy chủ có thể chỉ trả về một thông báo lỗi nào đó hoặc, trong một số trường hợp, trả lại nội dung của tệp dưới dạng plain text:

```
GET /static/exploit.php?command=id HTTP/1.1
Host: normal-website.com
```

```php
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 39

<?php echo system($_GET['command']); ?>
```

Hành vi này tự bản thân nó cũng có thể đáng chú ý, vì nó có thể cung cấp cách để rò rỉ mã nguồn, nhưng nó sẽ vô hiệu hóa mọi nỗ lực tạo web shell.

Loại cấu hình này thường khác nhau giữa các thư mục. Một thư mục mà các tệp do người dùng tải lên được lưu trữ sẽ có khả năng bị áp dụng các kiểm soát nghiêm ngặt hơn nhiều so với những vị trí khác trong hệ thống tệp vốn được cho là ngoài tầm với của người dùng cuối. Nếu bạn có thể tìm ra cách tải lên một script vào một thư mục khác – nơi vốn không được thiết kế để chứa tệp do người dùng cung cấp – thì máy chủ vẫn có thể thực thi script của bạn.

>
Máy chủ web thường sử dụng trường `filename` trong các yêu cầu **`multipart/form-data`** để xác định tên và vị trí nơi tệp sẽ được lưu.
> 

# Blacklist

Một trong những cách rõ ràng nhất để ngăn người dùng tải lên các script độc hại là đưa vào blacklist các phần mở rộng tệp tiềm ẩn nguy hiểm như **`.php`**. Tuy nhiên, phương pháp blacklisting vốn dĩ có lỗ hổng, vì rất khó để chặn tường minh mọi phần mở rộng tệp có thể được sử dụng để thực thi mã. Những blacklist như vậy đôi khi có thể bị vượt qua bằng cách sử dụng các phần mở rộng tệp ít được biết đến hơn nhưng vẫn có thể thực thi, chẳng hạn như **`.php5`**, **`.shtml`**, v.v.

# Ghi đè cấu hình server

Các máy chủ thường sẽ không thực thi tệp trừ khi chúng được cấu hình để làm như vậy. Ví dụ, trước khi một máy chủ Apache có thể thực thi các tệp PHP được client yêu cầu, lập trình viên có thể phải thêm các chỉ thị sau vào tệp **`/etc/apache2/apache2.conf`:**

```
LoadModule php_module /usr/lib/apache2/modules/libphp.so
AddType application/x-httpd-php .php
```

Nhiều máy chủ cũng cho phép lập trình viên tạo các tệp cấu hình đặc biệt trong từng thư mục riêng lẻ để ghi đè hoặc bổ sung một hoặc nhiều thiết lập toàn cục. Ví dụ, máy chủ Apache sẽ tải cấu hình dành riêng cho thư mục từ một tệp có tên **`.htaccess`** nếu tệp này tồn tại.

Tương tự, lập trình viên có thể tạo cấu hình riêng cho từng thư mục trên máy chủ **IIS** bằng cách sử dụng tệp **`web.config`**. Tệp này có thể bao gồm các chỉ thị như sau, trong ví dụ này cho phép các tệp JSON được phục vụ cho người dùng:

```xml
<staticContent>
    <mimeMap fileExtension=".json" mimeType="application/json" />
</staticContent>
```

Các máy chủ web sẽ sử dụng những tệp cấu hình kiểu này nếu chúng tồn tại, nhưng thông thường bạn không được phép truy cập chúng thông qua các yêu cầu HTTP. Tuy nhiên, đôi khi bạn có thể gặp các máy chủ không chặn việc bạn tải lên tệp cấu hình độc hại của riêng mình. Trong trường hợp này, ngay cả khi phần mở rộng tệp bạn cần bị đưa vào blacklist, bạn vẫn có thể đánh lừa máy chủ ánh xạ một phần mở rộng tùy ý sang một MIME type có thể thực thi.

# Obfuscating

Ngay cả những blacklist toàn diện nhất cũng có thể bị vượt qua bằng các kỹ thuật làm rối cổ điển. Giả sử mã xác thực phân biệt chữ hoa chữ thường và không nhận ra rằng `exploit.pHp` thực chất là một tệp **`.php`**. Nếu đoạn mã sau đó ánh xạ phần mở rộng tệp sang MIME type lại **không** phân biệt chữ hoa chữ thường, sự sai lệch này sẽ cho phép bạn lén đưa các tệp PHP độc hại qua bước xác thực và cuối cùng có thể được máy chủ thực thi.

Bạn cũng có thể đạt được kết quả tương tự bằng các kỹ thuật sau:

- **Cung cấp nhiều phần mở rộng:** Tùy thuộc vào thuật toán được sử dụng để phân tích tên tệp, tệp sau có thể được hiểu là một tệp PHP hoặc hình ảnh JPG:
    
    ```
    exploit.php.jpg
    ```
    
- **Thêm ký tự thừa ở cuối:** Một số thành phần sẽ loại bỏ hoặc bỏ qua các khoảng trắng, dấu chấm và ký tự tương tự ở cuối:
    
    ```
    exploit.php.
    ```
    
- **Sử dụng URL encoding (hoặc double URL encoding)** cho dấu chấm, dấu gạch chéo xuôi, hoặc gạch chéo ngược. Nếu giá trị không được giải mã khi xác thực phần mở rộng, nhưng lại được giải mã phía máy chủ, điều này có thể cho phép bạn tải lên các tệp độc hại vốn sẽ bị chặn:
    
    ```
    exploit%2Ephp
    ```
    
- **Thêm dấu chấm phẩy hoặc ký tự null byte đã được URL-encode trước phần mở rộng:** Nếu việc xác thực được viết bằng ngôn ngữ bậc cao như PHP hoặc Java, nhưng máy chủ lại xử lý tệp bằng các hàm bậc thấp trong C/C++, ví dụ, điều này có thể gây ra sự sai lệch về điểm kết thúc tên tệp:
    
    ```
    exploit.asp;.jpg
    exploit.asp%00.jpg
    ```
    
- **Sử dụng ký tự Unicode đa byte,** vốn có thể được chuyển đổi thành null byte hoặc dấu chấm sau khi chuyển đổi hoặc chuẩn hóa Unicode. Các chuỗi như `xC0 x2E`, `xC4 xAE` hoặc `xC0 xAE` có thể được dịch thành `x2E` nếu tên tệp được phân tích dưới dạng chuỗi UTF-8, nhưng sau đó lại được chuyển sang ký tự ASCII trước khi sử dụng trong đường dẫn.

Một số cơ chế phòng thủ khác liên quan đến việc loại bỏ hoặc thay thế các phần mở rộng nguy hiểm để ngăn tệp bị thực thi. Nếu việc chuyển đổi này không được áp dụng **đệ quy**, bạn có thể đặt chuỗi bị cấm theo cách mà khi bị loại bỏ, nó vẫn để lại một phần mở rộng hợp lệ. Ví dụ, hãy xem điều gì xảy ra nếu bạn loại bỏ **`.php`** khỏi tên tệp sau:

```
exploit.p.phphp
```

Đây chỉ là một phần nhỏ trong rất nhiều cách có thể được sử dụng để làm rối phần mở rộng tệp.

# File Content

Thay vì tin tưởng một cách ngầm định vào **`Content-Type`** được chỉ định trong yêu cầu, các máy chủ an toàn hơn sẽ cố gắng xác minh rằng nội dung của tệp thực sự khớp với định dạng mong đợi.

Trong trường hợp chức năng tải ảnh, máy chủ có thể cố gắng kiểm tra một số thuộc tính nội tại của ảnh, chẳng hạn như kích thước. Ví dụ, nếu bạn thử tải lên một script PHP, nó sẽ hoàn toàn không có thuộc tính kích thước. Do đó, máy chủ có thể suy luận rằng tệp này chắc chắn không phải là ảnh và từ chối việc tải lên.

Tương tự, một số loại tệp nhất định luôn chứa một chuỗi byte đặc trưng trong phần **header** hoặc **footer**. Những chuỗi này có thể được sử dụng như một dấu vân tay (fingerprint) hoặc chữ ký (signature) để xác định xem nội dung có khớp với loại tệp mong đợi hay không. Ví dụ, các tệp **JPEG** luôn bắt đầu bằng dãy byte `FF D8 FF`.

Đây là một cách xác thực loại tệp chắc chắn hơn nhiều, nhưng ngay cả phương pháp này cũng không phải tuyệt đối an toàn. Với các công cụ đặc biệt như **ExifTool**, việc tạo ra một tệp **polyglot JPEG** (tệp đa ngữ cảnh) chứa mã độc trong phần metadata của nó có thể trở nên hết sức đơn giản.

# Khai thác race condition

Các framework hiện đại đã được “rèn luyện” để chống chịu tốt hơn với các kiểu tấn công này. Thông thường, chúng không tải trực tiếp tệp vào vị trí đích trên hệ thống tệp. Thay vào đó, chúng áp dụng các biện pháp phòng ngừa như tải tệp vào một thư mục tạm thời (sandboxed) trước và ngẫu nhiên hóa tên tệp để tránh ghi đè lên các tệp đã tồn tại. Sau đó, chúng tiến hành xác thực trên tệp tạm thời này và chỉ chuyển nó đến vị trí đích khi đã được xác định là an toàn.

Tuy nhiên, trong một số trường hợp, lập trình viên lại tự triển khai cơ chế xử lý tải tệp độc lập với framework. Việc này không chỉ phức tạp để làm đúng mà còn có thể tạo ra các race condition nguy hiểm, cho phép kẻ tấn công hoàn toàn bỏ qua ngay cả những cơ chế xác thực mạnh mẽ nhất.

Ví dụ, một số website tải tệp trực tiếp lên hệ thống tệp chính rồi mới xóa nó đi nếu tệp không vượt qua quá trình xác thực. Hành vi này thường thấy ở những website dựa vào phần mềm diệt virus hoặc các công cụ tương tự để kiểm tra mã độc. Quá trình này có thể chỉ mất vài mili-giây, nhưng trong khoảng thời gian ngắn ngủi mà tệp tồn tại trên máy chủ, kẻ tấn công vẫn có thể khai thác và thực thi nó.

Những lỗ hổng kiểu này thường **cực kỳ tinh vi**, khiến chúng khó bị phát hiện trong quá trình kiểm thử hộp đen (blackbox testing), trừ khi bạn tìm ra cách để rò rỉ mã nguồn liên quan.

Những race condition tương tự cũng có thể xảy ra trong các chức năng cho phép bạn tải tệp lên bằng cách cung cấp một URL. Trong trường hợp này, máy chủ phải tải tệp về qua Internet và tạo một bản sao cục bộ trước khi có thể tiến hành bất kỳ bước xác thực nào.

Vì tệp được tải về thông qua HTTP, lập trình viên sẽ không thể sử dụng các cơ chế tích hợp sẵn trong framework để xác thực tệp một cách an toàn. Thay vào đó, họ có thể tự viết các quy trình thủ công để lưu trữ tạm thời và xác thực tệp, vốn có thể không đủ an toàn.

Ví dụ, nếu tệp được tải vào một thư mục tạm thời với tên được ngẫu nhiên hóa, về lý thuyết, kẻ tấn công sẽ không thể khai thác race condition nào. Nếu chúng không biết tên thư mục, chúng sẽ không thể gửi yêu cầu đến tệp đó để kích hoạt việc thực thi.

Mặt khác, nếu tên thư mục ngẫu nhiên được sinh ra bằng các hàm **pseudo-random** (giả ngẫu nhiên) như `uniqid()` trong PHP, thì nó vẫn có thể bị brute-force.

Để làm cho các cuộc tấn công kiểu này dễ thực hiện hơn, bạn có thể tìm cách **kéo dài thời gian xử lý tệp**, từ đó mở rộng “cửa sổ thời gian” cho việc brute-force tên thư mục. Một cách để làm điều này là tải lên một tệp có kích thước lớn. Nếu tệp được xử lý theo từng khối (chunks), bạn có thể lợi dụng điều này bằng cách tạo một tệp độc hại có payload ở ngay phần đầu, sau đó thêm một lượng lớn byte padding tùy ý theo sau.

# Lỗ hổng không cần thực thi mã từ xa

Trong các ví dụ trước, chúng ta đã có thể tải lên các script phía máy chủ để thực thi mã từ xa (RCE). Đây là hậu quả nghiêm trọng nhất của một chức năng tải tệp không an toàn, nhưng các lỗ hổng này vẫn có thể bị khai thác theo những cách khác.

Mặc dù bạn có thể không thực thi được script trên máy chủ, nhưng bạn vẫn có thể tải lên các script để thực hiện tấn công phía client. Ví dụ, nếu bạn có thể tải lên tệp **HTML** hoặc ảnh **SVG**, bạn có thể chèn thẻ `<script>` để tạo payload XSS dạng **stored**.

Nếu tệp đã tải lên sau đó được hiển thị trên một trang mà những người dùng khác truy cập, trình duyệt của họ sẽ thực thi script khi cố gắng render trang. Lưu ý rằng do các hạn chế của **same-origin policy**, những kiểu tấn công này chỉ hoạt động nếu tệp được phục vụ từ cùng một **origin** mà bạn đã tải nó lên.

Nếu tệp được tải lên có vẻ như vừa được lưu trữ vừa được phục vụ một cách an toàn, phương án cuối cùng là thử khai thác các lỗ hổng đặc thù liên quan đến quá trình phân tích hoặc xử lý các định dạng tệp khác nhau.

Ví dụ, nếu bạn biết máy chủ có phân tích các tệp dựa trên **XML**, chẳng hạn như các tệp Microsoft Office **.doc** hoặc **.xls**, thì đây có thể là một vector tiềm năng cho các cuộc tấn công **XXE injection**.

# HTTP

Cần lưu ý rằng một số máy chủ web có thể được cấu hình để hỗ trợ các yêu cầu **PUT**. Nếu không có cơ chế phòng thủ thích hợp, điều này có thể cung cấp một phương thức thay thế để tải lên các tệp độc hại, ngay cả khi không có chức năng tải tệp nào được cung cấp qua giao diện web.

Ví dụ:

```
PUT /images/exploit.php HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-httpd-php
Content-Length: 49

<?php echo file_get_contents('/path/to/file'); ?>
```


> Bạn có thể thử gửi các yêu cầu **OPTIONS** đến nhiều endpoint khác nhau để kiểm tra xem có endpoint nào công bố hỗ trợ phương thức **PUT** hay không.

# Ngăn chặn

Việc cho phép người dùng tải tệp lên là rất phổ biến và không nhất thiết phải nguy hiểm nếu bạn áp dụng đúng các biện pháp phòng ngừa. Nhìn chung, cách hiệu quả nhất để bảo vệ website của bạn khỏi các lỗ hổng này là triển khai tất cả các thực hành sau:

- **Kiểm tra phần mở rộng tệp dựa trên whitelist** các phần mở rộng được phép, thay vì blacklist các phần mở rộng bị cấm. Việc xác định những phần mở rộng nào bạn muốn cho phép dễ dàng hơn nhiều so với việc đoán xem kẻ tấn công có thể thử tải lên những gì.
- **Đảm bảo tên tệp không chứa bất kỳ chuỗi con nào** có thể được hiểu là một thư mục hoặc một chuỗi traversal (ví dụ: `../`).
- **Đổi tên các tệp được tải lên** để tránh xung đột có thể gây ghi đè lên các tệp hiện có.
- **Không tải tệp vào hệ thống tệp vĩnh viễn của máy chủ** cho đến khi chúng đã được xác thực hoàn toàn.
- **Cố gắng sử dụng framework có sẵn** để xử lý trước khi tải tệp thay vì tự viết cơ chế xác thực của riêng bạn.