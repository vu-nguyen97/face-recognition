### Cấu hình chung:

- IDE: Visual studio code: Search và cài extensions: Python
- Cài Docker desktop (trên window)
- Cài python version 3.x.x
  => Sau bước này: check lại version:
  docker --version
  python --version

### Giải thích folder source code:

- app.py: file sẽ gọi đầu tiên khi ứng dụng chạy thành công
- Dockerfile: file cấu hình để chạy docker
- requirements.txt

### Chạy project: (đảm bảo đã bật docker desktop)

    B1. Chạy docker trên terminal để build một image có tên "face_recognition" bằng lệnh:
    	"docker build -t face_recognition ."
    B2. Chạy LẦN ĐẦU trên terminal để tạo container từ image face_recognition B1:
    	"docker run -p 8000:8000 face_recognition"
    Note: Từ lần chạy thứ 2, chỉ cần mở Docker desktop và chạy container tương ứng.

### List api:

1. http://localhost:8000/face

- Method: POST
- Body (form-data) với các params:
  - file (định dạng File): ảnh cần upload và lưu vào DB
    -> Return {"message": "Add face successfully"}

2. http://localhost:8000/check-face

- Method: POST
- Body (form-data) với các params:
  - file (định dạng File): ảnh cần compare với trong DB (mặc định của thư viện là lớn hơn 60% là khớp)
  - type (định dạng Text): 0 (fixed)
    -> Return {"message": "Ảnh khớp"}
