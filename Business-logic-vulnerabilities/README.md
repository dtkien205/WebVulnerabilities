# Business logic vulnerabilities
Lỗ hổng logic nghiệp vụ (Business logic vulnerabilities) là những sai sót trong thiết kế và triển khai ứng dụng, cho phép kẻ tấn công khai thác các hành vi không mong muốn. Điều này có thể khiến kẻ tấn công lợi dụng các chức năng hợp pháp để đạt được mục đích độc hại. Những lỗi này thường xuất phát từ việc nhà phát triển không dự đoán được các trạng thái bất thường của ứng dụng, nên không xử lý chúng một cách an toàn.

Logic flaws thường vô hình đối với những người không chủ đích tìm kiếm chúng, vì chúng hiếm khi lộ ra khi sử dụng ứng dụng bình thường. Tuy nhiên, kẻ tấn công có thể khai thác những hành vi bất thường này bằng cách tương tác với ứng dụng theo những cách mà lập trình viên không lường trước được.

Một trong những mục đích chính của logic nghiệp vụ (business logic) là thực thi các quy tắc và ràng buộc đã được xác định trong quá trình thiết kế ứng dụng hoặc chức năng. Nói chung, các quy tắc nghiệp vụ xác định ứng dụng phải phản ứng như thế nào khi một tình huống cụ thể xảy ra. Điều này bao gồm việc ngăn người dùng làm những điều có thể gây ảnh hưởng tiêu cực đến doanh nghiệp hoặc những hành động không hợp lý.

Sai sót trong logic có thể cho phép kẻ tấn công vượt qua các quy tắc này. Ví dụ, họ có thể:
- Hoàn tất một giao dịch mà không cần đi qua quy trình mua hàng như dự định.
- Thay đổi các giá trị quan trọng trong giao dịch do thiếu hoặc sai sót trong việc xác thực dữ liệu đầu vào của người dùng.

Bằng cách truyền các giá trị bất ngờ vào logic phía máy chủ, kẻ tấn công có thể khiến ứng dụng thực hiện những hành vi mà nó không được thiết kế để làm.

Lỗ hổng dựa trên logic (logic-based vulnerabilities) có thể rất đa dạng và thường là duy nhất đối với từng ứng dụng và chức năng cụ thể. Việc xác định chúng thường đòi hỏi kiến thức của con người, chẳng hạn như hiểu về lĩnh vực nghiệp vụ hoặc nhận thức về mục tiêu tiềm ẩn của kẻ tấn công trong từng bối cảnh cụ thể. Điều này khiến chúng khó bị phát hiện bởi các công cụ quét tự động.

## Nguyên nhân phát sinh business logic vulnerabilities
Business logic vulnerabilities thường phát sinh do nhóm thiết kế và phát triển đưa ra những giả định sai lầm về cách người dùng sẽ tương tác với ứng dụng. Những giả định sai này dẫn đến việc kiểm tra và xác thực dữ liệu đầu vào không đầy đủ.

Ví dụ, nếu lập trình viên giả định rằng người dùng chỉ gửi dữ liệu thông qua trình duyệt web, họ có thể chỉ dựa vào các cơ chế kiểm tra phía client (client-side validation) để xác thực dữ liệu. Tuy nhiên, các kiểm tra này rất dễ bị vượt qua bởi kẻ tấn công sử dụng các công cụ chặn và chỉnh sửa request như Burp Suite hoặc một proxy trung gian. Kết quả là, khi kẻ tấn công thao tác khác với hành vi người dùng thông thường, ứng dụng không có biện pháp thích hợp để ngăn chặn, và không xử lý tình huống một cách an toàn.

Lỗi logic đặc biệt phổ biến trong những hệ thống phức tạp, nơi ngay cả nhóm phát triển cũng không hoàn toàn hiểu rõ toàn bộ hoạt động của ứng dụng.
Để tránh lỗi logic, lập trình viên cần:

- Hiểu tổng thể ứng dụng, bao gồm việc nắm rõ cách các chức năng khác nhau có thể kết hợp với nhau theo những cách không ngờ tới.

- Trong các mã nguồn lớn, lập trình viên ở từng phần riêng lẻ thường không hiểu chi tiết về cách hoạt động của các phần khác, dẫn đến giả định sai lầm.

- Những giả định sai này có thể vô tình tạo ra các lỗ hổng logic nghiêm trọng.

