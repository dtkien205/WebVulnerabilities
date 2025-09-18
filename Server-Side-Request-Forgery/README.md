# Server Side Request Forgery (SSRF)

- Xử lý giá trị URL do người dùng nhập vào

### Cách tìm lõ hổng
- Step 1: Tìm kiếm các chức năng liên quan tới URL
- Step 2: Tìm kiếm các Parameters có liên quan tới URL
- Step 3: Sử dụng payload để xác định


#### Out of Band

- http://127.0.0.1:1337
- file:///etc/passwd
- http://example.com

### Bypass Blacklist Filter
- Convert IP to decimal
- Bypass DNS Record (http://fbi.com <-> localhost, 127.0.0.1)
- Redirection

### Bài ví dụ:
- Upload File Via URL
- Easy SSRF
- Crawling
- Difference Check (DNS Rebinding)
- HTML to pdf
