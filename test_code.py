data = [("CS304", 2025, 97, "A"), ("ECON101", 2025, 100, "A")]

# Dùng generator expression (cách hiệu quả và gọn gàng nhất)
total_score = sum(row[2] for row in data)

print(f"Tổng điểm là: {total_score}")
# Kết quả: Tổng điểm là: 197
