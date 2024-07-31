# MÔI TRƯỜNG UBUNTU SERVER

### 1. SSH

- Mở terminal => "ssh ubuntu@192.168.1.244" => nhập pass server

### 2. Ping

- Check server:

  - Thử "ping google.com" và "ping github.com"
  - Nếu ko được thì search lại hoặc làm:

    - B1. "cat /etc/resolv.conf"
    - B2. thêm 2 dòng sau và lưu file ở B1

    ```sh
      nameserver 8.8.8.8
      nameserver 8.8.4.4
    ```

    - B3: sudo systemctl restart network-manager

### 3. Setup git

- B1. Cấu hình git trên server:
  git config --global user.name "Your Name"
  git config --global user.email "youremail@example.com"
- B2: Chạy
  git clone https://github.com/vu-nguyen97/face-recognition.git

- Note: Nếu ko đăng nhập dc với user + pass của github thì có thể tự gen token "personal access token"
- Kết thúc là clone dc project

### 4. Cài docker

- https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
  Cài với link trên, chỉ cần mục "install using the repository"
- Check "docker -v"

### 5. Cài project

    B1: cd face-recognition
    B2: sudo docker build -t face_recognition .
    B3: sudo docker run -p 8000:8000 --name face face_recognition

- Check readme của project (https://github.com/vu-nguyen97/face-recognition/blob/main/README.md)
- Kiểm tra lại: "sudo docker ps" để xem cái container của face_recognition đang chạy
- "curl -X POST http://localhost:8000/check-face" => sẽ lỗi "No file part" là đúng (do chưa truyền ảnh) => API WORK trên ubuntu !!!!

### 6. Check kết nối trên postman local

- Thử telnet 192.168.1.244 8000
- curl -X POST http://192.168.1.244:8000/check-face trên cmd thành công
- Nếu ko call dc trên local (lỗi 503 server unavailable), thử:
  - Check log server: sudo docker logs face
  - Kiểm tra trạng thái Firewall trên Ubuntu: "sudo ufw status"
  - Đảm bảo rằng cổng 8000 được phép: "sudo ufw allow 8000"
  - Nhờ mở (check) port 8000 của server

# MÔI TRƯỜNG LOCAL

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
