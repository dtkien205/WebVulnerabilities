# Access Control Vulnerabilities And Privilege Escalation
## Access control là gì?
Kiểm soát truy cập là việc áp dụng các ràng buộc lên những ai hoặc những gì được phép thực hiện hành động hay truy cập tài nguyên. Trong bối cảnh ứng dụng web, kiểm soát truy cập phụ thuộc vào xác thực và quản lý phiên:
- **Xác thực (Authentication)** xác nhận người dùng đúng là người mà họ tuyên bố.
- **Quản lý phiên (Session management)** nhận diện những yêu cầu HTTP tiếp theo được gửi bởi cùng người dùng đó.
- **Kiểm soát truy cập (Access control)** quyết định liệu người dùng có được phép thực hiện hành động mà họ đang cố gắng thực hiện hay không.

Lỗi kiểm soát truy cập rất phổ biến và thường là lỗ hổng nghiêm trọng. Thiết kế/quản trị kiểm soát truy cập là vấn đề phức tạp, biến động, phải kết hợp ràng buộc kinh doanh, tổ chức, pháp lý vào triển khai kỹ thuật. Vì các quyết định này do con người đặt ra nên nguy cơ sai sót cao.

### Kiểm soát truy cập theo chiều dọc
---
**Kiểm soát truy cập theo chiều dọc (vertical access controls)** là cơ chế **giới hạn quyền truy cập vào các chức năng nhạy cảm** cho những loại người dùng cụ thể.

Với kiểm soát theo chiều dọc, các nhóm/loại người dùng khác nhau được phép dùng những chức năng ứng dụng khác nhau. Ví dụ: quản trị viên có thể sửa hoặc xóa tài khoản của bất kỳ ai, còn người dùng thường thì không có quyền làm các hành động đó. Kiểm soát theo chiều dọc có thể là cách triển khai chi tiết hơn của các mô hình bảo mật nhằm thực thi chính sách nghiệp vụ như phân tách nhiệm vụ và ít quyền nhất.


### Kiểm soát truy cập theo chiều ngang
---
**Kiểm soát truy cập theo chiều ngang (horizontal access controls)** là cơ chế **giới hạn quyền truy cập vào tài nguyên** cho những người dùng cụ thể.

Với kiểm soát theo chiều ngang, các người dùng khác nhau chỉ được truy cập một phần các tài nguyên cùng loại. **Ví dụ**: ứng dụng ngân hàng cho phép người dùng xem giao dịch và thanh toán từ tài khoản của chính họ, nhưng không từ tài khoản của người khác.

### Kiểm soát truy cập phụ thuộc vào ngữ cảnh
---
**Kiểm soát truy cập phụ thuộc ngữ cảnh (context-dependent access controls)** giới hạn quyền truy cập vào chức năng/tài nguyên dựa trên trạng thái của ứng dụng hoặc cách người dùng tương tác với nó.

Loại kiểm soát này ngăn người dùng thực hiện sai trình tự hành động. Ví dụ, một trang bán lẻ có thể chặn người dùng sửa giỏ hàng sau khi đã thanh toán.

## Leo thang đặc quyền theo chiều dọc

**Leo thang đặc quyền theo chiều dọc (vertical privilege escalation)** xảy ra khi người dùng **truy cập được vào chức năng mà họ không được phép**. Ví dụ, user thường vào được trang admin và có thể xoá tài khoản người khác → đó là leo thang đặc quyền theo chiều dọc.

**Chức năng không được bảo vệ (Unprotected functionality)** là nguyên nhân cơ bản dẫn tới leo thang đặc quyền: ứng dụng không áp đặt bất kỳ lớp bảo vệ nào cho chức năng nhạy cảm. Ví dụ, chức năng quản trị chỉ được gắn link trong trang chào mừng của admin, nhưng user thường vẫn có thể vào nếu họ truy cập trực tiếp URL admin.

Ví dụ một URL chức năng nhạy cảm:
```arduino
https://insecure-website.com/admin
```

URL này có thể truy cập bởi mọi người dùng, không chỉ những admin có liên kết trong giao diện. Đôi khi URL quản trị còn bị lộ ở nơi khác, như tệp `robots.txt`:
```arduino
https://insecure-website.com/robots.txt
```
Ngay cả khi không bị lộ, kẻ tấn công vẫn có thể dùng **wordlist** để **brute-force** vị trí của chức năng nhạy cảm.