Nếu các giả định của lập trình viên không được ghi chép rõ ràng, thì các lỗ hổng loại này rất dễ len lỏi vào trong ứng dụng mà không ai nhận ra.

## Tác động của business logic vulnerabilities
Tác động của lỗ hổng logic nghiệp vụ đôi khi có thể không quá nghiêm trọng, vì đây là một nhóm lỗi rất rộng và mức độ ảnh hưởng phụ thuộc vào từng trường hợp cụ thể. Tuy nhiên, bất kỳ hành vi ngoài ý muốn nào cũng có thể dẫn đến các cuộc tấn công nghiêm trọng, nếu kẻ tấn công khai thác đúng cách.

Vì lý do này, những hành vi logic bất thường (quirky logic) nên được khắc phục càng sớm càng tốt, ngay cả khi bạn chưa tìm ra cách khai thác cụ thể, bởi vì luôn có khả năng người khác sẽ làm được.

Về cơ bản, tác động của một lỗi logic phụ thuộc vào chức năng mà nó liên quan đến:

- Nếu lỗi nằm trong cơ chế xác thực (authentication mechanism), nó có thể đe dọa nghiêm trọng đến toàn bộ hệ thống bảo mật.

    → Kẻ tấn công có thể khai thác để leo thang đặc quyền (privilege escalation) hoặc bỏ qua bước xác thực hoàn toàn, từ đó truy cập dữ liệu và chức năng nhạy cảm.

- Nếu lỗi logic xuất hiện trong các giao dịch tài chính, hậu quả có thể gây thiệt hại lớn cho doanh nghiệp, chẳng hạn như: mất tiền, gian lận tài chính, thao túng hoặc sai lệch dữ liệu giao dịch.

Ngoài ra, ngay cả khi lỗi logic không mang lại lợi ích trực tiếp cho kẻ tấn công, nó vẫn có thể được sử dụng để gây tổn hại cho doanh nghiệp, ví dụ như:
- Làm gián đoạn hoạt động,
- Phá hoại dữ liệu hoặc quy trình,
- Làm mất uy tín của hệ thống hoặc thương hiệu.

## Excessive trust in client-side controls
Một giả định căn bản sai lầm là cho rằng người dùng sẽ chỉ tương tác với ứng dụng thông qua giao diện web được cung cấp. Điều này đặc biệt nguy hiểm vì nó dẫn tới giả định tiếp theo rằng việc xác thực phía client sẽ ngăn người dùng gửi dữ liệu độc hại. Tuy nhiên, kẻ tấn công có thể đơn giản sử dụng các công cụ như Burp Proxy để sửa đổi dữ liệu sau khi nó được gửi từ trình duyệt nhưng trước khi dữ liệu đó được đưa vào logic phía máy chủ. Điều này về cơ bản khiến các biện pháp kiểm soát phía client trở nên vô hiệu.

Chấp nhận dữ liệu mà không kiểm tra tính toàn vẹn và không thực hiện xác thực phía server đúng cách có thể cho phép kẻ tấn công gây ra đủ loại hại chỉ với nỗ lực tương đối nhỏ. Việc họ có thể đạt được điều gì tùy thuộc vào chức năng liên quan và cách ứng dụng sử dụng dữ liệu có thể điều khiển được. Trong bối cảnh phù hợp, kiểu lỗi này có thể gây hậu quả thảm khốc cho cả chức năng liên quan đến nghiệp vụ lẫn an ninh của chính trang web.

## Không xử lý đúng các dữ liệu đầu vào bất thường
Một mục tiêu của logic ứng dụng là giới hạn dữ liệu đầu vào của người dùng chỉ trong những giá trị phù hợp với các quy tắc nghiệp vụ. Ví dụ, ứng dụng có thể được thiết kế để chấp nhận các giá trị tùy ý của một kiểu dữ liệu nhất định, nhưng logic sẽ quyết định giá trị đó có chấp nhận được từ góc độ nghiệp vụ hay không. Nhiều ứng dụng tích hợp các giới hạn số học vào logic của chúng. Điều này có thể bao gồm các giới hạn để quản lý hàng tồn kho, áp dụng hạn mức ngân sách, kích hoạt các giai đoạn của chuỗi cung ứng, v.v.

