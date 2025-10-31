# Information disclosure
Information disclosure còn gọi là rò rỉ thông tin, là khi một website vô tình để lộ dữ liệu nhạy cảm cho người dùng. Tùy ngữ cảnh, trang web có thể rò rỉ nhiều loại thông tin cho kẻ tấn công tiềm năng, bao gồm:

- Dữ liệu về người dùng khác, ví dụ tên đăng nhập hoặc thông tin tài chính.
- Dữ liệu thương mại/kinh doanh nhạy cảm.
- Chi tiết kỹ thuật về website và hạ tầng của nó.

Nguy cơ từ việc lộ dữ liệu người dùng hoặc dữ liệu kinh doanh thì rõ ràng, nhưng việc để lộ thông tin kỹ thuật đôi khi cũng nghiêm trọng không kém. Một số thông tin có thể ít hữu dụng trực tiếp, nhưng nó có thể là điểm khởi đầu để mở rộng bề mặt tấn công, dẫn tới những lỗ hổng quan trọng hơn. Kiến thức thu thập được thậm chí có thể là mảnh ghép còn thiếu khi bạn cố gắng dựng các cuộc tấn công phức tạp, mức độ nghiêm trọng cao.

Đôi khi thông tin nhạy cảm bị vô ý lộ ra cho người dùng chỉ đang duyệt web bình thường. Tuy nhiên phổ biến hơn là kẻ tấn công phải kích thích (elicit) việc tiết lộ bằng cách tương tác với website theo những cách bất ngờ hoặc độc hại. Sau đó họ sẽ quan sát kỹ các phản hồi của website để tìm ra hành vi đáng chú ý.

## Examples of information disclosure
Một vài ví dụ cơ bản về tiết lộ thông tin như sau:

- Tiết lộ tên các thư mục ẩn, cấu trúc và nội dung của chúng thông qua file `robots.txt` hoặc danh sách thư mục (directory listing).
- Cung cấp truy cập tới các file mã nguồn thông qua bản sao lưu tạm thời.
- Nêu rõ tên bảng hoặc cột trong cơ sở dữ liệu trong các thông báo lỗi.
- Vô tình phơi bày thông tin cực kỳ nhạy cảm, chẳng hạn chi tiết thẻ tín dụng.
- Hard-code (nhúng cứng) API key, địa chỉ IP, thông tin đăng nhập cơ sở dữ liệu, v.v. trực tiếp trong mã nguồn.
- Gợi ý sự tồn tại hoặc không tồn tại của tài nguyên, tên người dùng, v.v. thông qua những khác biệt tinh tế trong hành vi của ứng dụng.

Trong phần này, bạn sẽ học cách tìm và khai thác một số ví dụ trên và nhiều trường hợp khác.

## Nguyên nhân phát sinh lỗ hổng tiết lộ thông tin
Lỗ hổng tiết lộ thông tin có thể phát sinh theo vô số cách khác nhau, nhưng nhìn chung có thể được phân loại rộng rãi như sau:

- Không loại bỏ nội dung nội bộ khỏi nội dung công khai. Ví dụ, các chú thích của lập trình viên trong mã đánh dấu đôi khi hiển thị với người dùng trong môi trường production.

- Cấu hình không an toàn của trang web và các công nghệ liên quan. Ví dụ, không tắt các tính năng gỡ lỗi và chẩn đoán đôi khi có thể cung cấp cho kẻ tấn công các công cụ hữu ích để giúp họ có được thông tin nhạy cảm. Các cấu hình mặc định cũng có thể để trang web dễ bị tấn công, ví dụ bằng cách hiển thị các thông báo lỗi quá chi tiết.

- Thiết kế và hành vi của ứng dụng có sai sót. Ví dụ, nếu một trang web trả về các phản hồi khác biệt khi xảy ra các trạng thái lỗi khác nhau, điều này cũng có thể cho phép kẻ tấn công liệt kê các dữ liệu nhạy cảm, chẳng hạn như thông tin đăng nhập hợp lệ của người dùng.

## Tác động của các lỗ hổng tiết lộ thông tin là gì?
Các lỗ hổng tiết lộ thông tin có thể gây ra cả tác động trực tiếp lẫn gián tiếp tùy thuộc vào mục đích của trang web và do đó là những thông tin mà kẻ tấn công có thể thu được. Trong một số trường hợp, chính hành động để lộ thông tin nhạy cảm thôi đã có thể gây hậu quả nghiêm trọng cho các bên bị ảnh hưởng. Ví dụ, một cửa hàng trực tuyến làm lộ chi tiết thẻ tín dụng của khách hàng có khả năng chịu hậu quả nặng nề.

