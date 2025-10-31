# JWT attacks
JSON Web Token (JWT) là một định dạng chuẩn để gửi dữ liệu JSON được ký bằng mật mã giữa các hệ thống. Về lý thuyết, JWT có thể chứa bất kỳ loại dữ liệu nào, nhưng thường được dùng để gửi thông tin (“claims”) về người dùng như một phần của cơ chế xác thực, quản lý phiên làm việc và kiểm soát truy cập.

Khác với session token kiểu cổ điển, toàn bộ dữ liệu mà máy chủ cần được lưu phía client bên trong chính JWT. Điều này khiến JWT trở thành lựa chọn phổ biến cho các website phân tán cao, nơi người dùng cần tương tác liền mạch với nhiều máy chủ back-end.

JWT **có thể chứa bất kỳ loại dữ liệu nào**, nhưng thường được dùng để gửi **thông tin (claims) về người dùng** nhằm phục vụ:
  - **Xác thực (authentication)**
  - **Quản lý phiên làm việc (session handling)**
  - **Kiểm soát truy cập (access control)**

Với **session token cổ điển**, dữ liệu phiên được lưu trên **máy chủ**. Với **JWT**, **toàn bộ dữ liệu máy chủ cần dùng được lưu ở phía client (người dùng)** trong chính JWT đó. Điều này khiến JWT trở thành **lựa chọn phổ biến cho các trang web phân tán**, nơi người dùng cần **tương tác liền mạch với nhiều máy chủ backend khác nhau**.

## JWT format
Một **JWT** gồm **3 phần** được **phân tách bằng dấu chấm (.)**:
```php-template
<Header>.<Payload>.<Signature>
```

**Ví dụ:**
```
eyJraWQiOiI5MTM2ZGRiMy1jYjBhLTRhMTktYTA3ZS1lYWRmNWE0NGM4YjUiLCJhbGciOiJSUzI1NiJ9.
eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTY0ODAzNzE2NCwibmFtZSI6IkNhcmxvcyBNb250b3lhIiwic3ViIjoiY2FybG9zIiwicm9sZSI6ImJsb2dfYXV0aG9yIiwiZW1haWwiOiJjYXJsb3NAY2FybG9zLW1vbnRveWEubmV0IiwiaWF0IjoxNTE2MjM5MDIyfQ.
SYZBPIBg2CRjXAJ8vCER0LA_ENjII1JakvNQoP-Hw6GG1zfl4JyngsZReIfqRvIAEi5L4HV0q7_9qGhQZvy9ZdxEJbwTxRs_6Lb-fZTDpW6lKYNdMyjw45_alSCZ1fypsMWz_2mTpQzil0lOtps5Ei_z7mM7M8gCwe_AGpI53JxduQOaB5HkT5gVrv9cKu9CsW5MS6ZbqYXpGyOG5ehoxqm8DL5tFYaW3lB50ELxi0KsuTKEbD0t5BCl0aCR2MBJWAbN-xeLwEenaqBiwPVvKixYleeDQiBEIylFdNNIMviKRgXiYuAvMziVPbwSgkZVHeEdF5MQP1Oe2Spac-6IfA
```

### Header
- Là **JSON đã mã hóa base64url**, chứa **thông tin siêu dữ liệu về token**
    ```json
    {   
    "alg": "RS256",
    "kid": "9136ddb3-cb0a-4a19-a07e-eadf5a44c8b5"
    }
    ```
- `alg` chỉ thuật toán ký, `kid` là ID khóa.

### Payload
- Là **JSON chứa các thông tin (claims) về người dùng**
    ```json
    {
        "iss": "portswigger",
        "exp": 1648037164,
        "name": "Carlos Montoya",
        "sub": "carlos",
        "role": "blog_author",
        "email": "carlos@carlos-montoya.net",
        "iat": 1516239022
    }
    ```
- Dữ liệu này **có thể đọc và sửa dễ dàng** nếu ai đó có token.

### Signature
- Được tạo bằng cách **ký (sign) chuỗi** `<header>.<payload>` **bằng khóa bí mật hoặc khóa riêng.**

