import random
import sys

# پشتیبانی از کاراکترهای فارسی و ایموجی در کنسول ویندوز
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------- محیط 2*2 ----------------
# True  = روشن (ON)
# False = خاموش (OFF)

def create_environment(initial_state=None):
    if initial_state is None:
        initial_state = [[random.choice([True, False]) for _ in range(2)]
                          for _ in range(2)]
    return [row[:] for row in initial_state]


def show_environment(env, agent_pos, step):
    print(f"\n--- گام {step} | موقعیت عامل: {agent_pos} ---")
    for r in range(2):
        row = []
        for c in range(2):
            light = "💡" if env[r][c] else "  "
            if (r, c) == agent_pos:
                light = "🤖" + ("💡" if env[r][c] else "")
            row.append(f"[{light}]")
        print(" ".join(row))


def all_lights_off(env):
    return all(not cell for row in env for cell in row)


# ------------- عامل واکنشی ساده -------------
class SimpleReflexAgent:
    """
    قواعد واکنشی (if-then) صرفاً بر اساس احساس فعلی:
      - percept == 'ON'  -> TURN_OFF (خاموش کن، حرکت نکن)
      - percept == 'OFF' -> MOVE     (به خانه بعدی برو)
    جهت پیمایش ثابت: چپ به راست، سپس ردیف بعد.
    """

    def __init__(self):
        self.position = (0, 0)          # شروع از گوشه بالا-چپ
        self.visited_order = [(0, 0), (0, 1), (1, 0), (1, 1)]

    def perceive(self, env):
        r, c = self.position
        return 'ON' if env[r][c] else 'OFF'

    def decide(self, percept):
        if percept == 'ON':             # قاعده ۱
            return 'TURN_OFF'
        else:                           # قاعده ۲
            return 'MOVE'

    def act(self, action, env):
        r, c = self.position
        if action == 'TURN_OFF':
            env[r][c] = False           # خاموش کردن چراغ
        elif action == 'MOVE':
            # رفتن به خانه بعدی در ترتیب پیمایش
            idx = self.visited_order.index(self.position)
            if idx < len(self.visited_order) - 1:
                self.position = self.visited_order[idx + 1]


# ---------------- اجرای برنامه ----------------
def run_agent():
    env = create_environment([[True, True],
                              [True, True]])   # همه خانه‌ها روشن
    agent = SimpleReflexAgent()
    step = 0

    print("محیط اولیه (هدف: خاموش کردن همه چراغ‌ها):")
    show_environment(env, agent.position, step)

    # حداکثر ۲۰ گام برای اطمینان (پیمایش ۴ خانه کافی است)
    max_steps = 20
    while not all_lights_off(env) and step < max_steps:
        step += 1
        percept = agent.perceive(env)       # ۱) احساس
        action = agent.decide(percept)      # ۲) تصمیم‌گیری قاعده‌ای
        print(f"\nگام {step}: احساس={percept} -> اقدام={action}")
        agent.act(action, env)              # ۳) اجرا
        show_environment(env, agent.position, step)

    print("\n✅ نتیجه نهایی: همه‌ی خانه‌ها خاموش شدند!"
          if all_lights_off(env) else "\n❌ هدف محقق نشد.")


if __name__ == "__main__":
    run_agent()
