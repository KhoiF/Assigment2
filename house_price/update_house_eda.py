import json

with open('code.ipynb', 'r') as f:
    nb = json.load(f)

# Find the EDA section
new_cells = []
in_eda = False
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown' and '7. Exploratory Data Analysis' in ''.join(cell['source']):
        new_cells.append(cell)
        
        # Insert the exact cells from the PDF
        new_cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': ["Quan sát phân phối Price, outlier và mối quan hệ giữa Area với Price. Giá nhà có thể lệch phải do một số bất động sản có giá rất cao."]
        })
        
        code1 = """fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(df['Price'].dropna(), bins=50, kde=True, color="#2E86C1", ax=axes[0])
axes[0].set_title("Phân phối Price")

sns.scatterplot(data=df, x="Area", y="Price", alpha=0.35, color="#E45756", ax=axes[1])
axes[1].set_title("Mối quan hệ Area và Price")

plt.tight_layout()
plt.show()"""
        new_cells.append({'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': [line + '\n' for line in code1.split('\n')]})

        new_cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': ["Phân phối Price tập trung chủ yếu trong khoảng 4–8, với mật độ cao nhất xung quanh 5–7.\nBiểu đồ Area–Price cho thấy phần lớn bất động sản có diện tích dưới khoảng 150 m²."]
        })

        new_cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': ["Quan sát phân bố dữ liệu ở 3 feature tương quan mạnh"]
        })

        code2 = """floor_counts = df["Floors"].value_counts().sort_index()
plt.figure(figsize=(8, 4))
sns.barplot(x=floor_counts.index, y=floor_counts.values, color="#4C78A8")
plt.title("Phân phối số tầng")
plt.xlabel("Số tầng")
plt.ylabel("Số lượng nhà")
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.show()"""
        new_cells.append({'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': [line + '\n' for line in code2.split('\n')]})
        
        new_cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': ["Biểu đồ cho thấy đa số các nhà sẽ từ 2 - 5 tầng, một số 1 tầng, và một số ít 6 và 7 tầng"]
        })

        code3 = """bedroom_counts = df["Bedrooms"].value_counts().sort_index()
plt.figure(figsize=(8, 4))
sns.barplot(x=bedroom_counts.index, y=bedroom_counts.values, color="#54A24B")
plt.title("Phân phối số phòng ngủ")
plt.xlabel("Số phòng ngủ")
plt.ylabel("Số lượng nhà")
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.show()"""
        new_cells.append({'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': [line + '\n' for line in code3.split('\n')]})

        in_eda = True
        continue
    
    if in_eda and cell['cell_type'] == 'markdown' and '8. Train/Test Split' in ''.join(cell['source']):
        in_eda = False
    
    if not in_eda:
        new_cells.append(cell)

nb['cells'] = new_cells

with open('code.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