Hãy lấy ví dụ đơn giản về một cửa hàng trực tuyến. Khi đặt hàng sản phẩm, người dùng thường chỉ định số lượng họ muốn mua. Mặc dù về lý thuyết bất kỳ số nguyên nào cũng là dữ liệu hợp lệ, logic nghiệp vụ có thể ngăn người dùng đặt nhiều hơn số lượng tồn kho hiện có. Để triển khai các quy tắc như vậy, nhà phát triển cần dự đoán mọi kịch bản có thể xảy ra và tích hợp cách xử lý vào logic ứng dụng. Nói cách khác, họ cần nói cho ứng dụng biết liệu nên cho phép một dữ liệu đầu vào nhất định hay không và ứng dụng nên phản ứng thế nào dựa trên các điều kiện khác nhau. Nếu không có logic rõ ràng để xử lý một trường hợp nhất định, điều này có thể dẫn đến hành vi không mong muốn và có thể bị khai thác.

Ví dụ, một kiểu dữ liệu số có thể chấp nhận giá trị âm. Tùy theo chức năng liên quan, cho phép giá trị âm có thể không hợp lý từ góc độ nghiệp vụ. Tuy nhiên, nếu ứng dụng không thực hiện xác thực phía server đầy đủ và không từ chối dữ liệu này, kẻ tấn công có thể truyền giá trị âm và gây ra hành vi không mong muốn.

Xét ví dụ chuyển tiền giữa hai tài khoản ngân hàng. Chức năng này rất có khả năng sẽ kiểm tra xem người gửi có đủ tiền trước khi hoàn tất chuyển khoản:
```php
$transferAmount = $_POST['amount'];
$currentBalance = $user->getBalance();

if ($transferAmount <= $currentBalance) {
    // Hoàn tất chuyển khoản
} else {
    // Chặn chuyển khoản: không đủ tiền
}
```

Nhưng nếu logic không ngăn chặn đủ việc người dùng gửi một giá trị âm trong tham số amount, điều này có thể bị kẻ tấn công lợi dụng để vượt qua kiểm tra số dư và chuyển tiền theo "hướng ngược lại". Nếu kẻ tấn công gửi -1000 cho tài khoản nạn nhân, điều này có thể dẫn đến việc nạn nhân nhận 1000 từ kẻ tấn công (tùy cách hệ thống xử lý), vì logic sẽ luôn đánh giá -1000 là nhỏ hơn số dư hiện tại và chấp thuận chuyển khoản.

Những lỗi logic đơn giản như vậy có thể phá hoại nghiêm trọng nếu xuất hiện trong chức năng nhạy cảm. Chúng cũng dễ bỏ sót trong quá trình phát triển và kiểm thử, đặc biệt khi những dữ liệu này bị chặn trên giao diện bằng các kiểm tra phía client.

Khi kiểm tra (audit) một ứng dụng, bạn nên sử dụng các công cụ như Burp Proxy và Repeater để thử gửi các giá trị bất thường. Cụ thể, thử nhập các giá trị nằm trong phạm vi mà người dùng hợp lệ hiếm khi nhập:

- Các giá trị số cực lớn hoặc cực nhỏ,
- Các chuỗi có độ dài bất thường cho các trường text,
- Thậm chí thử kiểu dữ liệu bất ngờ.

Bằng cách quan sát phản hồi của ứng dụng, bạn nên cố trả lời các câu hỏi sau:

- Có giới hạn nào đang được áp đặt lên dữ liệu không?
- Điều gì xảy ra khi bạn đạt đến (hoặc vượt qua) những giới hạn đó?
- Có đang diễn ra bất kỳ chuyển đổi hoặc chuẩn hóa nào trên dữ liệu đầu vào của bạn không?

Điều này có thể hé lộ các kiểm tra dữ liệu yếu, cho phép bạn thao túng ứng dụng theo những cách bất thường. Hãy nhớ rằng, nếu bạn tìm được một biểu mẫu (form) trên trang mục tiêu mà không xử lý dữ liệu bất thường an toàn, rất có khả năng các biểu mẫu khác cũng có cùng vấn đề.

## Giả định sai lầm về hành vi người dùng
### Người dùng đáng tin cậy sẽ không phải lúc nào cũng đáng tin cậy
Ứng dụng có thể trông an toàn vì đã triển khai những biện pháp chặt chẽ để thực thi luật nghiệp vụ. Tuy nhiên, một số ứng dụng mắc sai lầm khi giả định rằng sau khi người dùng đã vượt qua các kiểm soát ban đầu, thì người dùng và dữ liệu của họ sẽ luôn được tin tưởng vô điều kiện. Điều này có thể khiến ứng dụng nới lỏng việc áp dụng các kiểm soát tương tự ở những phần khác.