Trong một số trường hợp, chức năng nhạy cảm được “che giấu” bằng cách đặt một URL khó đoán hơn. Đây là ví dụ về cái gọi là **“security by obscurity” (bảo mật nhờ che giấu)**. Tuy nhiên, chỉ ẩn URL không phải là kiểm soát truy cập hiệu quả, vì người dùng vẫn có thể tìm ra URL đã làm rối theo nhiều cách.

Hãy tưởng tượng ứng dụng đặt chức năng quản trị tại URL:
```arduino
https://insecure-website.com/administrator-panel-yb556
```

Kẻ tấn công có thể không đoán được ngay. Nhưng ứng dụng vẫn có thể **lộ URL** cho người dùng. Chẳng hạn URL bị để lộ trong JavaScript dùng để dựng giao diện tùy theo vai trò:
```html
<script>
  var isAdmin = false;
  if (isAdmin) {
    ...
    var adminPanelTag = document.createElement('a');
    adminPanelTag.setAttribute('href', 'https://insecure-website.com/administrator-panel-yb556');
    adminPanelTag.innerText = 'Admin panel';
    ...
  }
</script>
```
Script này sẽ thêm liên kết “Admin panel” vào UI nếu người dùng là admin. **Tuy nhiên, file script chứa URL vẫn hiển thị cho tất cả người dùng**, bất kể vai trò.

---
### Phương pháp kiểm soát truy cập dựa trên tham số
Một số ứng dụng xác định quyền truy cập hoặc vai trò của người dùng khi đăng nhập, rồi lưu thông tin này ở nơi người dùng có thể sửa. Ví dụ:
- Trường ẩn (hidden field).
- Cookie.
- Tham số query string cố định.

Ứng dụng sau đó ra quyết định kiểm soát truy cập dựa trên giá trị được gửi lên. Chẳng hạn:
```pgsql
https://insecure-website.com/login/home.jsp?admin=true
https://insecure-website.com/login/home.jsp?role=1
```
Cách làm này không an toàn, vì người dùng có thể tự ý đổi giá trị và truy cập tính năng mà họ không được phép, như chức năng quản trị.

---
### Kiểm soát truy cập bị hỏng do cấu hình nền tảng không đúng
Một số ứng dụng thực thi kiểm soát truy cập ở tầng nền tảng (platform layer): họ hạn chế truy cập vào các URL và phương thức HTTP dựa trên vai trò người dùng. Ví dụ có thể cấu hình:
```
DENY: POST, /admin/deleteUser, managers
```
Quy tắc này chặn phương thức POST lên URL `/admin/deleteUser` đối với người dùng thuộc nhóm **managers**. Tuy nhiên, nhiều thứ có thể sai khiến việc kiểm soát này bị bypass.

Một số framework hỗ trợ các header không chuẩn cho phép ghi đè URL gốc, như `X-Original-URL` và `X-Rewrite-URL`. Nếu website dựa chặt vào việc lọc theo URL ở lớp trước (reverse proxy/WAF) nhưng ứng dụng lại chấp nhận URL từ header, kẻ tấn công có thể bypass bằng yêu cầu như:
```
POST / HTTP/1.1
X-Original-URL: /admin/deleteUser
...
```
Một kiểu tấn công khác liên quan đến **phương thức HTTP** của request. Các cơ chế kiểm soát ở lớp “mặt trước” (front-end/platform layer) trước đó thường **lọc theo URL và phương thức HTTP**. **Một số website lại chấp nhận nhiều phương thức khác nhau** để thực hiện cùng một hành động. Nếu kẻ tấn công có thể dùng **GET (hoặc phương thức khác)** để thực thi hành động trên một URL bị hạn chế, họ có thể vượt qua kiểm soát truy cập được áp dụng ở lớp nền tảng.

---

### Kiểm soát truy cập bị hỏng do sự khác biệt trong việc khớp URL
Các website có mức độ “khớp đường dẫn” (path matching) khác nhau giữa request đến và endpoint đã định nghĩa. Ví dụ, có hệ thống cho phép **không phân biệt hoa–thường**, nên `/ADMIN/DELETEUSER` vẫn map về `/admin/deleteUser`. Nếu cơ chế kiểm soát truy cập khắt khe hơn (coi chúng là hai endpoint khác nhau), nó có thể không áp đúng hạn chế.

