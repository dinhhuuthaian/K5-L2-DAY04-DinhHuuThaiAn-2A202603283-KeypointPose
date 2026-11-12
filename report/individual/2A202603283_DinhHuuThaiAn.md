# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`. Ví dụ: `20241234_NguyenVanAn.md`.

Dữ liệu: 12 ảnh người COCO val2017 (Lin et al., 2014) và 8 ảnh chân dung Wikimedia Commons, chỉ dùng trong lớp.

## 0. Thông tin học viên

- Họ tên: Đinh Hữu Thái An
- MSSV: 2A202603283
- Email: dinhhuuthaian9191@gmail.com
- Link repository: https://github.com/dinhhuuthaian/K5-L2-DAY04-DinhHuuThaiAn-2A202603283-KeypointPose
- Phiên bản CVAT (Help → About): 2.74.1
- Máy: hệ điều hành _Windows 10 (bản 10.0.19045)__ · RAM _16__ GB · chạy CVAT chế độ đầy đủ / lite
- Bộ ảnh (`src/exports/assignment.json` do `lab.py setup` tạo): có 
- Giờ bắt đầu: 16h30
- Giờ kết thúc: 19h

## 1. Kiểm tra label (CP0)

| Label | Kiểu | Số điểm | Tên điểm đúng bảng của lab? | Đúng thứ tự? | Số cạnh |
|---|---|---:|---|---|---:|
| `person` | Skeleton  | 17 | có | có | 19 |
| `face` | Skeleton | 13 | có | có | 13 |

Mẫu `person` dựng theo người quay mặt về camera (các điểm `left_*` nằm bên phải khung mẫu)? Có 

Cách đổi cờ `occluded` / `outside` cho **một điểm** trên phiên bản CVAT này (một câu): Nếu mà không thấy điểm đó và không xác định được vị trí điểm đó.

...

## 2. Số lượng đã gán và thời gian (CP1, CP2)

| Nhóm ảnh | Số ảnh | Số skeleton đã gán | Số người dưới 60 px (không gán) | Số poster / gương / màn hình bỏ qua | Thời gian (phút) |
|---|---:|---:|---:|---:|---:|
| `easy` | 5 | 5 | 0 | 0 | 40 |
| `occluded` | 3 | 5 | 0 | 0 | 25 |
| `back` | 2 | 4 | 0 | 0 | 20 |
| `small` | 1 | 2 | 0 | 0 | 15 |
| `crowd` | 1 | 3 | 0 | 0 | 20 |
| `faces` | 8 | 8 | — | 0 | 30 |

- Số ảnh người đã xong ở mốc phút 105: _10__ / 10
- Thời gian thực tế (phút): CP1 _90__ · CP2 _30__ · CP3 _20__
- Ảnh tốn thời gian nhất là ảnh nào, vì sao?
000000012552 là ảnh đầu tiên của person vì k tìm được chỗ đổi v1 v2 v0 như nào nên tốn thời gian một xíu
...

## 3. Bảng ca khó (CP1, CP2)

Mỗi điểm bạn phân vân một dòng, nhất là phân vân giữa `v = 1` và `v = 0`, hoặc không chắc hướng người.

| Ảnh | Người / mặt | Điểm | Cờ đã chọn | Phân vân giữa | Lý do chọn |
|---|---|---|---:|---|---|
|000000150192.jpg | person | left_wrist | v1 | v0 | vì nó vẫn xác định được vị trí |
| | | | | | |
| | | | | | |

## 4. Bảng tự review (CP3)

Đi từ ảnh cuối về ảnh đầu. 5 ảnh người (ít nhất 2 ảnh `back` hoặc `crowd`) và 3 ảnh mặt. Ít nhất 8 dòng, kể cả dòng `ok`. Ghi lỗi trước, sửa sau.

Mã lỗi dùng đúng một trong: `lr_swap`, `vis_flag`, `position`, `missing`, `extra`, `ok`.