Nếu các luật nghiệp vụ và biện pháp bảo mật không được áp dụng một cách nhất quán trên toàn bộ ứng dụng, điều này có thể tạo ra những lỗ hổng nguy hiểm mà kẻ tấn công có thể lợi dụng.

### Người dùng không phải lúc nào cũng cung cấp dữ liệu bắt buộc
Một hiểu lầm phổ biến là cho rằng người dùng sẽ luôn nhập giá trị cho những trường bắt buộc. Trình duyệt có thể ngăn người dùng thông thường gửi form khi thiếu trường required, nhưng như chúng ta biết, kẻ tấn công có thể sửa đổi tham số khi truyền tải. Thậm chí họ còn có thể loại bỏ hoàn toàn tham số.

Vấn đề này trở nên đặc biệt nghiêm trọng khi nhiều chức năng được triển khai trong cùng một đoạn mã phía server. Trong trường hợp đó, sự hiện diện hoặc vắng mặt của một tham số có thể quyết định đoạn mã nào được chạy. Việc xóa tham số có thể cho phép kẻ tấn công truy cập những luồng mã lẽ ra phải bị che chắn.

Khi dò tìm lỗi logic, bạn nên thử xóa từng tham số một và quan sát ảnh hưởng tới phản hồi. Những điều cần làm:

- Chỉ xóa một tham số tại một thời điểm để đảm bảo các nhánh mã liên quan đều được kích hoạt và kiểm tra.

- Thử xoá cả tên tham số lẫn giá trị của nó. Server thường xử lý hai trường hợp này khác nhau.

- Theo dõi các quy trình nhiều bước (multi-stage) tới tận cùng - đôi khi thay đổi tham số ở bước trước sẽ gây ảnh hưởng ở bước sau trong workflow.

Áp dụng quy trình này cho cả tham số URL lẫn POST, và đừng quên kiểm tra cookie nữa. Quy trình đơn giản này có thể hé lộ những hành vi bất thường của ứng dụng mà có thể khai thác được.

## Người dùng không phải lúc nào cũng theo đúng trình tự dự kiến

Nhiều giao dịch dựa vào các luồng công việc (workflow) đã được định trước gồm một chuỗi các bước. Giao diện web thường hướng người dùng qua quy trình này, đưa họ đến bước tiếp theo mỗi khi hoàn tất bước hiện tại. Tuy nhiên, kẻ tấn công không nhất thiết phải tuân theo trình tự đó. Nếu không tính đến khả năng này sẽ tạo ra những lỗi nguy hiểm và đôi khi khá dễ khai thác.

Ví dụ: nhiều website triển khai xác thực hai bước (2FA) yêu cầu người dùng đăng nhập trên một trang rồi mới nhập mã xác thực trên trang khác. Giả sử rằng người dùng sẽ luôn hoàn thành quy trình này - và do đó không kiểm tra rằng họ thực sự đã làm vậy - có thể cho phép kẻ tấn công bỏ qua bước 2FA hoàn toàn.

Việc giả định về trình tự các sự kiện có thể dẫn tới nhiều vấn đề ngay cả trong cùng một workflow hoặc chức năng. Sử dụng các công cụ như Burp Proxy và Repeater, một khi kẻ tấn công đã nhìn thấy một request, họ có thể phát lại nó bất cứ khi nào và sử dụng forced browsing để thực hiện bất kỳ tương tác nào với máy chủ theo bất kỳ thứ tự nào họ muốn. Điều này cho phép họ hoàn thành những hành động khác nhau trong khi ứng dụng đang ở một trạng thái không mong đợi.

Để xác định những loại lỗi này, bạn nên sử dụng forced browsing để gửi các request theo một thứ tự không mong muốn. Ví dụ, bạn có thể bỏ qua một số bước, truy cập một bước riêng lẻ nhiều lần, quay về các bước trước đó, v.v. Hãy chú ý cách các bước khác nhau được truy cập. Mặc dù bạn thường chỉ gửi một request GET hoặc POST tới một URL cụ thể, đôi khi bạn có thể truy cập các bước bằng cách gửi những tập tham số khác nhau tới cùng một URL. Như với tất cả các lỗi logic, cố gắng xác định những giả định mà các nhà phát triển đã thực hiện và bề mặt tấn công nằm ở đâu. Sau đó bạn có thể tìm cách vi phạm những giả định này.