Các sai khác tương tự xảy ra khi dùng Spring và bật `useSuffixPatternMatch`. Tùy chọn này cho phép các path có đuôi **mở rộng tùy ý** được map vào endpoint không có đuôi. Tức là `/admin/deleteUser`.anything vẫn khớp với pattern `/admin/deleteUser`. **Trước Spring 5.3, tùy chọn này mặc định bật**.

Ở hệ thống khác, bạn có thể gặp chuyện `/admin/deleteUser` và `/admin/deleteUser`/ bị coi là **hai endpoint khác nhau**. Khi đó, chỉ cần thêm **dấu gạch chéo cuối** có thể bypass kiểm soát truy cập.

## Leo thang đặc quyền theo chiều ngang
**Leo thang đặc quyền theo chiều ngang (Horizontal privilege escalation)** xảy ra khi một người dùng có thể truy cập **tài nguyên thuộc về người dùng khác** (cùng loại) thay vì chỉ tài nguyên của chính mình. Ví dụ: một nhân viên xem được hồ sơ của nhân viên khác ngoài hồ sơ của mình.

Các cuộc tấn công “ngang” thường dùng kỹ thuật tương tự “dọc”. Chẳng hạn, một người dùng truy cập trang tài khoản của chính họ bằng URL:
```bash
https://insecure-website.com/myaccount?id=123
```
Nếu kẻ tấn công sửa tham số id thành ID của người khác, họ có thể truy cập trang tài khoản của người kia, kèm dữ liệu và chức năng liên quan.

Trong một số ứng dụng, tham số có thể khai thác không mang giá trị dự đoán được. Ví dụ, thay vì số tăng dần, ứng dụng dùng **GUID/UUID** để định danh người dùng. Điều này có thể ngăn kẻ tấn công đoán hoặc dự đoán ID của người khác. Tuy nhiên, các GUID của người dùng khác có thể bị lộ ở nơi khác trong ứng dụng khi người dùng được tham chiếu, như trong tin nhắn, đánh giá, v.v.

Trong một số trường hợp, ứng dụng **có phát hiện** người dùng không được phép truy cập tài nguyên và **trả về redirect** về trang đăng nhập. Tuy nhiên, **chính response chứa redirect đó** vẫn có thể kèm theo một phần dữ liệu nhạy cảm của người bị nhắm tới, nên cuộc tấn công vẫn thành công.

## Leo thang đặc quyền theo chiều ngang sang chiều dọc

Thường thì một cuộc tấn công **leo thang ngang (horizontal)** có thể chuyển hóa thành **leo thang dọc (vertical)** bằng cách chiếm đoạt tài khoản của người dùng có đặc quyền cao hơn. **Ví dụ**, leo thang ngang có thể cho phép kẻ tấn công đặt lại hoặc chiếm được mật khẩu của người dùng khác. Nếu mục tiêu là tài khoản quản trị viên, kẻ tấn công sẽ có quyền quản trị → tức là leo thang đặc quyền theo chiều dọc.

Kẻ tấn công có thể truy cập trang tài khoản của người khác bằng kỹ thuật **sửa tham số** (parameter tampering) đã mô tả ở phần leo thang ngang:
```bash
https://insecure-website.com/myaccount?id=456
```

Nếu người dùng mục tiêu là **admin**, kẻ tấn công sẽ vào được **trang tài khoản quản trị**. Trang này có thể để lộ mật khẩu admin, cho phép đổi mật khẩu, hoặc cung cấp trực tiếp các chức năng đặc quyền.

## Tham chiếu đối tượng trực tiếp không an toàn (IDOR)

IDOR là một loại lỗ hổng kiểm soát truy cập xuất hiện khi ứng dụng dùng **dữ liệu do người dùng cung cấp** để truy cập trực tiếp tới đối tượng (record, file, tài nguyên) mà **không kiểm tra quyền** thích đáng. Thuật ngữ này nổi tiếng từ OWASP Top 10 năm 2007, nhưng thực chất chỉ là một trong nhiều sai sót triển khai kiểm soát truy cập có thể bị vòng qua. IDOR thường **gắn với leo thang đặc quyền ngang** (truy cập dữ liệu của người dùng khác), nhưng **cũng có thể dẫn tới leo thang dọc (chiếm đặc quyền cao hơn).**

---
### Lỗ hổng IDOR liên quan trực tiếp đến các đối tượng cơ sở dữ liệu
URL:
```arduino
https://insecure-website.com/customer_account?customer_number=132355
```
Ứng dụng lấy `customer_number` làm chỉ mục record trong truy vấn DB. Nếu không có kiểm soát quyền bổ sung, kẻ tấn công chỉ cần đổi giá trị (132356, 132357, …) là **xem được hồ sơ khách hàng khác** → **IDOR** → **leo thang ngang.**