Mặt khác, việc tiết lộ thông tin kỹ thuật, chẳng hạn như cấu trúc thư mục hoặc những thư viện bên thứ ba đang được sử dụng, có thể ít hoặc hầu như không có tác động trực tiếp. Tuy nhiên, nếu rơi vào tay kẻ xấu, đây có thể là thông tin then chốt để dựng nên nhiều kiểu khai thác khác. Mức độ nghiêm trọng trong trường hợp này phụ thuộc vào những gì kẻ tấn công có thể làm với những thông tin đó.

### Cách đánh giá mức độ nghiêm trọng của lỗ hổng tiết lộ thông tin
Mặc dù tác động cuối cùng có thể rất nghiêm trọng, nhưng chỉ trong những tình huống cụ thể thì việc tiết lộ thông tin mới là một vấn đề có mức độ nghiêm trọng cao khi đứng riêng. Khi kiểm thử, việc tiết lộ thông tin kỹ thuật đặc biệt thường chỉ có giá trị nếu bạn có thể chứng minh cách kẻ tấn công có thể tận dụng nó để gây hại.

Ví dụ, biết rằng một trang web đang sử dụng một phiên bản framework cụ thể thì có giá trị hạn chế nếu phiên bản đó đã được vá đầy đủ. Tuy nhiên, thông tin này trở nên quan trọng khi trang web đang chạy một phiên bản cũ có lỗ hổng đã biết. Trong trường hợp đó, thực hiện một cuộc tấn công thảm khốc có thể đơn giản như áp dụng một exploit công khai đã được mô tả.

Cần dùng lẽ thường khi phát hiện thông tin có khả năng nhạy cảm bị rò rỉ. Rất có thể các chi tiết kỹ thuật nhỏ có thể được phát hiện bằng nhiều cách trên nhiều trang web bạn kiểm thử. Do vậy, trọng tâm chính của bạn nên là tác động và khả năng khai thác của thông tin bị rò rỉ, chứ không chỉ đơn thuần là sự tồn tại của lỗ hổng tiết lộ thông tin. Ngoại lệ rõ ràng là khi thông tin bị lộ nhạy cảm đến mức tự nó đã cần được xử lý, báo cáo và khắc phục.

## Cách kiểm tra lỗ hổng tiết lộ thông tin
Nói chung, điều quan trọng là không phát triển “tầm nhìn hẹp” trong quá trình kiểm thử. Nói cách khác, bạn nên tránh tập trung quá hẹp vào một lỗ hổng cụ thể. Dữ liệu nhạy cảm có thể bị rò rỉ ở nhiều nơi khác nhau, nên điều quan trọng là không bỏ sót bất cứ thứ gì có thể hữu ích sau này. Bạn thường sẽ tìm thấy dữ liệu nhạy cảm trong khi đang kiểm thử cho một vấn đề khác. Một kỹ năng then chốt là khả năng nhận ra những thông tin đáng chú ý bất cứ khi nào và ở bất cứ đâu bạn bắt gặp chúng.

Dưới đây là một vài ví dụ về các kỹ thuật và công cụ ở mức cao mà bạn có thể sử dụng để giúp xác định các lỗ hổng tiết lộ thông tin trong quá trình kiểm thử.

- Fuzzing
- Sử dụng Burp Scanner
- Sử dụng các công cụ engagement của Burp
- Kỹ thuật tạo phản hồi có tính cung cấp thông tin (engineering informative responses)

### Fuzzing
---
Nếu bạn xác định được các tham số thú vị, bạn có thể thử gửi các kiểu dữ liệu không mong đợi và các chuỗi fuzz được chế tác đặc biệt để xem ảnh hưởng của chúng. Chú ý kỹ; mặc dù các phản hồi đôi khi trực tiếp tiết lộ thông tin đáng chú ý, chúng cũng có thể gợi ý hành vi của ứng dụng một cách tinh tế hơn. Ví dụ, đó có thể là một sự khác biệt nhỏ về thời gian xử lý yêu cầu. Ngay cả khi nội dung của thông báo lỗi không tiết lộ gì, đôi khi việc một trường hợp lỗi này xảy ra thay vì một trường hợp khác cũng là thông tin hữu ích.

Bạn có thể tự động hóa phần lớn quá trình này bằng các công cụ như Burp Intruder. Điều này mang lại một số lợi ích, đáng chú ý nhất là bạn có thể:

