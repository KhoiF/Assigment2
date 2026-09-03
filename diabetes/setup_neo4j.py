import os
from neo4j import GraphDatabase

# --- Cấu hình Neo4j ---
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password') # Sửa thành mật khẩu của bạn nếu không dùng biến môi trường
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', 'neo4j')

# --- Dữ liệu Knowledge Graph từ Nhà thuốc Long Châu ---
ARTICLES = [
    {
        "id": "longchau_01",
        "title": "Bệnh tiểu đường: Nguyên nhân, triệu chứng và cách điều trị",
        "url": "https://nhathuoclongchau.com.vn/benh/tieu-duong-dai-thao-duong"
    },
    {
        "id": "longchau_02",
        "title": "Chế độ ăn cho người tiểu đường giúp ổn định đường huyết",
        "url": "https://nhathuoclongchau.com.vn/bai-viet/che-do-an-cho-nguoi-tieu-duong.html"
    }
]

DIET_ADVICES = [
    {
        "id": "diet_1",
        "title": "Hạn chế đường và tinh bột tinh chế",
        "content": "Giảm thiểu tiêu thụ các loại thực phẩm chứa nhiều đường tinh luyện, ngũ cốc đã qua chế biến kỹ, khoai tây và trái cây sấy khô để tránh tăng đường huyết đột ngột.",
        "duration": "Thường xuyên",
        "frequency": "Hàng ngày",
        "source": "longchau_02"
    },
    {
        "id": "diet_2",
        "title": "Ưu tiên rau xanh và trái cây có GI thấp",
        "content": "Tăng cường ăn các loại rau xanh (súp lơ, bông cải xanh, măng tây, bí đao...) và trái cây tươi có chỉ số đường huyết thấp (cam, quýt, bưởi, táo, ổi...).",
        "duration": "Thường xuyên",
        "frequency": "Mỗi bữa ăn",
        "source": "longchau_02"
    }
]

LIFESTYLE_ACTIONS = [
    {
        "id": "life_1",
        "title": "Tập thể dục thường xuyên",
        "content": "Tập thể dục giúp cải thiện độ nhạy insulin và kiểm soát cân nặng, từ đó giúp ổn định đường huyết tốt hơn.",
        "duration": "Ít nhất 30 phút/ngày",
        "frequency": "150 phút/tuần",
        "source": "longchau_01"
    }
]

DRUG_INFOS = [
    {
        "id": "drug_1",
        "title": "Tuân thủ phác đồ điều trị của bác sĩ",
        "content": "Dùng thuốc hạ đường huyết đúng liều lượng, đúng giờ. Tuyệt đối không tự ý ngưng thuốc ngay cả khi đường huyết đã ổn định mà chưa có ý kiến của bác sĩ.",
        "duration": "Theo chỉ định",
        "frequency": "Hàng ngày",
        "source": "longchau_01"
    },
    {
        "id": "drug_2",
        "title": "Thuốc phòng ngừa biến chứng",
        "content": "Ngoài thuốc hạ đường huyết, bác sĩ có thể chỉ định thêm các loại thuốc nhằm bảo vệ và phòng ngừa biến chứng tại thận, hệ thần kinh và tim mạch.",
        "duration": "Lâu dài",
        "frequency": "Theo chỉ định",
        "source": "longchau_01"
    }
]

COMPLICATIONS = [
    {
        "id": "comp_1",
        "title": "Biến chứng tim mạch",
        "content": "Gia tăng nguy cơ mắc bệnh mạch vành, nhồi máu cơ tim và đột quỵ nếu đường huyết không được kiểm soát tốt trong thời gian dài.",
        "duration": "Âm thầm tiến triển",
        "frequency": "Nguy cơ cao",
        "source": "longchau_01"
    },
    {
        "id": "comp_2",
        "title": "Tổn thương thần kinh và loét bàn chân",
        "content": "Có thể gây tê bì, mất cảm giác ở các chi, làm tăng nguy cơ nhiễm trùng và loét bàn chân, thậm chí phải đoạn chi.",
        "duration": "Mạn tính",
        "frequency": "Nguy cơ cao",
        "source": "longchau_01"
    },
    {
        "id": "comp_3",
        "title": "Tổn thương thận và mắt",
        "content": "Tiểu đường là nguyên nhân hàng đầu gây suy thận và bệnh võng mạc tiểu đường, có thể dẫn đến mù lòa.",
        "duration": "Mạn tính",
        "frequency": "Nguy cơ cao",
        "source": "longchau_01"
    }
]


def seed_database():
    print(f"Connecting to Neo4j at {NEO4J_URI}...")
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        # Test connection
        driver.verify_connectivity()
    except Exception as e:
        print(f"Failed to connect to Neo4j. Lỗi: {e}")
        print("Vui lòng đảm bảo Neo4j đang chạy và cấu hình (URI, USERNAME, PASSWORD) đã được thiết lập đúng.")
        return

    with driver.session(database=NEO4J_DATABASE) as session:
        # Xoá dữ liệu cũ về diabetes (tuỳ chọn)
        session.run("MATCH (n) DETACH DELETE n")
        print("Đã xoá toàn bộ dữ liệu cũ trong database.")

        # 1. Tạo node Bệnh
        session.run("""
            MERGE (d:Disease {id: 'diabetes'})
            SET d.name = 'Bệnh đái tháo đường'
        """)

        # 2. Tạo nodes Nguồn bài viết (Articles)
        for art in ARTICLES:
            session.run("""
                MERGE (a:Article {id: $id})
                SET a.title = $title, a.url = $url
            """, id=art["id"], title=art["title"], url=art["url"])

        # 3. Hàm hỗ trợ tạo các node item và link tới Disease & Article
        def create_items_and_relations(items, relation_type):
            for item in items:
                session.run(f"""
                    MATCH (d:Disease {{id: 'diabetes'}})
                    MATCH (a:Article {{id: $source_id}})
                    MERGE (i:Item {{id: $item_id}})
                    SET i.title = $title,
                        i.content = $content,
                        i.duration = $duration,
                        i.frequency = $frequency
                    MERGE (d)-[:{relation_type}]->(i)
                    MERGE (i)-[:SOURCED_FROM]->(a)
                """, item_id=item["id"], title=item["title"], content=item["content"], 
                     duration=item["duration"], frequency=item["frequency"], 
                     source_id=item["source"])

        # Thực thi tạo nodes & relationships
        create_items_and_relations(DIET_ADVICES, 'HAS_DIET_ADVICE')
        create_items_and_relations(LIFESTYLE_ACTIONS, 'HAS_LIFESTYLE_ACTION')
        create_items_and_relations(DRUG_INFOS, 'HAS_DRUG_INFO')
        create_items_and_relations(COMPLICATIONS, 'HAS_COMPLICATION')

        print("Đã thiết lập thành công Knowledge Graph (Neo4j) dựa trên thông tin từ Nhà thuốc Long Châu!")

    driver.close()

if __name__ == "__main__":
    seed_database()