Đôi khi kẻ tấn công còn đổi sang user có **quyền cao hơn** hoặc lợi dụng rò rỉ mật khẩu/luồng đổi mật khẩu để đạt leo thang dọc.

---

### Lỗ hổng IDOR liên quan trực tiếp đến các tệp tĩnh
Lỗ hổng IDOR thường xuất hiện khi tài nguyên nhạy cảm được **lưu dưới dạng file tĩnh** trên hệ thống file phía server. Ví dụ, một website có thể lưu bản ghi hội thoại (chat transcript) xuống đĩa với tên file tăng dần, rồi cho phép người dùng tải về thông qua URL như sau:
```arduino
https://insecure-website.com/static/12144.txt
```

Website lưu transcript chat theo **tên file tăng dần** và cho phép người dùng tải về. Kẻ tấn công chỉ việc **đổi tên file** để đọc transcript của người khác, có thể lộ thông tin đăng nhập và dữ liệu nhạy cảm.

## Lỗ hổng kiểm soát truy cập trong các quy trình nhiều bước
Nhiều website triển khai các chức năng quan trọng qua nhiều bước. Điều này phổ biến khi:
- Cần thu thập nhiều đầu vào/lựa chọn.
- Người dùng cần **xem lại và xác nhận** trước khi thực thi hành động.

Ví dụ, chức năng quản trị **cập nhật thông tin người dùng** có thể gồm:

- Tải form chứa thông tin của một user cụ thể.
- Gửi các thay đổi.
- Xem lại thay đổi và xác nhận.

Đôi khi website áp dụng kiểm soát truy cập chặt chẽ ở một số bước, nhưng bỏ qua bước khác. Hãy hình dung trang web kiểm soát đúng ở bước 1 và 2, nhưng không kiểm ở bước 3. Họ giả định rằng người dùng chỉ đến được bước 3 nếu đã qua các bước trước. Kẻ tấn công có thể bỏ qua bước 1–2 và gửi trực tiếp request của bước 3 với các tham số cần thiết để chiếm quyền truy cập.

## Kiểm soát truy cập dựa trên Referer
**Kiểm soát truy cập dựa trên Referer:** Một số website dựa vào header `Referer` trong HTTP để quyết định quyền truy cập. Trình duyệt thường thêm `Referer` để cho biết trang nào đã khởi tạo request.

Ví dụ, ứng dụng kiểm soát chặt trang quản trị chính `/admin`, nhưng với các trang con như `/admin/deleteUser` lại chỉ kiểm tra `Referer`. Nếu `Referer` chứa URL `/admin` thì cho phép.

Trong trường hợp này, kẻ tấn công có thể hoàn toàn điều khiển `Referer`. Nghĩa là họ có thể tự rèn request trực tiếp tới trang nhạy cảm, tự đặt `Referer` phù hợp, và truy cập trái phép.

## Kiểm soát truy cập dựa trên vị trí
Một số website thực thi kiểm soát truy cập dựa trên **vị trí địa lý** của người dùng. Điều này thường áp dụng cho ngân hàng hoặc dịch vụ nội dung số nơi có ràng buộc pháp lý hay kinh doanh theo vùng. Các kiểm soát kiểu này thường có thể bị vượt qua bằng web proxy, VPN, hoặc can thiệp cơ chế định vị phía client.

## Làm thế nào để ngăn chặn lỗ hổng kiểm soát truy cập
Các lỗ hổng kiểm soát truy cập có thể được ngăn chặn bằng cách áp dụng **phòng thủ nhiều lớp** (defense-in-depth) và các nguyên tắc sau:
- Không bao giờ chỉ dựa vào `obfuscation` để kiểm soát truy cập.
- Mặc định từ chối (deny by default) trừ khi tài nguyên được chủ đích công khai.
- Dùng một cơ chế ủy quyền thống nhất toàn ứng dụng để thực thi kiểm soát truy cập khi có thể.
- Ở mức mã nguồn, bắt buộc lập trình viên khai báo quyền truy cập cho từng tài nguyên, và mặc định từ chối.
- Kiểm toán và kiểm thử kỹ lưỡng kiểm soát truy cập để bảo đảm hoạt động như thiết kế.