- Thêm vị trí payload vào các tham số và sử dụng các từ điển fuzz có sẵn để thử một khối lượng lớn input khác nhau trong thời gian ngắn.

- Dễ dàng nhận diện sự khác biệt trong phản hồi bằng cách so sánh mã trạng thái HTTP, thời gian phản hồi, độ dài, v.v.

- Sử dụng quy tắc grep để nhanh chóng nhận diện các từ khóa như error, invalid, SELECT, SQL, v.v.

- Áp dụng quy tắc trích xuất grep để trích xuất và so sánh nội dung các mục đáng chú ý trong phản hồi.

Bạn cũng có thể dùng extension Logger++ (có sẵn trên BApp store). Ngoài việc ghi lại các request và response từ tất cả công cụ của Burp, nó cho phép bạn định nghĩa bộ lọc nâng cao để làm nổi bật những mục đáng chú ý. Đây chỉ là một trong nhiều extension của Burp có thể giúp bạn tìm bất kỳ dữ liệu nhạy cảm nào bị rò rỉ bởi website.

### Using Burp Scanner
---
Người dùng Burp Suite Professional có lợi thế khi được sử dụng Burp Scanner. Công cụ này cung cấp các tính năng quét trực tiếp (live scanning) để kiểm tra bảo mật các mục khi bạn duyệt web, hoặc bạn có thể lên lịch cho các bản quét tự động để thu thập và kiểm thử toàn bộ trang web mục tiêu thay cho bạn.

Cả hai phương pháp đều sẽ tự động phát hiện và cảnh báo cho bạn về nhiều lỗ hổng tiết lộ thông tin.
Ví dụ: Burp Scanner sẽ cảnh báo nếu nó phát hiện thông tin nhạy cảm như private key, địa chỉ email, hoặc số thẻ tín dụng trong phản hồi. Nó cũng có thể nhận diện các tệp sao lưu (backup files), danh sách thư mục (directory listing), và nhiều dạng tiết lộ thông tin khác.

### Using Burp's engagement tools
---
Burp cung cấp một số công cụ engagement mà bạn có thể dùng để tìm thông tin thú vị trên trang web mục tiêu dễ dàng hơn. Bạn có thể truy cập các công cụ này từ menu ngữ cảnh - chỉ cần nhấp chuột phải vào bất kỳ thông điệp HTTP nào, mục trong Burp Proxy, hoặc mục trong site map rồi chọn "Engagement tools".

Những công cụ sau đặc biệt hữu ích trong ngữ cảnh này.

**Search**
---

Bạn có thể dùng công cụ này để tìm bất kỳ biểu thức nào trong mục được chọn. Bạn có thể tinh chỉnh kết quả bằng các tùy chọn tìm nâng cao, chẳng hạn như tìm bằng regex hoặc tìm phủ định. Điều này hữu ích để nhanh chóng tìm các xuất hiện (hoặc sự vắng mặt) của các từ khóa cụ thể mà bạn quan tâm.

**Find comments**
---
Bạn có thể dùng công cụ này để nhanh chóng trích xuất bất kỳ chú thích (comment) của nhà phát triển nào được tìm thấy trong mục được chọn. Công cụ cũng cung cấp các tab để truy cập tức thì vào chu trình request/response HTTP mà trong đó mỗi comment được phát hiện.

**Discover content**
---
Bạn có thể dùng công cụ này để xác định thêm nội dung và chức năng không được liên kết từ nội dung hiển thị của trang web. Điều này hữu ích để tìm các thư mục và file bổ sung mà có thể không xuất hiện trong site map một cách tự động.

### Kỹ thuật tạo các phản hồi có tính cung cấp thông tin
---
Các thông báo lỗi chi tiết đôi khi có thể tiết lộ thông tin hữu ích khi bạn thực hiện quy trình kiểm thử bình thường. Tuy nhiên, bằng cách nghiên cứu cách các thông báo lỗi thay đổi theo đầu vào của bạn, bạn có thể tiến thêm một bước nữa. Trong một số trường hợp, bạn có thể thao túng trang web để trích xuất dữ liệu tùy ý thông qua một thông báo lỗi.

