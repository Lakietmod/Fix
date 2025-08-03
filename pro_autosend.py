from datetime import datetime, timedelta
import random
import threading
import time
from zlapi.models import *
import pytz
import requests
import json
from core.bot_sys import get_user_name_by_id, read_settings, write_settings

time_poems = {
    "01:00": [
        "🌙✨ Đêm khuya vang, giấc mơ đây, ngủ ngon nhé!",
        "🌌💤 Gió lạnh ru, lòng nhẹ bay, nghỉ thôi nào!",
        "🌃❄️ 1 giờ sáng, chân ấm đây, mơ đẹp nha!",
        "🌜🌠 Trăng mờ ảo, giấc mơ bay, ngủ thật sâu!",
        "✨🌙 Đêm sâu lắng, mắt nhắm ngay, nghỉ ngơi nào!",
        "🌌💫 Sao lung linh, đêm yên đây, ngủ ngon thôi!",
        "🌃🌬️ Khuya tĩnh lặng, giấc mơ đây, nghỉ ngơi nhé!",
        "🌙❄️ Đêm lạnh lắm, chân kéo đây, mơ đẹp nào!",
        "🌠✨ Trăng dịu dàng, lòng nhẹ bay, ngủ thật sâu!",
        "🌜🌌 1 giờ rồi, đừng thức nữa, nghỉ thôi nha!",
        "✨💤 Đêm yên bình, giấc mơ đây, ngủ ngon nhé!",
        "🌙🌠 Gió khuya lạnh, mắt nhắm đây, nghỉ ngơi thôi!",
        "🌌❄️ Đêm sâu thẩm, chân ấm bay, mơ đẹp nha!",
        "🌃✨ Khuya vắng vẻ, lòng nhẹ đây, ngủ thật sâu!",
        "🌜💫 Trăng lặng lẽ, giấc mơ đây, nghỉ ngơi nào!"
    ],
    "02:30": [
        "🌙🌌 Khuya lạnh lắm, giấc mơ đây, ngủ ngon nhé!",
        "🌃✨ Đêm sâu lắng, chân kéo ngay, nghỉ thôi nào!",
        "🌜💤 Gió khuya ru, lòng nhẹ bay, mơ đẹp nha!",
        "🌠❄️ 2 rưỡi sáng, mắt nhắm đây, ngủ thật sâu!",
        "✨🌙 Đêm tĩnh lặng, giấc mơ bay, nghỉ ngơi thôi!",
        "🌌💫 Sao lấp lánh, chân ấm đây, ngủ ngon nào!",
        "🌃🌬️ Khuya yên bình, giấc mơ đây, nghỉ ngơi nhé!",
        "🌙❄️ Đêm sâu thẩm, lòng nhẹ bay, mơ đẹp thôi!",
        "🌠✨ Trăng mờ ảo, giấc mơ đây, ngủ thật sâu!",
        "🌜🌌 2 giờ hơn, đừng thức nữa, nghỉ ngơi nha!",
        "✨💤 Đêm lạnh lắm, chân kéo đây, ngủ ngon nhé!",
        "🌙🌠 Gió hát ru, giấc mơ bay, nghỉ thôi nào!",
        "🌌❄️ Khuya tĩnh lặng, mắt nhắm đây, mơ đẹp nha!",
        "🌃✨ Đêm sâu lắng, lòng nhẹ đây, ngủ thật sâu!"
    ],
    "04:00": [
        "🌃🌙 Đêm khuya lạnh, giấc mơ đây, ngủ ngon nhé!",
        "🌜✨ 4 giờ sáng, chân ấm bay, nghỉ thôi nào!",
        "🌌💤 Gió lạnh ru, lòng nhẹ đây, mơ đẹp nha!",
        "🌠❄️ Đêm tĩnh lặng, mắt nhắm ngay, ngủ thật sâu!",
        "✨🌙 Trăng mờ ảo, giấc mơ bay, nghỉ ngơi thôi!",
        "🌃💫 Sao lung linh, chân kéo đây, ngủ ngon nào!",
        "🌙🌬️ Khuya yên bình, giấc mơ đây, nghỉ ngơi nhé!",
        "🌌❄️ Đêm sâu thẩm, lòng nhẹ bay, mơ đẹp thôi!",
        "🌠✨ Trăng lặng lẽ, giấc mơ đây, ngủ thật sâu!",
        "🌜🌌 4 giờ rồi, đừng thức nữa, nghỉ ngơi nha!",
        "✨💤 Đêm lạnh lắm, chân ấm đây, ngủ ngon nhé!",
        "🌙🌠 Gió khuya ru, giấc mơ bay, nghỉ thôi nào!",
        "🌌❄️ Khuya tĩnh lặng, mắt nhắm đây, mơ đẹp nha!",
        "🌃✨ Đêm sâu lắng, lòng nhẹ đây, ngủ thật sâu!"
    ],
    "05:30": [
        "🌅☀️ Bình minh gần, giấc mơ đây, dậy thôi nào!",
        "☀️✨ Sáng nhẹ nhàng, năng lượng bay, chào ngày nhé!",
        "🌞💫 5 rưỡi sáng, lòng hăng say, khởi đầu thôi!",
        "🌻🌸 Nắng ban mai, giấc mơ đây, dậy thật nhanh!",
        "✨🌅 Sáng tươi mới, tinh thần bay, chào buổi sáng!",
        "☀️🌬️ Gió mát lạnh, năng lượng đây, bắt đầu nào!",
        "🌞🌈 Bình minh rạng, giấc mơ bay, dậy đi thôi!",
        "🌅💤 Sáng lung linh, lòng nhẹ đây, chào ngày nhé!",
        "☀️🌻 Nắng dịu dàng, tinh thần bay, khởi đầu thôi!",
        "✨🌞 5 giờ hơn, ngày mới đây, dậy thật nhanh!",
        "🌅🌸 Sáng rực rỡ, giấc mơ đây, chào buổi sáng!",
        "☀️🌬️ Nắng ban mai, lòng hăng say, bắt đầu nào!",
        "🌞💫 Sáng tươi đẹp, năng lượng bay, dậy đi nhé!",
        "🌻✨ Gió mát sáng, giấc mơ đây, chào ngày thôi!"
    ],
    "07:00": [
        "🌞☀️ Sáng rực rỡ, ngày mới đây, dậy thôi nào!",
        "☀️✨ 7 giờ sáng, nắng lung linh, chào buổi sáng!",
        "🌅💫 Một ngày mới, lòng hăng say, bắt đầu thôi!",
        "🌻🌸 Nắng ban mai, giấc mơ đây, dậy thật nhanh!",
        "✨🌞 Sáng tươi đẹp, năng lượng bay, chào ngày mới!",
        "☀️🌬️ Gió mát lạnh, tinh thần đây, khởi đầu nào!",
        "🌞🌈 Bình minh rạng, giấc mơ bay, dậy đi thôi!",
        "🌅💤 Sáng lung linh, lòng nhẹ đây, chào ngày nhé!",
        "☀️🌻 Nắng dịu dàng, tinh thần bay, bắt đầu thôi!",
        "✨🌞 7 giờ rồi, ngày mới đây, dậy thật nhanh!",
        "🌅🌸 Sáng rực rỡ, giấc mơ đây, chào buổi sáng!",
        "☀️🌬️ Nắng ban mai, lòng hăng say, bắt đầu nào!",
        "🌞💫 Sáng tươi đẹp, năng lượng bay, dậy đi nhé!",
        "🌻✨ Gió mát sáng, giấc mơ đây, chào ngày thôi!"
    ],
    "08:30": [
        "🌞☕ Sáng hiệu quả, công việc đây, cố lên nào!",
        "☕✨ 8 rưỡi sáng, tinh thần bay, làm việc thôi!",
        "🌻💫 Nắng ban mai, năng lượng đây, bắt đầu nhé!",
        "✨🌞 Sáng rực rỡ, lòng hăng say, làm thật tốt!",
        "☀️🌬️ Gió mát lạnh, giấc mơ bay, hiệu quả nào!",
        "🌅🌸 Nắng dịu dàng, tinh thần đây, làm việc thôi!",
        "🌞🌈 8 giờ hơn, công việc đây, cố lên nhé!",
        "☕💤 Sáng tươi mới, lòng nhẹ bay, làm thật nhanh!",
        "✨🌻 Nắng lung linh, năng lượng đây, hiệu quả thôi!",
        "☀️🌞 Sáng yên bình, giấc mơ đây, làm việc nào!",
        "🌅💫 Gió mát sáng, tinh thần bay, cố lên thôi!",
        "🌞🌸 Nắng ban mai, lòng hăng say, làm thật tốt!",
        "☕✨ Sáng rực rỡ, công việc đây, hiệu quả nào!"
    ],
    "10:06": [
        "🌞⏰ 10 giờ sáng, năng lượng đây, làm việc nào!",
        "☀️✨ Nắng rực rỡ, tinh thần bay, cố lên nhé!",
        "🌻💫 Sáng tươi mới, giấc mơ đây, hiệu quả thôi!",
        "✨🌞 Gió mát lạnh, lòng hăng say, làm thật tốt!",
        "☕🌸 Nắng dịu dàng, công việc đây, bắt đầu nào!",
        "🌅🌈 10 giờ rồi, tinh thần bay, làm việc thôi!",
        "🌞💤 Sáng lung linh, năng lượng đây, cố lên nhé!",
        "☀️🌻 Nắng ban mai, giấc mơ bay, hiệu quả nào!",
        "✨⏰ Sáng yên bình, lòng nhẹ đây, làm thật nhanh!",
        "🌞🌸 Gió mát sáng, tinh thần đây, làm việc thôi!",
        "☕💫 Nắng rực rỡ, công việc bay, cố lên nào!",
        "🌅✨ Sáng tươi đẹp, năng lượng đây, hiệu quả thôi!"
    ],
    "11:30": [
        "🌞🍽️ Gần trưa rồi, nghỉ ngơi đây, ăn ngon nhé!",
        "☀️✨ 11 rưỡi sáng, giấc mơ bay, nghỉ thôi nào!",
        "🌻💤 Nắng ban trưa, lòng nhẹ đây, thư giãn thôi!",
        "✨⏰ Trưa yên bình, năng lượng đây, ăn thật ngon!",
        "☕🌸 Gió mát lạnh, tinh thần bay, nghỉ ngơi nào!",
        "🌅🌈 Nắng dịu dàng, giấc mơ đây, ăn ngon nhé!",
        "🌞💫 11 giờ hơn, bụng đói đây, nghỉ thôi nào!",
        "☀️🌻 Trưa rực rỡ, món ngon bay, thư giãn thôi!",
        "✨🍽️ Nắng ban trưa, lòng hăng say, ăn thật ngon!",
        "🌞🌸 Gió mát trưa, giấc mơ đây, nghỉ ngơi nào!"
    ],
    "13:00": [
        "🌞⏰ 1 giờ chiều, năng lượng đây, làm việc nào!",
        "☀️✨ Nắng rực rỡ, tinh thần bay, cố lên nhé!",
        "🌻💫 Chiều tươi mới, giấc mơ đây, hiệu quả thôi!",
        "✨🌞 Gió mát lạnh, lòng hăng say, làm thật tốt!",
        "☕🌸 Nắng dịu dàng, công việc đây, bắt đầu nào!",
        "🌅🌈 1 giờ rồi, tinh thần bay, làm việc thôi!",
        "🌞💤 Chiều lung linh, năng lượng đây, cố lên nhé!",
        "☀️🌻 Nắng ban chiều, giấc mơ bay, hiệu quả nào!",
        "✨⏰ Chiều yên bình, lòng nhẹ đây, làm thật nhanh!"
    ],
    "14:30": [
        "🌞🌻 Chiều lãng mạn, giấc mơ đây, vui vẻ nào!",
        "☀️✨ 2 rưỡi chiều, tinh thần bay, làm việc nhé!",
        "🌅💫 Nắng dịu dàng, năng lượng đây, cố lên thôi!",
        "✨⏰ Chiều rực rỡ, lòng hăng say, hiệu quả nào!",
        "☕🌸 Gió mát lạnh, giấc mơ bay, làm thật tốt!",
        "🌞🌈 Nắng ban chiều, tinh thần đây, bắt đầu nào!",
        "🌻💤 Chiều yên bình, công việc bay, cố lên nhé!"
    ],
    "16:00": [
        "🌅✨ Chiều dần tới, giấc mơ đây, thư giãn nào!",
        "☀️🌻 4 giờ chiều, tinh thần bay, nghỉ ngơi nhé!",
        "🌞💫 Nắng nhạt dần, năng lượng đây, làm việc thôi!",
        "✨⏰ Chiều yên bình, lòng hăng say, hiệu quả nào!",
        "☕🌸 Gió mát chiều, giấc mơ bay, cố lên nhé!",
        "🌅🌈 Nắng dịu dàng, tinh thần đây, làm thật tốt!"
    ],
    "17:30": [
        "🌅🌞 Hoàng hôn gần, giấc mơ đây, nghỉ ngơi nào!",
        "☀️✨ 5 rưỡi chiều, tinh thần bay, thư giãn nhé!",
        "🌻💤 Nắng nhạt dần, lòng nhẹ đây, nghỉ thôi nào!",
        "✨⏰ Chiều tà đến, năng lượng bay, thư giãn thôi!",
        "☕🌸 Gió mát lạnh, giấc mơ đây, nghỉ ngơi nhé!"
    ],
    "19:00": [
        "🌙✨ Tối dịu dàng, giấc mơ đây, ăn ngon nào!",
        "🌌💤 7 giờ tối, tinh thần bay, nghỉ ngơi nhé!",
        "🌜❄️ Đêm yên bình, món ngon đây, thư giãn thôi!",
        "✨🍽️ Tối rực rỡ, lòng hăng say, ăn thật ngon!",
        "☕🌙 Gió mát đêm, giấc mơ bay, nghỉ ngơi nào!"
    ],
    "20:30": [
        "🌙✨ Sắp ngủ rồi, giấc mơ đây, ngủ ngon nào!",
        "🌌💤 8 rưỡi tối, chân kéo bay, nghỉ thôi nhé!",
        "🌜❄️ Đêm yên tĩnh, lòng nhẹ đây, mơ đẹp thôi!",
        "✨⏰ Tối dịu dàng, tinh thần bay, ngủ thật sâu!",
        "☕🌙 Gió mát đêm, giấc mơ đây, nghỉ ngơi nào!"
    ],
    "22:06": [
        "🌙🌌 Đêm khuya đến, giấc mơ đây, ngủ ngon nào!",
        "🌃✨ 10 giờ tối, chân ấm bay, nghỉ thôi nhé!",
        "🌜💤 Gió lạnh ru, lòng nhẹ đây, mơ đẹp thôi!",
        "✨⏰ Đêm yên bình, tinh thần bay, ngủ thật sâu!",
        "☕🌙 Trăng lặng lẽ, giấc mơ đây, nghỉ ngơi nào!"
    ],
    "23:30": [
        "🌙✨ Khuya lắm rồi, giấc mơ đây, ngủ ngon nào!",
        "🌌💤 11 rưỡi tối, chân kéo bay, nghỉ thôi nhé!",
        "🌜❄️ Đêm tĩnh lặng, lòng nhẹ đây, mơ đẹp thôi!",
        "✨⏰ Gió khuya ru, tinh thần bay, ngủ thật sâu!",
        "☕🌙 Trăng mờ ảo, giấc mơ đây, nghỉ ngơi nào!"
    ],
    "00:00": [
        "🌙🌌 Nửa đêm rồi, giấc mơ đây, ngủ ngon nào!",
        "🌃✨ 12 giờ khuya, chân ấm bay, nghỉ thôi nhé!",
        "🌜💤 Gió lạnh ru, lòng nhẹ đây, mơ đẹp thôi!",
        "✨⏰ Đêm sâu thẩm, tinh thần bay, ngủ thật sâu!",
        "☕🌙 Trăng lặng lẽ, giấc mơ đây, nghỉ ngơi nào!"
    ]
}

vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')

def handle_autosend_on(bot, thread_id, author_id):
    """Bật tính năng autosend cho thread"""
    settings = read_settings(bot.uid)
    if "autosend" not in settings:
        settings["autosend"] = {}
    settings["autosend"][thread_id] = True
    write_settings(bot.uid, settings)
    return f"🚦 Lệnh autosend đã được Bật 🚀 trong nhóm này ✅"

def handle_autosend_off(bot, thread_id, author_id):
    """Tắt tính năng autosend cho thread"""
    settings = read_settings(bot.uid)
    if "autosend" in settings and thread_id in settings["autosend"]:
        settings["autosend"][thread_id] = False
        write_settings(bot.uid, settings)
        return f"🚦 Lệnh autosend đã Tắt ⭕️ trong nhóm này ✅"
    return "🚦 Nhóm chưa có thông tin cấu hình autosend để ⭕️ Tắt 🤗"

def get_autosend_status(bot, thread_id):
    """Lấy trạng thái autosend của thread"""
    settings = read_settings(bot.uid)
    return settings.get("autosend", {}).get(thread_id, False)

def list_autosend_groups(bot):
    """Liệt kê các nhóm đã bật autosend"""
    settings = read_settings(bot.uid)
    autosend_groups = settings.get("autosend", {})
    
    active_groups = []
    for thread_id, status in autosend_groups.items():
        if status:
            try:
                group_info = bot.fetchGroupInfo(thread_id)
                group_name = group_info.gridInfoMap.get(thread_id, {}).get('name', f'Group_{thread_id}')
                active_groups.append(f"📌 {group_name} - ID: {thread_id}")
            except:
                active_groups.append(f"📌 Unknown Group - ID: {thread_id}")
    
    if active_groups:
        return f"🚦 Danh sách nhóm đã bật autosend:\n" + "\n".join(active_groups)
    else:
        return "🚦 Không có nhóm nào đã bật autosend"

