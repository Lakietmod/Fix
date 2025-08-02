from datetime import datetime, timedelta
import random
import threading
import time
from zlapi.models import *
import pytz
import requests
import json

# Dữ liệu thơ theo thời gian
time_poems = {
    "01:00": [
        "🌙✨ Đem khuya vang, giac mo đay, ngu ngon nhe!",
        "🌌💤 Gio lanh ru, long nhe bay, nghi thoi nao!",
        "🌃❄️ 1 gio sang, chan am đay, mo đep nha!",
        "🌜🌠 Trang mo ao, giac mo bay, ngu that sau!",
        "✨🌙 Đem sau lang, mat nham ngay, nghi ngoi nao!",
        "🌌💫 Sao lung linh, đem yen đay, ngu ngon thoi!",
        "🌃🌬️ Khuya tinh lang, giac mo đay, nghi ngoi nhe!",
        "🌙❄️ Đem lanh lam, chan keo đay, mo đep nao!",
        "🌠✨ Trang diu dang, long nhe bay, ngu that sau!",
        "🌜🌌 1 gio roi, đung thuc nua, nghi thoi nha!",
        "✨💤 Đem yen binh, giac mo đay, ngu ngon nhe!",
        "🌙🌠 Gio khuya lanh, mat nham đay, nghi ngoi thoi!",
        "🌌❄️ Đem sau tham, chan am bay, mo đep nha!",
        "🌃✨ Khuya vang ve, long nhe đay, ngu that sau!",
        "🌜💫 Trang lang le, giac mo đay, nghi ngoi nao!"
    ],
    "02:30": [
        "🌙🌌 Khuya lanh lam, giac mo đay, ngu ngon nhe!",
        "🌃✨ Đem sau lang, chan keo ngay, nghi thoi nao!",
        "🌜💤 Gio khuya ru, long nhe bay, mo đep nha!",
        "🌠❄️ 2 ruoi sang, mat nham đay, ngu that sau!",
        "✨🌙 Đem tinh lang, giac mo bay, nghi ngoi thoi!",
        "🌌💫 Sao lap lanh, chan am đay, ngu ngon nao!",
        "🌃🌬️ Khuya yen binh, giac mo đay, nghi ngoi nhe!",
        "🌙❄️ Đem sau tham, long nhe bay, mo đep thoi!",
        "🌠✨ Trang mo ao, giac mo đay, ngu that sau!",
        "🌜🌌 2 gio hon, đung thuc nua, nghi ngoi nha!",
        "✨💤 Đem lanh lam, chan keo đay, ngu ngon nhe!",
        "🌙🌠 Gio hat ru, giac mo bay, nghi thoi nao!",
        "🌌❄️ Khuya tinh lang, mat nham đay, mo đep nha!",
        "🌃✨ Đem sau lang, long nhe đay, ngu that sau!"
    ],
    "04:00": [
        "🌃🌙 Đem khuya lanh, giac mo đay, ngu ngon nhe!",
        "🌜✨ 4 gio sang, chan am bay, nghi thoi nao!",
        "🌌💤 Gio lanh ru, long nhe đay, mo đep nha!",
        "🌠❄️ Đem tinh lang, mat nham ngay, ngu that sau!",
        "✨🌙 Trang mo ao, giac mo bay, nghi ngoi thoi!",
        "🌃💫 Sao lung linh, chan keo đay, ngu ngon nao!",
        "🌙🌬️ Khuya yen binh, giac mo đay, nghi ngoi nhe!",
        "🌌❄️ Đem sau tham, long nhe bay, mo đep thoi!",
        "🌠✨ Trang lang le, giac mo đay, ngu that sau!",
        "🌜🌌 4 gio roi, đung thuc nua, nghi ngoi nha!",
        "✨💤 Đem lanh lam, chan am đay, ngu ngon nhe!",
        "🌙🌠 Gio khuya ru, giac mo bay, nghi thoi nao!",
        "🌌❄️ Khuya tinh lang, mat nham đay, mo đep nha!",
        "🌃✨ Đem sau lang, long nhe đay, ngu that sau!"
    ],
    "05:30": [
        "🌅☀️ Binh minh gan, giac mo đay, day thoi nao!",
        "☀️✨ Sang nhe nhang, nang luong bay, chao ngay nhe!",
        "🌞💫 5 ruoi sang, long hang say, khoi đau thoi!",
        "🌻❀ Nang ban mai, giac mo đay, day that nhanh!",
        "✨🌅 Sang tuoi moi, tinh than bay, chao buoi sang!",
        "☀️🌬️ Gio mat lanh, nang luong đay, bat đau nao!",
        "🌞🌈 Binh minh rang, giac mo bay, day đi thoi!",
        "🌅💤 Sang lung linh, long nhe đay, chao ngay nhe!",
        "☀️🌻 Nang diu dang, tinh than bay, khoi đau thoi!",
        "✨🌞 5 gio hon, ngay moi đay, day that nhanh!",
        "🌅❀ Sang ruc ro, giac mo đay, chao buoi sang!",
        "☀️🌬️ Nang ban mai, long hang say, bat đau nao!",
        "🌞💫 Sang tuoi đep, nang luong bay, day đi nhe!",
        "🌻✨ Gio mat sang, giac mo đay, chao ngay thoi!"
    ],
    "07:00": [
        "🌞☀️ Sang ruc ro, ngay moi đay, day thoi nao!",
        "☀️✨ 7 gio sang, nang lung lay, chao buoi sang!",
        "🌅💫 Mot ngay moi, long hang say, bat đau thoi!",
        "🌻❀ Nang ban mai, giac mo đay, day that nhanh!",
        "✨🌞 Sang tuoi đep, nang luong bay, chao ngay moi!",
        "☀️🌬️ Gio mat lanh, tinh than đay, khoi đau nao!",
        "🌞🌈 Binh minh rang, giac mo bay, day đi thoi!",
        "🌅💤 Sang lung linh, long nhe đay, chao ngay nhe!",
        "☀️🌻 Nang diu dang, tinh than bay, bat đau thoi!",
        "✨🌞 7 gio roi, ngay moi đay, day that nhanh!",
        "🌅❀ Sang ruc ro, giac mo đay, chao buoi sang!",
        "☀️🌬️ Nang ban mai, long hang say, bat đau nao!",
        "🌞💫 Sang tuoi đep, nang luong bay, day đi nhe!",
        "🌻✨ Gio mat sang, giac mo đay, chao ngay thoi!"
    ],
    "08:30": [
        "🌞☕ Sang hieu qua, cong viec đay, co len nao!",
        "☕✨ 8 ruoi sang, tinh than bay, lam viec thoi!",
        "🌻💫 Nang ban mai, nang luong đay, bat đau nhe!",
        "✨🌞 Sang ruc ro, long hang say, lam that tot!",
        "☀️🌬️ Gio mat lanh, giac mo bay, hieu qua nao!",
        "🌅❀ Nang diu dang, tinh than đay, lam viec thoi!",
        "🌞🌈 8 gio hon, cong viec đay, co len nhe!",
        "☕💤 Sang tuoi moi, long nhe bay, lam that nhanh!",
        "✨🌻 Nang lung linh, nang luong đay, hieu qua thoi!",
        "☀️🌞 Sang yen binh, giac mo đay, lam viec nao!",
        "🌅💫 Gio mat sang, tinh than bay, co len thoi!",
        "🌞❀ Nang ban mai, long hang say, lam that tot!",
        "☕✨ Sang ruc ro, cong viec đay, hieu qua nao!"
    ],
    "10:06": [
        "🌞⏰ 10 gio sang, nang luong đay, lam viec nao!",
        "☀️✨ Nang ruc ro, tinh than bay, co len nhe!",
        "🌻💫 Sang tuoi moi, giac mo đay, hieu qua thoi!",
        "✨🌞 Gio mat lanh, long hang say, lam that tot!",
        "☕❀ Nang diu dang, cong viec đay, bat đau nao!",
        "🌅🌈 10 gio roi, tinh than bay, lam viec thoi!",
        "🌞💤 Sang lung linh, nang luong đay, co len nhe!",
        "☀️🌻 Nang ban mai, giac mo bay, hieu qua nao!",
        "✨⏰ Sang yen binh, long nhe đay, lam that nhanh!",
        "🌞❀ Gio mat sang, tinh than đay, lam viec thoi!",
        "☕💫 Nang ruc ro, cong viec bay, co len nao!",
        "🌅✨ Sang tuoi đep, nang luong đay, hieu qua thoi!"
    ],
    "11:30": [
        "🌞🍽️ Gan trua roi, nghi ngoi đay, an ngon nhe!",
        "☀️✨ 11 ruoi sang, giac mo bay, nghi thoi nao!",
        "🌻💤 Nang ban trua, long nhe đay, thu gian thoi!",
        "✨⏰ Trua yen binh, nang luong đay, an that ngon!",
        "☕❀ Gio mat lanh, tinh than bay, nghi ngoi nao!",
        "🌅🌈 Nang diu dang, giac mo đay, an ngon nhe!",
        "🌞💫 11 gio hon, bung đoi đay, nghi thoi nao!",
        "☀️🌻 Trua ruc ro, mon ngon bay, thu gian thoi!",
        "✨🍽️ Nang ban trua, long hang say, an that ngon!",
        "🌞❀ Gio mat trua, giac mo đay, nghi ngoi nao!"
    ],
    "13:00": [
        "🌞⏰ 1 gio chieu, nang luong đay, lam viec nao!",
        "☀️✨ Nang ruc ro, tinh than bay, co len nhe!",
        "🌻💫 Chieu tuoi moi, giac mo đay, hieu qua thoi!",
        "✨🌞 Gio mat lanh, long hang say, lam that tot!",
        "☕❀ Nang diu dang, cong viec đay, bat đau nao!",
        "🌅🌈 1 gio roi, tinh than bay, lam viec thoi!",
        "🌞💤 Chieu lung linh, nang luong đay, co len nhe!",
        "☀️🌻 Nang ban chieu, giac mo bay, hieu qua nao!",
        "✨⏰ Chieu yen binh, long nhe đay, lam that nhanh!"
    ],
    "14:30": [
        "🌞🌻 Chieu lang man, giac mo đay, vui ve nao!",
        "☀️✨ 2 ruoi chieu, tinh than bay, lam viec nhe!",
        "🌅💫 Nang diu dang, nang luong đay, co len thoi!",
        "✨⏰ Chieu ruc ro, long hang say, hieu qua nao!",
        "☕❀ Gio mat lanh, giac mo bay, lam that tot!",
        "🌞🌈 Nang ban chieu, tinh than đay, bat đau nao!",
        "🌻💤 Chieu yen binh, cong viec bay, co len nhe!"
    ],
    "16:00": [
        "🌅✨ Chieu dan troi, giac mo đay, thu gian nao!",
        "☀️🌻 4 gio chieu, tinh than bay, nghi ngoi nhe!",
        "🌞💫 Nang nhat dan, nang luong đay, lam viec thoi!",
        "✨⏰ Chieu yen binh, long hang say, hieu qua nao!",
        "☕❀ Gio mat chieu, giac mo bay, co len nhe!",
        "🌅🌈 Nang diu dang, tinh than đay, lam that tot!"
    ],
    "17:30": [
        "🌅🌞 Hoang hon gan, giac mo đay, nghi ngoi nao!",
        "☀️✨ 5 ruoi chieu, tinh than bay, thu gian nhe!",
        "🌻💤 Nang nhat dan, long nhe đay, nghi thoi nao!",
        "✨⏰ Chieu ta đen, nang luong bay, thu gian thoi!",
        "☕❀ Gio mat lanh, giac mo đay, nghi ngoi nhe!"
    ],
    "19:00": [
        "🌙✨ Toi diu dang, giac mo đay, an ngon nao!",
        "🌌💤 7 gio toi, tinh than bay, nghi ngoi nhe!",
        "🌜❄️ Đem yen binh, mon ngon đay, thu gian thoi!",
        "✨🍽️ Toi ruc ro, long hang say, an that ngon!",
        "☕🌙 Gio mat đem, giac mo bay, nghi ngoi nao!"
    ],
    "20:30": [
        "🌙✨ Sap ngu roi, giac mo đay, ngu ngon nao!",
        "🌌💤 8 ruoi toi, chan keo bay, nghi thoi nhe!",
        "🌜❄️ Đem yen tinh, long nhe đay, mo đep thoi!",
        "✨⏰ Toi diu dang, tinh than bay, ngu that sau!",
        "☕🌙 Gio mat đem, giac mo đay, nghi ngoi nao!"
    ],
    "22:06": [
        "🌙🌌 Đem khuya đen, giac mo đay, ngu ngon nao!",
        "🌃✨ 10 gio toi, chan am bay, nghi thoi nhe!",
        "🌜💤 Gio lanh ru, long nhe đay, mo đep thoi!",
        "✨⏰ Đem yen binh, tinh than bay, ngu that sau!",
        "☕🌙 Trang lang le, giac mo đay, nghi ngoi nao!"
    ],
    "23:30": [
        "🌙✨ Khuya lam roi, giac mo đay, ngu ngon nao!",
        "🌌💤 11 ruoi toi, chan keo bay, nghi thoi nhe!",
        "🌜❄️ Đem tinh lang, long nhe đay, mo đep thoi!",
        "✨⏰ Gio khuya ru, tinh than bay, ngu that sau!",
        "☕🌙 Trang mo ao, giac mo đay, nghi ngoi nao!"
    ],
    "00:00": [
        "🌙🌌 Nua đem roi, giac mo đay, ngu ngon nao!",
        "🌃✨ 12 gio khuya, chan am bay, nghi thoi nhe!",
        "🌜💤 Gio lanh ru, long nhe đay, mo đep thoi!",
        "✨⏰ Đem sau tham, tinh than bay, ngu that sau!",
        "☕🌙 Trang lang le, giac mo đay, nghi ngoi nao!"
    ]
}