Lưu ý rằng loại kiểm thử này thường sẽ gây ra ngoại lệ vì các biến mong đợi có giá trị null hoặc chưa được khởi tạo. Đến một vị trí ở trạng thái một phần định nghĩa hoặc không nhất quán cũng có khả năng khiến ứng dụng báo lỗi. Trong trường hợp này, hãy chắc chắn chú ý kỹ tới bất kỳ thông báo lỗi hoặc thông tin debug nào bạn gặp phải. Chúng có thể là nguồn thông tin tiết lộ có giá trị, giúp bạn tinh chỉnh cuộc tấn công và hiểu rõ các chi tiết chính về hành vi phía back-end.

## Domain-specific flaws
Trong nhiều trường hợp, bạn sẽ gặp các lỗi logic có tính đặc thù theo business domain hoặc mục đích của trang.

Chức năng giảm giá của các cửa hàng trực tuyến là một bề mặt tấn công kinh điển khi săn lỗi logic. Đây có thể là “mỏ vàng” cho kẻ tấn công, vì có đủ kiểu lỗi logic cơ bản xảy ra trong cách áp dụng giảm giá.

Ví dụ, hãy xét một cửa hàng trực tuyến áp dụng giảm giá 10% cho các đơn hàng trên $1000. Cơ chế này có thể bị lạm dụng nếu logic nghiệp vụ không kiểm tra lại xem đơn hàng có bị thay đổi sau khi giảm giá đã được áp dụng hay không. Trong trường hợp đó, kẻ tấn công có thể đơn giản thêm các mặt hàng vào giỏ cho tới khi đạt ngưỡng $1000, rồi xóa những món họ không muốn trước khi đặt hàng. Họ sẽ vẫn nhận được giảm giá cho đơn hàng mặc dù lúc đặt hàng tổng giá không còn thỏa điều kiện ban đầu.

Bạn nên đặc biệt chú ý tới bất kỳ tình huống nào mà giá hoặc các giá trị nhạy cảm khác bị điều chỉnh dựa trên tiêu chí do người dùng quyết định. Cố gắng hiểu thuật toán ứng dụng dùng để thực hiện những điều chỉnh này và tại thời điểm nào các điều chỉnh được áp dụng. Điều này thường bao gồm việc thao tác ứng dụng để nó rơi vào trạng thái mà các điều chỉnh đã áp dụng không còn tương ứng với tiêu chí ban đầu mà nhà phát triển mong đợi.

Để xác định các lỗ hổng này, bạn cần suy nghĩ cẩn thận về mục tiêu có thể có của kẻ tấn công và tìm các cách khác nhau để đạt được mục tiêu đó bằng chức năng ứng dụng đang cung cấp. Việc này có thể đòi hỏi một mức độ kiến thức chuyên môn theo miền (domain-specific knowledge) để hiểu điều gì sẽ có lợi trong một bối cảnh nhất định. Lấy ví dụ đơn giản: bạn cần hiểu cách mạng xã hội hoạt động để nhận ra lợi ích của việc ép buộc nhiều tài khoản theo dõi bạn.

## Cung cấp một encryption oracle
Những tình huống nguy hiểm có thể xảy ra khi dữ liệu do người dùng điều khiển bị mã hoá và phần ciphertext (bản mã) thu được sau đó được trả lại cho người dùng dưới dạng nào đó. Loại dữ liệu này đôi khi được gọi là "encryption oracle". Kẻ tấn công có thể sử dụng nó để mã hoá bất kỳ dữ liệu nào theo đúng thuật toán và khóa (đặc biệt là khóa bất đối xứng) được dùng bởi hệ thống.

Điều này trở nên nguy hiểm khi có các đầu vào khác do người dùng kiểm soát trong ứng dụng mà mong đợi dữ liệu đã được mã hoá bằng cùng thuật toán. Trong trường hợp đó, kẻ tấn công có thể dùng encryption oracle để sinh các bản mã hợp lệ, rồi đưa các bản mã đó vào những chức năng nhạy cảm khác.

Vấn đề còn trầm trọng hơn nếu trên site có một đầu vào khác do người dùng kiểm soát cung cấp chức năng nghịch đảo (ví dụ: khả năng giải mã). Điều này cho phép kẻ tấn công giải mã các dữ liệu khác để hiểu cấu trúc mong đợi. Việc này giúp họ ít tốn công hơn khi tạo dữ liệu độc hại nhưng không bắt buộc để xây dựng một exploit thành công.