Có nhiều phương pháp để làm điều này tùy theo kịch bản cụ thể mà bạn gặp phải. Một ví dụ phổ biến là làm cho logic ứng dụng cố gắng thực hiện một hành động không hợp lệ trên một mục dữ liệu cụ thể. Ví dụ, gửi một giá trị tham số không hợp lệ có thể dẫn đến stack trace hoặc phản hồi debug chứa những chi tiết thú vị. Đôi khi bạn có thể khiến thông báo lỗi tiết lộ giá trị của dữ liệu mà bạn muốn trong phần phản hồi.

## Common sources of information disclosure

### Files for web crawlers
---
Nhiều trang web cung cấp các tệp ở `/robots.txt` và `/sitemap.xml` để giúp các crawler điều hướng trang của họ. Những tệp này thường liệt kê những thư mục cụ thể mà crawler nên bỏ qua, ví dụ vì chúng có thể chứa thông tin nhạy cảm.

Vì các tệp này thường không được liên kết từ trong chính trang web, chúng có thể không xuất hiện ngay trong site map của Burp. Tuy nhiên, vẫn đáng thử truy cập thủ công `/robots.txt` hoặc `/sitemap.xml` để xem có tìm được điều gì hữu ích hay không.

### Directory listings
---
Máy chủ web có thể được cấu hình để tự động liệt kê nội dung của các thư mục không có trang index. Điều này có thể hỗ trợ kẻ tấn công bằng cách cho phép họ nhanh chóng xác định các tài nguyên tại một đường dẫn nhất định và đi thẳng vào phân tích, tấn công các tài nguyên đó. Nó đặc biệt làm tăng độ phơi bày của các tập tin nhạy cảm trong thư mục mà không dự kiến cho người dùng truy cập, như file tạm thời và crash dump.

Việc liệt kê thư mục tự nó không nhất thiết là một lỗ hổng bảo mật. Tuy nhiên, nếu website cũng không thực hiện kiểm soát truy cập đúng cách, việc tiết lộ sự tồn tại và vị trí của các tài nguyên nhạy cảm theo cách này rõ ràng là một vấn đề.

### Developer comments
---
Trong quá trình phát triển, đôi khi các chú thích inline trong HTML được thêm vào mã. Những chú thích này thường được loại bỏ trước khi deploy lên môi trường production. Tuy nhiên, những chú thích có thể bị quên, bị bỏ sót, hoặc thậm chí bị để lại do người nào đó không nhận thức đầy đủ về tác động bảo mật. Mặc dù những chú thích này không hiển thị trên trang đã render, chúng có thể dễ dàng truy cập bằng Burp, hoặc thậm chí bằng công cụ developer tích hợp của trình duyệt.

Thỉnh thoảng, những chú thích này chứa thông tin hữu ích cho kẻ tấn công. Ví dụ, chúng có thể gợi ý sự tồn tại của các thư mục ẩn hoặc cung cấp manh mối về logic ứng dụng.

### Error messages
---

Một trong những nguyên nhân phổ biến nhất gây rò rỉ thông tin là các thông báo lỗi quá chi tiết. Nguyên tắc chung là bạn nên chú ý kỹ tất cả các thông báo lỗi gặp phải trong quá trình audit.

Nội dung của thông báo lỗi có thể tiết lộ thông tin về đầu vào hay kiểu dữ liệu được mong đợi từ một tham số. Điều này giúp bạn thu hẹp phạm vi tấn công bằng cách xác định các tham số có thể khai thác. Nó thậm chí có thể ngăn bạn lãng phí thời gian thử những payload mà đơn giản là sẽ không hoạt động.

Các thông báo lỗi chi tiết cũng có thể cung cấp thông tin về các công nghệ khác nhau đang được trang web sử dụng. Ví dụ, chúng có thể nêu rõ engine template, loại cơ sở dữ liệu, hoặc máy chủ mà trang đang dùng, kèm theo số phiên bản. Thông tin này hữu ích vì bạn có thể dễ dàng tìm kiếm các exploit đã được công bố cho phiên bản đó. Tương tự, bạn có thể kiểm tra xem có lỗi cấu hình thường gặp hoặc các thiết lập mặc định nguy hiểm nào mà bạn có thể khai thác hay không. Một số trong đó có thể được nêu bật trong tài liệu chính thức.

Bạn cũng có thể phát hiện rằng trang web đang sử dụng một framework mã nguồn mở nào đó. Trong trường hợp đó, bạn có thể nghiên cứu mã nguồn sẵn có-một tài nguyên vô giá để dựng exploit cho riêng mình.

