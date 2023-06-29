from pynput import keyboard

def on_press(key):
    try:
        print('按键 {0} 被按下了。'.format(key.char))
    except AttributeError:
        print('特殊按键 {0} 被按下了。'.format(key))

def on_release(key):
    print('按键 {0} 被释放了。'.format(key))
    if key == keyboard.Key.esc:
        # 如果按下了ESC键，停止监听
        return False

# 创建监听器对象
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

# 启动监听器
listener.start()

# 保持监听，直到按下ESC键停止
listener.join()