- Dùng để **xác minh tính toàn vẹn và xác thực nguồn gốc token.**

## JWT signature
Máy chủ phát hành token sẽ **tạo chữ ký (`signature`) bằng cách băm (`hash`) phần `header` và `payload`**.  
Trong một số trường hợp, **hash này còn được mã hóa thêm**. Quá trình này đều **dựa vào một khóa bí mật (secret signing key)**.

- **Đảm bảo tính toàn vẹn**:  
  Vì chữ ký được **tạo trực tiếp từ `header` và `payload`**,  
  → **chỉ cần thay đổi 1 byte** trong `header` hoặc `payload` sẽ khiến **chữ ký không khớp**.

- **Ngăn chỉnh sửa trái phép**:  
  Nếu **không biết khóa bí mật của máy chủ**,  
  → sẽ **không thể tạo ra chữ ký hợp lệ** cho `header` và `payload` bất kỳ.

> ✅ Nhờ vậy, máy chủ có thể **xác minh rằng dữ liệu trong JWT chưa bị chỉnh sửa kể từ khi phát hành**.

## JWT vs JWS vs JWE
- **Đặc tả JWT (JSON Web Token) rất hạn chế**:  Nó **chỉ định nghĩa một định dạng để biểu diễn thông tin (“claims”) dưới dạng JSON**  và có thể **truyền giữa hai bên**.

- Trong thực tế, **JWT hiếm khi được sử dụng như một thực thể độc lập**. Đặc tả JWT thường được **mở rộng bởi**:

  - **JSON Web Signature (JWS)** – định nghĩa **cách ký số dữ liệu trong JWT**
  - **JSON Web Encryption (JWE)** – định nghĩa **cách mã hóa dữ liệu trong JWT**

  → Nhờ đó, **JWT mới có thể được triển khai đầy đủ và an toàn trong thực tế**.

    Nói cách khác, **một JWT thường là JWS hoặc JWE**

<br>

📌 **Tóm lại:**  
 - **JWS = JWT đã ký số (signed)**  
 - **JWE = JWT đã mã hóa (encrypted)**

 ## Lỗ hổng bảo mật trước các cuộc tấn công JWT phát sinh như thế nào?
Các **lỗ hổng JWT thường phát sinh do việc xử lý JWT sai cách trong ứng dụng**. Bởi vì **các đặc tả JWT được thiết kế khá linh hoạt**, nên **nhà phát triển có thể tự quyết nhiều chi tiết triển khai** → điều này dễ dẫn đến **vô tình tạo ra lỗ hổng, dù dùng thư viện bảo mật tốt**.

**Các lỗi triển khai phổ biến**
- **Không xác minh chữ ký (`signature`) đúng cách**  
  → cho phép kẻ tấn công **chỉnh sửa dữ liệu trong `payload`** và gửi lại cho ứng dụng.

- **Rò rỉ hoặc yếu khóa bí mật (secret key)**  
  - Dù có xác minh chữ ký đúng cách, **JWT chỉ an toàn nếu khóa bí mật vẫn an toàn**.
  - Nếu khóa bị **rò rỉ, đoán được hoặc brute-force thành công**,  kẻ tấn công có thể **tự tạo JWT với chữ ký hợp lệ**,  **vô hiệu hóa toàn bộ cơ chế bảo mật dựa trên JWT**.

## Cách làm việc với JWT trong Burp Suite
**Read more:** 
[***Working with JWTs in Burp Suite***](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts)

## **Khai thác lỗi xác minh chữ ký JWT**
Theo thiết kế, **máy chủ thường không lưu trữ bất kỳ thông tin nào về JWT đã phát hành**.  Thay vào đó, **mỗi JWT là một thực thể độc lập, tự chứa toàn bộ dữ liệu cần thiết**.

✅ ***Ưu điểm***: dễ mở rộng, không cần lưu trạng thái phiên trên máy chủ.  
⚠️ ***Nhược điểm***: **máy chủ không biết nội dung gốc hoặc chữ ký gốc của token**, nên nếu **không xác minh chữ ký đúng cách**, **không có gì ngăn kẻ tấn công chỉnh sửa nội dung JWT**.