Sự khác biệt giữa các thông báo lỗi cũng có thể hé lộ những hành vi khác nhau đang diễn ra phía sau hậu trường. Quan sát khác biệt trong thông báo lỗi là khía cạnh then chốt của nhiều kỹ thuật, chẳng hạn như SQL injection, username enumeration, v.v.

### Debugging data
---

Vì mục đích gỡ lỗi, nhiều trang web tạo ra các thông báo lỗi và file log tùy chỉnh chứa rất nhiều thông tin về hành vi của ứng dụng. Mặc dù những thông tin này hữu ích trong quá trình phát triển, nhưng nếu bị lộ trong môi trường production thì chúng cũng cực kỳ hữu dụng cho kẻ tấn công.

Các thông điệp debug đôi khi chứa thông tin quan trọng để phát triển một cuộc tấn công, bao gồm:

- Giá trị của các biến phiên (session) quan trọng có thể bị thao tác qua dữ liệu do người dùng cung cấp.
- Tên host và thông tin đăng nhập cho các thành phần back-end.
- Tên file và thư mục trên máy chủ.
- Các khóa được dùng để mã hóa dữ liệu truyền qua client.

Thông tin gỡ lỗi đôi khi được ghi vào một file riêng. Nếu kẻ tấn công truy cập được file này, nó có thể là một tài liệu tham khảo hữu ích để hiểu trạng thái chạy của ứng dụng. Nó cũng cung cấp nhiều manh mối về cách họ có thể cung cấp input được chế tác để thao túng trạng thái ứng dụng và điều khiển thông tin thu được.

### User account pages
---

Theo bản chất, trang hồ sơ hoặc trang tài khoản của người dùng thường chứa thông tin nhạy cảm như địa chỉ email, số điện thoại, khóa API, v.v. Vì người dùng thông thường chỉ có quyền truy cập trang tài khoản của chính mình nên điều này tự nó không phải là một lỗ hổng. Tuy nhiên, một số trang web tồn tại lỗi logic có thể cho phép kẻ tấn công lợi dụng những trang này để xem dữ liệu của người dùng khác.

Ví dụ, hãy xem xét một trang web xác định trang tài khoản người dùng cần tải dựa trên tham số user:

```pgsql
GET /user/personal-info?user=carlos
```

Hầu hết các trang web đều có biện pháp ngăn chặn kẻ tấn công chỉ việc thay đổi tham số này để truy cập trang tài khoản của người dùng bất kỳ. Tuy nhiên, đôi khi logic dùng để tải từng phần dữ liệu riêng lẻ lại không chặt chẽ như vậy.

Kẻ tấn công có thể không thể tải toàn bộ trang tài khoản của người khác, nhưng logic để truy xuất và hiển thị, ví dụ, địa chỉ email đã đăng ký của người dùng có thể không kiểm tra xem tham số user có khớp với người dùng hiện đang đăng nhập hay không. Trong trường hợp đó, chỉ cần thay đổi tham số user có thể cho phép kẻ tấn công hiển thị địa chỉ email của bất kỳ người dùng nào trên chính trang tài khoản của mình.

Chúng ta sẽ tìm hiểu chi tiết hơn về các loại lỗ hổng này khi đi sâu vào chủ đề kiểm soát truy cập (access control) và IDOR (Insecure Direct Object References).

### Source code disclosure via backup files
---
Việc có quyền truy cập mã nguồn làm cho kẻ tấn công dễ hiểu hành vi ứng dụng và dựng các cuộc tấn công mức độ nghiêm trọng cao hơn. Đôi khi dữ liệu nhạy cảm còn được nhúng cứng trong mã nguồn. Ví dụ điển hình là API key và thông tin đăng nhập để truy cập các thành phần backend.

Nếu bạn nhận diện được một công nghệ mã nguồn mở cụ thể đang được sử dụng, điều này cho phép truy cập dễ dàng tới một lượng mã nguồn hạn chế (ví dụ mã nguồn công khai của thư viện/framework đó).

Thỉnh thoảng, thậm chí có thể khiến trang web tiết lộ chính mã nguồn của nó. Khi lập bản đồ một website, bạn có thể thấy một số file mã nguồn được tham chiếu rõ ràng. Đáng tiếc thay, việc yêu cầu những file đó thường không hiển thị mã nguồn. Khi một server xử lý các file có phần mở rộng đặc biệt, ví dụ `.php`, thường nó sẽ thực thi mã thay vì gửi mã thô về client. Tuy nhiên, trong một số tình huống, bạn có thể lừa trang web trả về nội dung file thay vì thực thi. Ví dụ, các trình soạn thảo văn bản thường tạo những file sao lưu tạm thời khi file gốc đang được chỉnh sửa. Những file sao lưu này thường được biểu thị bằng ký tự bổ sung, ví dụ thêm dấu ngã (~) vào tên file hoặc đổi sang phần mở rộng khác. Yêu cầu một file mã bằng phần mở rộng sao lưu đôi khi cho phép bạn đọc nội dung mã nguồn trong phản hồi.

