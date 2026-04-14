from PIL import Image, ImageDraw, ImageFont
import os


def add_seat_range(seat_data, area, row, start_seat, end_seat):
    """把某一排的一个座位范围加入列表"""
    for seat in range(start_seat, end_seat + 1):
        seat_data.append({
            "area": area,
            "row": row,
            "seat": seat
        })


def build_seat_data():
    """按照规则生成所有座位数据(示例,以艺嘉楼大礼堂为例)"""
    seat_data = []

    # A区
    add_seat_range(seat_data, "A", 1, 1, 15)
    add_seat_range(seat_data, "A", 2, 1, 16)
    add_seat_range(seat_data, "A", 3, 1, 17)
    add_seat_range(seat_data, "A", 4, 1, 18)
    add_seat_range(seat_data, "A", 5, 1, 19)
    for row in range(6, 13):
        add_seat_range(seat_data, "A", row, 1, 20)

    # B区
    add_seat_range(seat_data, "B", 1, 16, 23)
    add_seat_range(seat_data, "B", 2, 17, 24)
    add_seat_range(seat_data, "B", 3, 18, 27)
    add_seat_range(seat_data, "B", 4, 19, 30)
    add_seat_range(seat_data, "B", 5, 20, 31)
    add_seat_range(seat_data, "B", 6, 21, 32)
    add_seat_range(seat_data, "B", 7, 21, 34)
    add_seat_range(seat_data, "B", 8, 21, 36)
    for row in range(9, 13):
        add_seat_range(seat_data, "B", row, 21, 38)

    # C区
    add_seat_range(seat_data, "C", 13, 1, 19)
    for row in range(14, 23):
        add_seat_range(seat_data, "C", row, 1, 20)
    add_seat_range(seat_data, "C", 23, 1, 19)

    # D区
    add_seat_range(seat_data, "D", 13, 20, 37)
    for row in range(14, 16):
        add_seat_range(seat_data, "D", row, 21, 38)
    for row in range(16, 23):
        add_seat_range(seat_data, "D", row, 21, 44)

    return seat_data


def generate_tickets():
    # 1. 基础配置
    template_path = "picture.png"
    output_dir = "output_tickets"
    font_path = "msyh.ttc"

    # 字体大小，需调参
    font_size = 25

    # 2. 坐标配置（使用Windows自带的打开方式“画图”，查找位置）
    coord_area = (1215, 136)  # “区”前填写位置
    coord_row = (1291, 136)   # “排”前填写位置
    coord_seat = (1364, 136)  # “座”前填写位置

    # 纯白色
    text_color = (255, 255, 255)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 检查模板图
    if not os.path.exists(template_path):
        print(f"未找到模板图片：{template_path}")
        return

    # 检查字体
    if not os.path.exists(font_path):
        print(f"未找到字体文件：{font_path}")
        return

    # 加载字体
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"字体加载失败：{e}")
        return

    # 3. 生成所有座位数据
    # 测试阶段可将下面改为单张
    seat_data = build_seat_data()

    total = len(seat_data)
    print(f"共需生成 {total} 张票。")

    # 4. 批量生成
    for index, data in enumerate(seat_data, start=1):
        img = Image.open(template_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 文字内容
        area_text = data["area"]
        row_text = str(data["row"])
        seat_text = str(data["seat"])

        # 写字
        # anchor="md"：以坐标点为“水平居中、文字底部”对齐
        # 适合写在横线附近
        draw.text(coord_area, area_text, font=font, fill=text_color, anchor="md")
        draw.text(coord_row, row_text, font=font, fill=text_color, anchor="md")
        draw.text(coord_seat, seat_text, font=font, fill=text_color, anchor="md")

        # 文件名
        filename = f"ticket_{area_text}区_{row_text}排_{seat_text}座.png"
        save_path = os.path.join(output_dir, filename)

        # 保存
        img.save(save_path)
        print(f"[{index}/{total}] 已生成: {filename}")

    print("全部生成完成。")


if __name__ == "__main__":
    generate_tickets()