| Ảnh | Người / mặt | Điểm | Mã lỗi | Ghi chú | Đã sửa? |
|---|---|---|---|---|---|
| 000000012552.jpg | person | right_knee | missing | bị che bởi người đằng sau và người đó đang ngồi sổm | Có, đổi sang occluded |
| 000000393909.jpg | person | left_elbow | missing | bị chú chó che mất nên k xác định được vị trí | Có, đổi sang occluded |
| face_255797.jpg | face | left_eye, right_eye | vis_flag | Mắt bị kính râm che khuất, không thể xác định chính xác vị trí các điểm landmark mắt. | Giữ nguyên, đánh dấu vùng mắt bị che khuất |
| face_185015.jpg | face | ok | ok | Các điểm landmark mắt, mũi và miệng được xác định tương đối chính xác, không bị che khuất | Không cần sửa |
| face_145751.jpg | face | ok | ok | Các điểm landmark mắt, mũi và miệng được xác định tương đối chính xác, không bị che khuất | Không cần sửa |
| | | | | | |
| | | | | | |
| | | | | | |

Tổng hợp số lỗi theo mã:

| `lr_swap` | `vis_flag` | `position` | `missing` | `extra` | `ok` |
|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 0 | 2 | 0 | 0 |

Điểm còn phân vân giữa `v = 1` và `v = 0` (ghi cả hai lựa chọn và lý do chọn): có nhiều điểm bị che khuất khá nặng nhưng mà em nghĩ là vẫn có thể xác định được vị trí thì em vẫn để v = 1

...

## 5. Kiểm file xuất và kết quả tự kiểm (CP4)

Tự kiểm tay trong file JSON:

| File | Người / mặt kiểm (ảnh, thứ tự) | Số phần tử `keypoints` | Điểm `outside` ra `v = 0`, `occluded` ra `v = 1`? | `num_keypoints` khớp? |
|---|---|---:|---|---|
| `dinhhuuthaian_persons.zip` | Person (000000308257.jpg) | 16 | có | có |
| `dinhhuuthaian_persons.zip` | person(000000314154.jpg) | 15 | có | có |
| `dinhhuuthaian_faces.zip` | face(face_92028.jpg) | 13 | | có |

Sau khi xuất, CVAT ghi `occluded` thành `v = ___` và `outside` thành `v = ___`. Tọa độ của điểm `outside` trong file là `0, 0` hay tọa độ cũ? ___

Hai job đã chuyển sang completed trên CVAT? Có 

Dán phần **TÓM TẮT** in ra từ `src/check_submission.py`:

```text
- File person: DinhHuuThaiAn_persons.zip
  Số ảnh: 12 · số skeleton `person`: 19 · mỗi annotation 51 số
  Skeleton theo ảnh: 000000012552=3, 000000150192=2, 000000183176=1, 000000210604=2, 000000297227=2, 000000308257=1, 000000314154=1, 000000365099=1, 000000390585=1, 000000393909=2, 000000445187=1, 000000467300=2
  Cờ v: v=2 214 (66%) · v=1 34 (11%) · v=0 75 (23%)
  num_keypoints trung bình: 13.1
- File face: DinhHuuThaiAn_faces.zip
  Số ảnh: 8 · số skeleton `face`: 8 · mỗi annotation 39 số
  Skeleton theo ảnh: face_125051=1, face_145751=1, face_185015=1, face_255797=1, face_264124=1, face_38721=1, face_504911=1, face_92028=1
  Cờ v: v=2 104 (100%) · v=1 0 (0%) · v=0 0 (0%)
  num_keypoints trung bình: 13.0
- Ghi chú: 23 điểm v = 0 vẫn mang tọa độ cũ (CVAT 2.x xuất như vậy; chuẩn COCO ghi 0, 0). Không phải lỗi: điểm v = 0 bị bỏ qua khi huấn luyện và khi chấm.
- Số [LỖI]: 0 · số [CẢNH BÁO]: 3
Kết quả: ĐẠT (đọc lại từng cảnh báo ở trên)
```