Mức độ nghiêm trọng của một encryption oracle phụ thuộc vào những chức năng nào khác trong ứng dụng cũng sử dụng cùng thuật toán như oracle đó.

## Sự khác biệt trong bộ phân tích địa chỉ email
Một số website phân tích địa chỉ email để tách phần domain và xác định tổ chức mà chủ email thuộc về. Mặc dù quá trình này tưởng chừng đơn giản, thực tế rất phức tạp - ngay cả với các địa chỉ hợp lệ theo RFC.

Sự khác biệt trong cách phân tích (parsing) địa chỉ email có thể làm suy yếu logic này. Những khác biệt này xảy ra khi các phần khác nhau của ứng dụng xử lý địa chỉ email theo cách khác nhau.

Kẻ tấn công có thể lợi dụng những khác biệt này bằng các kỹ thuật mã hóa/encode để che giấu một phần của địa chỉ email. Điều này cho phép họ tạo ra địa chỉ email vượt qua các kiểm tra xác thực ban đầu nhưng lại bị hiểu khác bởi logic phân tích ở server.

Hệ quả chính của lỗi này là truy cập trái phép. Kẻ tấn công có thể đăng ký tài khoản bằng địa chỉ dường như hợp lệ thuộc về các domain bị hạn chế, từ đó có được quyền truy cập vào các khu vực nhạy cảm của ứng dụng (admin panel, chức năng chỉ dành cho nội bộ, v.v.).

## Prevent business logic vulnerabilities
Tóm lại, chìa khóa để phòng tránh lỗ hổng logic nghiệp vụ là:

- Đảm bảo rằng developer và tester hiểu rõ miền nghiệp vụ (domain) mà ứng dụng phục vụ.

- Tránh đưa ra các giả định ngầm về hành vi người dùng hoặc hành vi của các phần khác trong ứng dụng.

Bạn nên xác định rõ những giả định mình đã đặt ra về trạng thái phía server và triển khai logic cần thiết để xác minh rằng các giả định đó được thoả mãn. Điều này bao gồm việc đảm bảo rằng giá trị của bất kỳ đầu vào nào cũng hợp lý trước khi tiếp tục xử lý.

Cũng rất quan trọng để cả developer và tester có thể hiểu đầy đủ những giả định này và biết ứng dụng nên phản ứng như thế nào trong các kịch bản khác nhau. Việc này giúp nhóm phát hiện lỗi logic sớm nhất có thể. Để thuận tiện, đội phát triển nên tuân thủ các thực hành tốt sau ở bất cứ nơi nào có thể:

- Duy trì tài liệu thiết kế rõ ràng và luồng dữ liệu cho tất cả các giao dịch và workflow, ghi chú mọi giả định được thực hiện ở mỗi giai đoạn.

- Viết mã rõ ràng nhất có thể. Nếu khó hiểu điều gì phải xảy ra thì cũng khó phát hiện lỗi logic. Lý tưởng là mã tốt nên không cần nhiều tài liệu để hiểu. Trong những trường hợp không tránh khỏi sự phức tạp, tài liệu rõ ràng là bắt buộc để đảm bảo các dev và tester biết chính xác những giả định nào đang được đặt ra và hành vi mong đợi là gì.

- Ghi chú mọi tham chiếu tới mã khác dùng mỗi thành phần. Nghĩ tới các tác động phụ (side-effects) của những phụ thuộc này nếu kẻ tấn công thao túng chúng theo cách bất thường.

Vì tính chất khá đặc thù của nhiều lỗi logic, dễ có xu hướng cho rằng đó chỉ là một lỗi bất cẩn đơn lẻ và bỏ qua. Tuy nhiên, như đã thấy, những lỗi này thường là hậu quả của các thực hành kém ngay từ giai đoạn thiết kế ban đầu. Phân tích lý do vì sao một lỗi logic xuất hiện và vì sao đội không phát hiện được nó có thể giúp bạn tìm ra điểm yếu trong quy trình. Bằng cách thực hiện những điều chỉnh nhỏ, bạn có thể tăng khả năng chặn đứng các lỗi tương tự ngay từ nguồn hoặc phát hiện sớm hơn trong quá trình phát triển.