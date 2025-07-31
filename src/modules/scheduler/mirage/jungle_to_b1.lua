-- 初始化
setExecPath("Horizon/src/modules/scheduler/mirage/jungle_to_b1")
wasdCancel()

-- 切枪 & 锁定鼠标
lockMouse()
src("slot3")
src("+back")
src("+left")
setAngle(-1.154999, 82.157326)

-- 设置初始视角，向右前方走
sleep(6)          -- ceil(0.1 * 64) = 6

src("-back")
src("-left")
src("+forward")
src("+right")

-- 停止向右走
sleep(38)         -- ceil(0.6 * 64) = 39
src("-right")

-- 松W起跳
sleep(88)         -- ceil(1.368 * 64) = 88
src("-forward")
src("+jump;-jump")

-- 向右旋转跳上窗沿
sleep(27)         -- ceil(0.42 * 64) = 27
src("turnright 1 0 0")
src("+right")

-- 停止旋转视角，按下W 并校正位置
sleep(6)          -- 原 SLEEPTICK 6
src("-turnright")
src("-right")
src("+forward")
setAngle(0.000000, 55.354614)

-- 再次起跳，大跳
sleep(15)         -- 原 SLEEPTICK 20
src("slot2;slot1")
src("+duck")
src("+jump;-jump")
src("-forward")

-- 小幅旋转调整
sleep(6)          -- ceil(0.1 * 64) = 7
src("-duck")
src("turnright 0.4 0 0")
src("+right")

-- 停止偏转，解锁鼠标并定点
sleep(17)         -- ceil(0.2625 * 64) = 17
src("+duck")
src("-turnright")
src("-right")
unlockMouse()
setAngle(10.056204, 75.278900)

-- 取消下蹲
sleep(19)         -- ceil(0.3 * 64) = 20
src("-duck")