Các `[CẢNH BÁO]` còn giữ nguyên và lý do:
   [CẢNH BÁO] 000000012552.jpg #1: cặp knee, ankle nằm ngược phía so với các cặp còn lại. Có thể đổi trái/phải một cặp (`lr_swap`), hoặc tay / chân bắt chéo thật: kiểm lại.
  [CẢNH BÁO] 000000150192.jpg #1: các điểm chỉ trải cao 43 px (< 60 px). Người dưới 60 px không gán; nếu người cao hơn nhưng bị cắt khung thì bỏ qua cảnh báo này.
  [CẢNH BÁO] 000000308257.jpg #1: cặp ankle nằm ngược phía so với các cặp còn lại. Có thể đổi trái/phải một cặp (`lr_swap`), hoặc tay / chân bắt chéo thật: kiểm lại.
...

## 6. Ảnh chụp màn hình

1. Label `person` trong label constructor (đủ 17 điểm có tên):

   ![Label person](images/1_label_person.png)

2. Một người quay lưng đã gán, cờ đã đặt:

   ![Người quay lưng](images/2_nguoi_quay_lung.png)

3. Một khuôn mặt đã gán 13 điểm, phóng to vùng mắt:

   ![Khuôn mặt phóng to](images/3_mat_phong_to.png)

4. Một đoạn JSON xuất của một người:

   ![JSON export](images/4_json_export.png)

Nguồn ảnh: COCO val2017 / Wikimedia Commons.

## 7. Tự đánh giá

1. Lỗi bạn mắc nhiều nhất hôm nay, và cách bạn sẽ tránh ở dự án thật:

   Lỗi nhiều nhất là gán trái/phải không nhất quán ở người quay lưng, Ở dự án thật, em sẽ chốt quy tắc trước khi gán ("trái/phải theo cơ thể người trong ảnh, không theo người xem"), gán xong một ảnh quay lưng thì kiểm lại cặp vai, hông, cổ chân trước khi sang ảnh khác, và chạy script kiểm tra sau mỗi lượt xuất

2. Một quy tắc bạn đề xuất thêm vào guideline (kèm ảnh ví dụ nếu có):

  Với người quay lưng hoặc nghiêng, luôn gán trái/phải theo cơ thể người trong ảnh, và đặt điểm đầu tiên ở vai trái của người đó để làm mốc đối chiếu cho các điểm còn lại

3. Nhãn của bạn đi vào model ở đâu? Chọn một lỗi bạn đã sửa và nói nó sẽ làm model học sai thế nào (heatmap, trọng số trong loss, hay bước lật ảnh):

   Lấy lỗi đảo trái/phải ở cặp ankle. Nếu nhãn bị đảo, model sẽ học sai ở bước lật ảnh: khi lật ngang ảnh để augment, hệ thống hoán đổi cặp trái/phải theo danh sách `flip_pairs`, nên một điểm gán sai bên sẽ bị hoán đổi thành sai thêm một lần nữa và model nhận hai tín hiệu mâu thuẫn cho cùng một khớp

## 8. Khó khăn và lỗi kỹ thuật

- **Đăng nhập CVAT thất bại hai lần Script nhập mật khẩu ẩn nên không thấy mình gõ gì
- **File zip xuất không mở được trong VS Code** (báo là file nhị phân).
- **Tọa độ của điểm `v = 0` không nhất quán trong file xuất:** một số điểm giữ tọa độ cũ

## Bonus (nếu làm)

### B1 — 3 ảnh người khó thêm

| Ảnh | Số skeleton | Số người dưới 60 px | Ca khó nhất |
|---|---:|---:|---|
| | | | |
| | | | |
| | | | |

Kết quả `src/check_submission.py` cho `HoVaTen_bonus_persons.zip`:

```text
(dán ở đây)
```

### B2 — 5 ảnh khuôn mặt đen trắng / hồng ngoại

Ảnh không màu khó hơn ở điểm nào? Kính râm trên ảnh hồng ngoại có còn là `v = 1` không?

...

### B3 — Model so với nhãn của tôi (không tính điểm)

- Demo đã dùng:
- Ảnh đã thử:

1. Model có trả điểm cho khớp bị che, hay khớp ngoài ảnh không? Confidence ở các điểm đó thế nào?

   ...

2. Với người quay lưng, model có đổi trái/phải không?

   ...

3. Bộ điểm của model có giống 17 điểm COCO không?

   ...

## 9. Tài liệu tham khảo và công cụ AI đã dùng

...