def autosend_task(client):
    """Task chạy autosend trong background"""
    last_sent_time = {}
    
    while True:
        try:
            settings = read_settings(client.uid)
            autosend_groups = settings.get("autosend", {})
            
            if not autosend_groups:
                time.sleep(30)
                continue
                
            now = datetime.now(vn_tz)
            current_time_str = now.strftime("%H:%M")
            
            # Kiểm tra nếu thời gian hiện tại có trong danh sách
            if current_time_str in time_poems:
                # Lấy danh sách video từ URL
                listvd = "https://raw.githubusercontent.com/trannguyen-shiniuem/trannguyen-shiniuem/main/autosend1.json"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                }
                
                try:
                    response = requests.get(listvd, headers=headers, timeout=10)
                    response.raise_for_status()
                    urls = response.json()
                    if not urls:
                        raise ValueError("Danh sách video rỗng")
                    video_url = random.choice(urls)
                except Exception as e:
                    print(f"❌ Lỗi khi lấy danh sách video: {e}")
                    time.sleep(30)
                    continue
                
                # Kiểm tra video URL có hợp lệ không
                try:
                    video_check = requests.head(video_url, headers=headers, timeout=5)
                    if video_check.status_code != 200:
                        raise ValueError(f"Video URL không hợp lệ: {video_url}")
                except Exception as e:
                    print(f"❌ Video URL không khả dụng: {e}")
                    time.sleep(30)
                    continue
                
                # Chuẩn bị nội dung gửi
                thumbnail_url = "https://f66-zpg-r.zdn.vn/jxl/8107149848477004187/d08a4d364d8cf9d2a09d.jxl"
                duration = 1000000
                poem = random.choice(time_poems[current_time_str])
                formatted_message = f"🚦 {poem}\n🚦 {current_time_str} - Bot: {get_user_name_by_id(client, client.uid)} Autosend"
                
                # Gửi tin nhắn đến các nhóm đã bật autosend
                for thread_id, enabled in autosend_groups.items():
                    if not enabled:
                        continue
                        
                    # Kiểm tra thời gian gửi cuối để tránh spam
                    if thread_id not in last_sent_time or (now - last_sent_time.get(thread_id, now - timedelta(minutes=2)) >= timedelta(minutes=1)):
                        gui = Message(text=formatted_message)
                        try:
                            client.sendRemoteVideo(
                                video_url,
                                thumbnail_url,
                                duration=duration,
                                message=gui,
                                thread_id=thread_id,
                                thread_type=ThreadType.GROUP,
                                width=1080,
                                height=1920,
                                ttl=3600000
                            )
                            last_sent_time[thread_id] = now
                            print(f"✅ Đã gửi tin nhắn đến {thread_id}")
                            time.sleep(0.3)  # Delay để tránh spam API
                        except Exception as e:
                            print(f"❌ Lỗi khi gửi tin nhắn đến {thread_id}: {e}")
                            
        except Exception as e:
            print(f"❌ Lỗi trong autosend_task: {e}")
            
        time.sleep(30)  # Kiểm tra mỗi 30 giây