# Timezone Việt Nam
vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')

def start_autosend_thread(bot):
    """Khởi động thread autosend"""
    global autosend_thread, autosend_running
    
    if autosend_running:
        return
    
    autosend_running = True
    autosend_thread = threading.Thread(target=autosend_task, args=(bot,), daemon=True)
    autosend_thread.start()
    print("✅ Autosend thread đã được khởi động!")

def autosend_task(bot):
    """Task chính để gửi tin nhắn autosend"""
    last_sent_time = {}
    
    while autosend_running:
        try:
            # Đọc settings từ bot
            from core.bot_sys import read_settings
            settings = read_settings(bot.uid)
            
            # Kiểm tra xem có nhóm nào bật autosend không
            autosend_settings = settings.get("autosend", {})
            if not any(autosend_settings.values()):
                time.sleep(60)  # Chờ 1 phút nếu không có nhóm nào bật
                continue
            
            # Lấy thời gian hiện tại
            now = datetime.now(vn_tz)
            current_time_str = now.strftime("%H:%M")
            
            # Kiểm tra xem có thơ cho thời gian này không
            if current_time_str in time_poems:
                # Lấy video ngẫu nhiên
                video_url = get_random_video()
                if not video_url:
                    time.sleep(30)
                    continue
                
                # Cấu hình video
                thumbnail_url = "https://f66-zpg-r.zdn.vn/jxl/8107149848477004187/d08a4d364d8cf9d2a09d.jxl"
                duration = '1000000'
                
                # Chọn thơ ngẫu nhiên
                poem = random.choice(time_poems[current_time_str])
                
                # Format tin nhắn
                from core.bot_sys import get_user_name_by_id
                bot_name = get_user_name_by_id(bot, bot.uid)
                formatted_message = f"🚦 {poem}\n🚦 {current_time_str} - Bot: {bot_name} Autosend"
                
                # Gửi đến các nhóm đã bật autosend
                for thread_id, enabled in autosend_settings.items():
                    if not enabled:
                        continue
                    
                    # Kiểm tra thời gian gửi cuối (tránh spam)
                    if thread_id in last_sent_time:
                        time_diff = now - last_sent_time[thread_id]
                        if time_diff < timedelta(minutes=30):  # Tối thiểu 30 phút giữa các lần gửi
                            continue
                    
                    try:
                        # Tạo tin nhắn
                        gui = Message(text=formatted_message)
                        
                        # Gửi video
                        bot.sendRemoteVideo(
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
                        print(f"✅ Đã gửi autosend đến nhóm {thread_id} lúc {current_time_str}")
                        
                        # Delay giữa các nhóm
                        time.sleep(2)
                        
                    except Exception as e:
                        print(f"❌ Lỗi khi gửi autosend đến nhóm {thread_id}: {e}")
                        
        except Exception as e:
            print(f"❌ Lỗi trong autosend_task: {e}")
        
        # Chờ 30 giây trước khi kiểm tra lại
        time.sleep(30)

def get_random_video():
    """Lấy video ngẫu nhiên từ danh sách"""
    try:
        # URL danh sách video
        listvd = "https://raw.githubusercontent.com/trannguyen-shiniuem/trannguyen-shiniuem/main/autosend1.json"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        
        # Tải danh sách video
        response = requests.get(listvd, headers=headers, timeout=10)
        response.raise_for_status()
        urls = response.json()
        
        if not urls:
            raise ValueError("Danh sách video rỗng")
        
        # Chọn video ngẫu nhiên
        video_url = random.choice(urls)
        
        # Kiểm tra video có khả dụng không
        video_check = requests.head(video_url, headers=headers, timeout=5)
        if video_check.status_code != 200:
            raise ValueError(f"Video URL không hợp lệ: {video_url}")
        
        return video_url
        
    except Exception as e:
        print(f"❌ Lỗi khi lấy video: {e}")
        return None

def stop_autosend():
    """Dừng autosend thread"""
    global autosend_running
    autosend_running = False
    print("🛑 Autosend thread đã được dừng!")
