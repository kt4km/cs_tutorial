import numpy as np
import matplotlib.pyplot as plt

# ===================================================== # 
#       マス・ばね・ダンパ系のシミュレーションコード
# ===================================================== #

#----パラメータ設定----#
m = 1    # 質量[kg]
k = 1    # ばね定数[N/m]
c = 0.2  # 減衰係数[N s/m]



#----シミュレーション----#
x1 = -5    # 変位[m]
x2 = 0    # 速度[m/s]
x = np.array([[x1], [x2]])    # 状態

t = 0    # 時間[s]
Ns = 1000    # 反復回数
dt = 0.1    # 刻み幅[s]

Kp = 0.5    # 比例ゲイン
Ki = 0.5    # 積分ゲイン
Kd = 2    # 微分ゲイン

r = 2    # 目標値[m]

A = np.array([[0, 1], [-k/m, -c/m]])    # 係数
B = np.array([[0], [1/m]])    # 係数

e_sum = 0
e_before = 0

#----数値を保存用の箱----#
x_list = [[] for i in range(np.ndim(x))]    # ndimで次元を取得し，保存したい数値に合った次元の箱を生成
t_list = [[] for i in range(np.ndim(t))]

x_list = np.hstack([x_list, x])    # 初期値を箱に保存(hstackは行列の結合)
t_list = np.hstack([t_list, t])

# ====================================== #
# 制御ありと制御なしをflagでわけているので
# 各自コメントアウトで使い分けしてください
# ====================================== #
flag = 'control'    # 制御あり
# flag = 'noncontrol'    # 制御なし

for i in range(Ns):

    # 偏差
    e = r - x[0]


    # 偏差の足し合わせ
    e_sum = e_sum + dt*e


    # 制御入力(制御あり，なしで場合分けしてます)
    if flag == 'noncontrol':
        u = 0

    elif flag == 'control':
        u = Kp*e + Ki*e_sum + Kd*(e - e_before)/ dt    # PID


    # 1つ前の偏差の保存
    e_before = e


    # 状態方程式
    x_dot = A.dot(x) + B*u


    # オイラー法
    x = x + dt*x_dot    # 状態の更新


    t = t + dt    # 時間の更新


    x_list = np.hstack([x_list, x])    # 計算した数値を箱に保存する
    t_list = np.hstack([t_list, t])





#----計算結果をグラフで表示する----#
# def は関数を定義している
def draw_pos(t_list, x_list):
    # 横軸に時間，縦軸に台車の変位をプロットする
    fig = plt.figure()    # figureウィンドウを生成

    ax = fig.add_subplot(111)    # グラフを1行1列1番目に挿入
    ax.plot(t_list, x_list, color='red', linewidth=2)   
    ax.set_xlim(0,50)  # 横軸の範囲を指定
    ax.set_xticks(np.arange(0,51,5))   # x軸の目盛り0から50を5で分割する
    ax.set_xlabel('time[s]', fontsize=12)
    ax.set_ylabel('mass position[m]', fontsize=12)    # 縦軸にラベルを貼る
    ax.grid()  # グリッド線を引く

def draw_vel(t_list, x_list):
    # 横軸に時間，縦軸に台車の速度をプロットする
    fig = plt.figure()

    ax = fig.add_subplot(1,1,1)
    ax.plot(t_list, x_list, color='green', linewidth=2)
    ax.set_xlim(0,50)
    ax.set_xticks(np.arange(0,51,5))
    ax.set_xlabel('time[s]', fontsize=12)
    ax.set_ylabel('mass velocity[m/s]', fontsize=12)
    ax.grid ()


draw_pos(t_list, x_list[0])    # 制御対象の位置を描画
draw_vel(t_list, x_list[1])    # 制御対象の速度を描画

plt.show()  # グラフを表示する