### Information disclosure due to insecure configuration
---

Các trang web đôi khi dễ bị tổn thương do cấu hình không đúng. Điều này đặc biệt phổ biến do việc sử dụng rộng rãi các công nghệ bên thứ ba, với vô số tùy chọn cấu hình mà những người triển khai không nhất thiết hiểu rõ.

Trong những trường hợp khác, các nhà phát triển có thể quên tắt các tùy chọn gỡ lỗi khi đưa vào môi trường production. Ví dụ, phương thức HTTP TRACE được thiết kế cho mục đích chẩn đoán. Nếu được bật, máy chủ web sẽ phản hồi các yêu cầu dùng phương thức TRACE bằng cách phản chiếu chính xác yêu cầu đã nhận trong phần phản hồi. Hành vi này thường vô hại, nhưng thỉnh thoảng có thể dẫn tới rò rỉ thông tin, chẳng hạn như tên của các header xác thực nội bộ có thể được reverse proxy đính kèm vào yêu cầu.

### Version control history
---

Hầu như tất cả các trang web đều được phát triển bằng một dạng hệ thống quản lý phiên bản nào đó, chẳng hạn Git. Theo mặc định, một dự án Git lưu toàn bộ dữ liệu quản lý phiên bản trong một thư mục có tên `.git`. Đôi khi, các trang web vô tình để lộ thư mục này trong môi trường production. Trong trường hợp đó, bạn có thể truy cập nó bằng cách duyệt thẳng tới `/.git`.

Mặc dù thường không thực tế khi duyệt thủ công cấu trúc file thô và nội dung, có nhiều phương pháp để tải xuống toàn bộ thư mục `.git`. Sau đó bạn có thể mở nó bằng cài đặt Git trên máy cục bộ để truy cập lịch sử quản lý phiên bản của website. Lịch sử này có thể bao gồm các log chứa các thay đổi đã commit và nhiều thông tin thú vị khác.

Điều này có thể không cho bạn quyền truy cập toàn bộ mã nguồn, nhưng so sánh các diff sẽ cho phép bạn đọc các đoạn mã nhỏ. Giống như bất kỳ mã nguồn nào, bạn cũng có thể tìm thấy dữ liệu nhạy cảm được hard-code trong một số dòng đã thay đổi.

## Cách phòng tránh lỗ hổng tiết lộ thông tin
Việc ngăn chặn hoàn toàn các lỗ hổng tiết lộ thông tin là rất khó do có quá nhiều cách mà chúng có thể xảy ra. Tuy nhiên, có một số thực hành tốt nhất (best practices) mà bạn có thể áp dụng để giảm thiểu nguy cơ loại lỗ hổng này xuất hiện trong trang web của mình:

- Đảm bảo mọi người tham gia phát triển website đều nhận thức rõ thông tin nào được xem là nhạy cảm.
Đôi khi, những thông tin tưởng chừng vô hại lại hữu ích cho kẻ tấn công hơn bạn nghĩ. Việc nhấn mạnh những rủi ro này giúp tổ chức của bạn xử lý thông tin nhạy cảm an toàn hơn nói chung.

- Kiểm tra mã nguồn (audit) để phát hiện khả năng tiết lộ thông tin trong quy trình QA hoặc build.
Nhiều nhiệm vụ liên quan có thể tự động hóa được, chẳng hạn như loại bỏ chú thích của lập trình viên trước khi triển khai.

- Sử dụng thông báo lỗi chung chung càng nhiều càng tốt.
Không nên cung cấp cho kẻ tấn công các manh mối về hành vi của ứng dụng một cách không cần thiết.

- Kiểm tra kỹ rằng tất cả tính năng gỡ lỗi hoặc chẩn đoán đã bị vô hiệu hóa trong môi trường production.

- Đảm bảo bạn hiểu rõ các tùy chọn cấu hình và tác động bảo mật của mọi công nghệ bên thứ ba được triển khai.
Dành thời gian tìm hiểu và vô hiệu hóa bất kỳ tính năng hoặc cài đặt nào mà bạn không thực sự cần đến.