def start_autosend_handle(client, thread_type, message_object, message, thread_id, prefix, author_id):
    """Xử lý lệnh autosend"""
    from core.bot_sys import is_admin
    
    # Kiểm tra quyền admin
    if not is_admin(client, author_id):
        client.replyMessage(
            Message(text="❌ Bạn không có quyền sử dụng lệnh này!"), 
            message_object, 
            thread_id=thread_id, 
            thread_type=thread_type
        )
        return
    
    # Parse lệnh
    parts = message.strip().split()
    if len(parts) < 2:
        response = (
            f"🚦 Hướng dẫn sử dụng autosend:\n"
            f"➜ {prefix}autosend on - Bật autosend\n"
            f"➜ {prefix}autosend off - Tắt autosend\n"
            f"➜ {prefix}autosend status - Xem trạng thái\n"
            f"➜ {prefix}autosend list - Danh sách nhóm đã bật"
        )
        client.replyMessage(Message(text=response), message_object, thread_id=thread_id, thread_type=thread_type)
        return
    
    action = parts[1].lower()
    
    if action == "on":
        response = handle_autosend_on(client, thread_id, author_id)
        client.replyMessage(Message(text=response), message_object, thread_id=thread_id, thread_type=thread_type)
        
        # Khởi động autosend thread nếu chưa có
        if not hasattr(client, 'autosend_thread') or not client.autosend_thread.is_alive():
            client.autosend_thread = threading.Thread(target=autosend_task, args=(client,), daemon=True)
            client.autosend_thread.start()
            print("✅ Autosend thread đã được khởi động!")
            
    elif action == "off":
        response = handle_autosend_off(client, thread_id, author_id)
        client.replyMessage(Message(text=response), message_object, thread_id=thread_id, thread_type=thread_type)
        
    elif action == "status":
        status = get_autosend_status(client, thread_id)
        status_text = "🟢 Đang bật" if status else "🔴 Đang tắt"
        
        try:
            group_info = client.fetchGroupInfo(thread_id)
            group_name = group_info.gridInfoMap.get(thread_id, {}).get('name', 'Unknown Group')
        except:
            group_name = 'Unknown Group'
            
        response = f"🚦 Trạng thái autosend:\n📌 Nhóm: {group_name}\n🔧 Trạng thái: {status_text}"
        client.replyMessage(Message(text=response), message_object, thread_id=thread_id, thread_type=thread_type)
        
    elif action == "list":
        response = list_autosend_groups(client)
        client.replyMessage(Message(text=response), message_object, thread_id=thread_id, thread_type=thread_type)
        
    else:
        response = f"❌ Lệnh không hợp lệ! Sử dụng: {prefix}autosend [on/off/status/list]"
        client.replyMessage(Message(text=response), message_object, thread_id=thread_id, thread_type=thread_type)

def start_autosend_thread(client):
    """Khởi động autosend thread khi bot khởi động"""
    if not hasattr(client, 'autosend_thread') or not client.autosend_thread.is_alive():
        client.autosend_thread = threading.Thread(target=autosend_task, args=(client,), daemon=True)
        client.autosend_thread.start()
        print("✅ Autosend thread đã được khởi động khi bot start!")