### Chấp nhận chữ ký tùy ý

---

Các **thư viện JWT thường cung cấp hai hàm riêng biệt**:

- `verify()` → **xác minh chữ ký (signature)** của token  
- `decode()` → **chỉ giải mã (decode) nội dung**, **không kiểm tra chữ ký**

Đôi khi lập trình viên **nhầm lẫn và chỉ gọi `decode()` với token đầu vào**. Điều này đồng nghĩa với việc **ứng dụng hoàn toàn không xác minh chữ ký**.

### Chấp nhận token không có chữ ký (alg: none)
---
Phần `header` của JWT chứa tham số `alg` — cho biết **thuật toán dùng để ký token**,  
và máy chủ sẽ **dựa vào giá trị này để chọn thuật toán xác minh chữ ký**.

**Ví dụ:**
```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

- `alg` là **dữ liệu do người dùng kiểm soát**, và khi token vừa đến server thì **chưa được xác minh.**
- Điều này nghĩa là **server buộc phải tin vào thông tin chưa được kiểm chứng** để quyết định cách xác minh chữ ký.
→ Kẻ tấn công có thể **tác động trực tiếp đến cách server xác minh token**, khiến **cơ chế bảo mật bị vô hiệu hóa.**

JWT có thể được **ký bằng nhiều thuật toán khác nhau**, nhưng **cũng có thể không được ký**. Trong trường hợp này, tham số `alg` sẽ được đặt thành `none`,  
  → cho biết đây là **“JWT không được bảo mật” (unsecured JWT)**.

Do **nguy cơ bảo mật rõ ràng**, **các máy chủ thường từ chối token không có chữ ký**. Tuy nhiên, vì **việc kiểm tra dựa vào phân tích chuỗi (string parsing)**,  nên **đôi khi có thể vượt qua bằng các kỹ thuật làm rối cổ điển**, chẳng hạn như:
  - **Viết hoa/thường trộn lẫn** (`NoNe`, `nOnE`, …)
  - **Mã hóa không mong đợi** (URL encoding, Unicode encoding, …)

> ⚠️ Nếu vượt qua được, kẻ tấn công có thể **gửi JWT không cần chữ ký hợp lệ** để **giả mạo bất kỳ người dùng nào**.

## **Brute-forcing secret keys**
Một số thuật toán như **HS256** dùng **chuỗi bí mật làm khóa ký JWT**, nên nếu **khóa yếu hoặc mặc định**, kẻ tấn công có thể **đoán/brute-force** để **tạo JWT hợp lệ và chiếm quyền truy cập**.

Lỗi thường gặp là **quên thay đổi khóa mặc định hoặc giữ nguyên khóa trong code mẫu**, khiến **máy chủ dễ bị brute-force khóa bí mật**.

### Brute-forcing secret keys using hashcat
---

Bạn có thể dùng **hashcat** để **brute-force khóa bí mật (secret key)** của JWT.
1. Chuẩn bị:
   - Một **JWT hợp lệ** từ máy chủ mục tiêu
   - Một **wordlist chứa các khóa bí mật phổ biến**

2. Chạy lệnh:
   ```bash
   hashcat -a 0 -m 16500 <jwt> <wordlist>
   ```
   - a 0 → tấn công từ điển (dictionary attack)
   - m 16500 → chế độ dành cho JWT (HMAC-SHA256)

- Hashcat sẽ **dùng từng khóa trong wordlist để ký lại phần header + payload** của JWT
- Sau đó **so sánh chữ ký mới với chữ ký gốc**. Nếu trùng, hashcat sẽ in ra kết quả:
    ```ruby
    <jwt>:<identified-secret>
    ```
    > ⚠️ Nếu chạy lại nhiều lần, dùng thêm `--show` để hiển thị kết quả đã tìm được.

## JWT header parameter injections

Theo đặc tả JWS, chỉ **`alg`** là bắt buộc. Thực tế JWT header thường có thêm:

- **`jwk`** (JSON Web Key): nhúng khóa JSON.  
- **`jku`** (JSON Web Key Set URL): URL chứa tập khóa (JWKS).  
- **`kid`** (Key ID): ID để chọn khóa.

👉 Các tham số này do client kiểm soát, có thể khiến server dùng **khóa của attacker** để xác minh. Kẻ tấn công có thể chèn JWT giả mạo ký bằng khóa riêng của mình thay vì bí mật của server.

### Chèn JWT tự ký thông qua tham số jwk

Đặc tả **JSON Web Signature** (JWS) mô tả một tham số header tùy chọn jwk, mà server có thể dùng để nhúng trực tiếp khoá công khai của nó vào trong token dưới định dạng JWK.

Ví dụ:
```json
{
    "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
    "typ": "JWT",
    "alg": "RS256",
    "jwk": {
        "kty": "RSA",
        "e": "AQAB",
        "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
        "n": "yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9m"
    }
}
```

**Nguy cơ**
- Server cấu hình sai có thể chấp nhận bất kỳ khóa nào trong jwk để xác minh.
- Attacker có thể ký JWT bằng **private key** của mình, rồi nhúng **public key** tương ứng vào **jwk**.

**Khai thác**
- Dùng Burp JWT Editor để sinh **RSA key**, chỉnh payload, rồi chọn tấn công **Embedded JWK**.
- Có thể làm thủ công: thêm **jwk** và chỉnh **kid** cho khớp.

### Chèn JWT tự ký thông qua tham số jku

Thay vì nhúng khóa công khai bằng `jwk`, một số server cho phép dùng **`jku`** — URL trỏ tới một **JWK Set** (một đối tượng JSON chứa mảng các JWK). Khi xác minh chữ ký, server sẽ tải JWK Set từ URL này rồi lấy khóa thích hợp.

**Ví dụ JWK Set**
```json
{
  "keys": [
    {
      "kty": "RSA",
      "e": "AQAB",
      "kid": "75d0ef47-af89-47a9-9061-7c02a610d5ab",
      "n": "o-yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y_qTVX67WhsN3JvaFYw-fhvsWQ"
    },
    {
      "kty": "RSA",
      "e": "AQAB",
      "kid": "d8fDFo-fS9-faS14a9-ASf99sa-7c1Ad5abA",
      "n": "fc3f-yy1wpYmffgXBxhAUJzHql79gNNQ_cb33HocCuJolwDqmk6GPM4Y_qTVX67WhsN3JvaFYw-dfg6DH-asAScw"
    }
  ]
}
```
Thông thường JWK Set được public tại endpoint tiêu chuẩn như `/.well-known/jwks.json`.

**Rủi ro**
- Server kém an toàn có thể tải khóa từ bất kỳ URL do client chỉ định và dùng khóa đó để xác minh — cho phép attacker dùng khóa của họ.
- Một số site chỉ chấp nhận tên miền tin cậy, nhưng có thể bypass bằng lỗi phân tích URL (ví dụ khai thác SSRF hoặc khác biệt parsing).

**Phòng ngừa**
- Chỉ cho phép tải từ danh sách trắng domain đáng tin cậy và kiểm tra kỹ URL.
- Tốt nhất: dùng kho khóa nội bộ/whitelist thay vì tin URL do client cung cấp.

### Chèn JWT tự ký thông qua tham số kid

`kid` là tham số header JWT dùng để cho server biết khóa nào để xác minh chữ ký. `kid` chỉ là một chuỗi do developer định nghĩa (có thể là ID DB, tên file, v.v.). Nếu server tìm khóa dựa vào `kid` mà không kiểm tra an toàn (ví dụ cho phép truy cập file hệ thống), attacker có thể buộc server dùng **tập tin bất kỳ** trên máy chủ làm khóa xác minh.

**Ví dụ tấn công (ý tưởng):**
```json
{
  "kid": "../../path/to/file",
  "typ": "JWT",
  "alg": "HS256",
  "k": "asGsADas3421-dfh9DGN-AFDFDbasfd8-anfjkvc"
}
```

Nếu server cho phép đọc file đó làm secret, attacker có thể ký JWT với nội dung của file. Trường hợp đơn giản nhất: trỏ đến `/dev/null (rỗng)` — ký với chuỗi rỗng sẽ hợp lệ nếu server đọc `/dev/null` làm secret.

Nguy hiểm đặc biệt: khi server hỗ trợ thuật toán đối xứng (HS*), attacker có thể ghi JWT hợp lệ bằng cách dùng secret trùng với nội dung file dự đoán được.

Nếu máy chủ lưu trữ khóa xác minh của nó trong database, tham số tiêu đề `kid` cũng là một vectơ tiềm ẩn cho các cuộc tấn công SQLi

### Các tham số tiêu đề JWT thú vị khác

- **`cty` (Content Type)**  
  - Mô tả kiểu nội dung của payload (ví dụ `text/xml`, `application/json`). Thường bị bỏ qua nhưng thư viện phân tích vẫn có thể hỗ trợ.  
  - Nếu đã bypass được kiểm tra chữ ký, attacker có thể chèn `cty: text/xml` hoặc `application/x-java-serialized-object` để kích hoạt **XXE** hoặc **deserialization** attack.

- **`x5c` (X.509 Certificate Chain)**  
  - Chứa chứng chỉ X.509 (public cert) hoặc chuỗi chứng chỉ dùng để xác minh chữ ký.  
  - Có thể bị lợi dụng để **chèn chứng chỉ self-signed** (tương tự `jwk` injection). Phân tích chứng chỉ phức tạp có thể mở thêm lỗ hổng trong parser (tham khảo các CVE liên quan).

## Tấn công nhầm lẫn thuật toán

### Symmetric vs Asymmetric

- **Symmetric (đối xứng) — ví dụ: HS256 (HMAC + SHA-256)**  
  - Server dùng **một khóa duy nhất** để **ký** và **xác minh** JWT.  
  - Khóa này phải được giữ bí mật tuyệt đối (như mật khẩu).  

- **Asymmetric (bất đối xứng) — ví dụ: RS256 (RSA + SHA-256)**  
  - Dùng **cặp khóa**:  
    - **Private key**: server dùng để ký JWT → phải giữ bí mật.  
    - **Public key**: bất kỳ ai cũng có thể dùng để xác minh JWT → có thể công khai.  

👉 Tóm lại: Symmetric = 1 khóa (bí mật), Asymmetric = 2 khóa (private + public).

### Lỗ hổng nhầm lẫn thuật toán phát sinh như thế nào?

Algorithm confusion xảy ra khi thư viện JWT dùng **`alg`** từ header token để quyết định cách xác minh, và server vô tình cho phép thay đổi thuật toán do client chỉ định. Kết quả: attacker có thể ép server dùng thuật toán khác (ví dụ HS256 thay cho RS256) để giả mạo token mà không cần biết khóa bí mật.

**Ví dụ đơn giản (pseudo-code):**
```pseudo
function verify(token, secretOrPublicKey){
    algorithm = token.getAlgHeader()
    if algorithm == "RS256" then
        // coi secretOrPublicKey là RSA public key
    else if algorithm == "HS256" then
        // coi secretOrPublicKey là HMAC secret
    end
}
```

Nhà phát triển có thể luôn truyền publicKey (của RSA) vào verify() vì nghĩ chỉ dùng RS256:
```pseudo
publicKey = <public-key-of-server>
token = request.getCookie("session")
verify(token, publicKey)
```
Nếu attacker gửi token với `alg: HS256` và ký bằng publicKey làm HMAC secret, thư viện sẽ xác minh token bằng HMAC với cùng **publicKey** - dẫn đến token giả hợp lệ.

### Thực hiện một cuộc tấn công gây nhầm lẫn thuật toán

**Step 1: Lấy khóa công khai (Public key) của máy chủ**

Máy chủ đôi khi công khai khóa công khai dưới dạng JWK qua endpoint tiêu chuẩn như `/jwks.json` hoặc `/.well-known/jwks.json.` Nhiều JWK được gom trong một JWK Set (một object JSON chứa mảng keys).
```json
{
  "keys": [
    {
      "kty": "RSA",
      "e": "AQAB",
      "kid": "75d0ef47-af89-47a9-9061-7c02a610d5ab",
      "n": "o-yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y_qTVX67WhsN3JvaFYw-fhvsWQ"
    },
    {
      "kty": "RSA",
      "e": "AQAB",
      "kid": "d8fDFo-fS9-faS14a9-ASf99sa-7c1Ad5abA",
      "n": "fc3f-yy1wpYmffgXBxhAUJzHql79gNNQ_cb33HocCuJolwDqmk6GPM4Y_qTVX67WhsN3JvaFYw-dfg6DH-asAScw"
    }
  ]
}
```
Ngay cả khi khóa không được công khai, bạn vẫn có thể trích xuất nó từ một cặp JWT hiện có.

**Step 2 - Chuyển đổi khóa công khai sang định dạng phù hợp**

Mặc dù máy chủ có thể công khai khóa công khai ở định dạng JWK, khi xác minh chữ ký một token, nó sẽ dùng bản sao khóa của chính nó từ hệ thống tệp cục bộ hoặc cơ sở dữ liệu. Bản sao này có thể được lưu ở định dạng khác.

Để cuộc tấn công có thể hoạt động, phiên bản khóa mà bạn dùng để ký JWT phải **đúng hoàn toàn** với bản sao cục bộ của máy chủ. Ngoài việc cùng định dạng, **từng byte** phải khớp, kể cả các ký tự không hiển thị.

Trong ví dụ này, giả sử chúng ta cần khóa ở định dạng X.509 PEM. Bạn có thể chuyển JWK sang PEM bằng tiện ích mở rộng JWT Editor của Burp như sau:

1. Với extension đã được nạp, trên thanh tab chính của Burp, vào tab **JWT Editor → Keys**.  
2. Nhấn **New RSA Key**. Trong hộp thoại, dán JWK bạn đã thu được.  
3. Chọn nút radio **PEM** và sao chép khóa PEM thu được.  
4. Chuyển sang tab **Decoder** và Base64-encode (mã hóa Base64) PEM đó.  
5. Quay lại tab **JWT Editor → Keys** và nhấn **New Symmetric Key**.  
6. Trong hộp thoại, nhấn **Generate** để tạo một khóa mới ở định dạng JWK.  
7. Thay giá trị được sinh cho tham số `k` bằng khóa PEM đã được Base64 hóa mà bạn vừa sao chép.  
8. Lưu khóa.

**Step 3 - Sửa đổi JWT**

Khi đã có khóa công khai ở định dạng phù hợp, bạn có thể tùy ý sửa đổi JWT. Chỉ cần đảm bảo tiêu đề thuật toán được đặt thành HS256.

**Step 4 - Ký JWT bằng khóa công khai**

Ký mã thông báo bằng thuật toán HS256 với khóa công khai RSA làm bí mật.

### Lấy khóa công khai từ các token hiện có
Trong trường hợp khóa công khai không có sẵn, bạn vẫn có thể kiểm tra sự nhầm lẫn của thuật toán bằng cách lấy khóa từ một cặp JWT hiện có. Quá trình này tương đối đơn giản bằng cách sử dụng các công cụ như `jwt_forgery.py`. Bạn có thể tìm thấy công cụ này, cùng với một số tập lệnh hữu ích khác, trên kho lưu trữ [***rsa_sign2n***](https://github.com/silentsignal/rsa_sign2n). Chạy với lệnh:
```
docker run --rm -it portswigger/sig2n <token1> <token2>
```

Một số công cụ có thể lấy **hai JWT** hiện có để suy ra một số ứng viên cho tham số `n` của khóa RSA server. Từ mỗi ứng viên có thể sinh ra khóa (PEM) và các JWT giả ứng viên; bằng cách gửi từng JWT này tới server, chỉ có **một** JWT sẽ được chấp nhận — khóa tương ứng là khóa khớp với server.