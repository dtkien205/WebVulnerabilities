# File Upload Vulnerabilities

- File Upload Vulnerabilities được xếp vào loại **Logic Vulnerability**

- Nếu chức năng Upload cho phép chúng ta upload bất cứ file gì, cho phép người dùng tải tệp lên hệ thống tệp của mình mà không xác thực đầy đủ các thông tin như tên, loại, nội dung hoặc kích thước lên hệ thống nằm ngoài thiết kế logic ban đầu thì đây có thể  là lỗi

- Giả sử, chức năng Upload Avt (*.png, *.jpg) cho phép upload file *.html *.php thì đây là lỗi

### Một số bài ví dụ:
- [n0s4n1ty 1 - PicoCTF2025](https://play.picoctf.org/practice/challenge/482?category=1&originalEvent=74&page=1)