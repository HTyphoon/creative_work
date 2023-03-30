#最急降下法を用いる
import numpy as np
import scipy.interpolate as scipl
from cal_SPDdif import *
import matplotlib.pyplot as plt

subs = ['WU']
ref = [17, 37, 38, 44, 55, 64]
sess = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
spdref,spdtes = Spd_inf(subs)
#等色関数の読み取り
#y[:,0]:x(lambda),y[:,1]:y(lambda),y[:,2]:z(lambda)
sSPD_tes,xyzbar = output_sSPD1()
#print('xyzbar',xyzbar)
#s_delta_diff：標準観測者の分光放射輝度差、avg_delta_diffは被験者の分光放射輝度差   
s_delta_diff,avg_delta_diff = output_SpdDiff(subs)
refsstr = ['No.17', 'No.37', 'No.38', 'No.44', 'No.55', 'No.64']


#sigma(xyzbar(lambda)*delta_P(lambda))
#[6*3]行列
def Cal_func(spd,cmf_fun):
    
    return np.dot(spd.T,cmf_fun)

#CMFを微分
def dCMF_func(cmf,d_lamda):
    d_cmf = np.zeros(np.shape(cmf))
    for i in range(len(cmf)):
        if i < len(cmf) - 1:
            d_cmf[i,:] = (cmf[i+1,:] - cmf[i,:]) / d_lamda
            # print(i,len(spd)-1)
            # print('before else',d_spd[i,:])
            continue
        else:
            d_cmf[i,:] = (0 - cmf[i,:]) / d_lamda
            #print('else',d_cmf[40,:])
    return d_cmf

#分光放射輝度差を代入して導関数を求める式
def dCal_func(cmf,spd,d_lambda):
    d_cmf = dCMF_func(cmf,d_lambda)#cmfの微分

    df = Cal_func(spd,d_cmf)#cmfの微分を関数に代入
    f = Cal_func(spd,cmf)
    f_abs = np.abs(f)
    df_abs = np.abs(df)
    return df,df_abs,d_cmf,f,f_abs

#cmf入力し、それを更新する関数
def update_cmf(cmf_xyz,alpha):
    d_cmf = dCMF_func(cmf_xyz,1)
    
    ###------------------------よくわからないところどうして +=がいい答えが出て、-=の場合は出ないのか-------------------###
    cmf_xyz -= alpha * d_cmf
    return cmf_xyz

#等色関数のグラフ化
    ###------------------------どうやって二つの曲線を同じグラフに入れるのか------------------------------------------###
    
def cmf_graph():
    col = np.array([[1,0,0],[0,1,0],[0,0,1]])
    fig_cmf = plt.figure(figsize=(20,7))
    ax_cmf = fig_cmf.add_subplot(111)
    ax_cmf.set_xlabel('wavelength (nm)',fontsize=14)
    ax_cmf.set_ylabel('XYZ Stimulus Value',fontsize=14)

    plt.title('CIE31 Standard Observer CMF')

    for i in range(3):
        ax_cmf.plot(wl,cmf_xyz[:,i],color=col[i,:],linewidth = 1.0)
        ax_cmf.plot(wl,xyzbar[:,i],color=col[i,:],linewidth = 3.0,linestyle = 'dotted')
        #ax_cmf.plot(wl,xyzbar[:,i],color='r',linewidth=1.0)
        #ax_cmf.plot(wl,diff_of_cmf,color='g',linewidth=1.0)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
    
    return plt.show()

def plot_DF_vector(df_abs_ini,difference):
    fig_vector = plt.figure(figsize=(20,10))
    delta = np.array([6,3])
    for i in range(6):
        ax_vector = fig_vector.add_subplot(2,3,i+1)
        plt.subplots_adjust(wspace=0.6)
        ax_vector.set_ylabel('CMF multiple SPDdif',fontsize=20)
        plt.xticks([0,1,2],['x','y','z'],fontsize=20)
        plt.yticks(fontsize=20)
        delta = df_abs_ini + difference
        #print(delta)
        # plt.quiver(0,df_abs_ini[i,0],0,delta[i,0] ,scale=0.5,color='r')
        # plt.quiver(1,df_abs_ini[i,1],1,delta[i,1] ,scale=0.5,color='r')
        # plt.quiver(2,df_abs_ini[i,2],2,delta[i,2] ,scale=0.5,color='r')
        plt.plot([0,1,2],df_abs_ini[i,:],color = 'gray',marker='o')
        print
        plt.scatter([0,1,2],delta[i,:],color='blue',marker = 'x',s=128)
        plt.plot([0,1,2],[0,0,0],color='black')
        plt.title(refsstr[i],fontsize=20)
    plt.show()
    return 

#inital_mul = Cal_func(s_delta_diff,xyzbar)
if __name__ == '__main__':
    R = Cal_func(s_delta_diff,xyzbar)
    d_lambda = 1
    d_cmf = dCMF_func(xyzbar,d_lambda)
    df,df_abs,d_cmf,f,f_abs = dCal_func(xyzbar,avg_delta_diff,d_lambda)
    #print('df',df)
    # print('d_cmf',d_cmf)
    # print('R',R)#超えたい目標答え

    ##最急降下による最小値探索
    #[41*6] initial cmf_xyz = xyzbar標準観測者の等色関数を初期値に設定
    cmf_xyz = xyzbar
    #print(cmf_xyz)
    #学習率
    alpha = 0.0001
    
    #収束判定条件
    #print('df_abs',df_abs)
    eps = df_abs.min() / 1000
    #eps 3.329440382331563e-10
    #print('eps',eps)
    
    #繰り返し最大数
    k_max = 10000
    f_abs_ini = f_abs
    for k in range(1,k_max):
        
        #cmfの更新
        cmf_xyz = update_cmf(cmf_xyz,alpha)

        f_abs = dCal_func(cmf_xyz,avg_delta_diff,d_lambda)[4]
        difference = f_abs - f_abs_ini 
        if (df_abs < eps).all():
            
            print(df_abs<eps)
            print('今は' + str(k+1) + '回目である')
            print('DF_ABS_INI',f_abs_ini)
            print('df_abs',df_abs)
            print('difference',difference)
            break
        elif k == k_max-1:          
            print('今は' + str(k+1) + '回目である')
            print('DF_ABS_INI',f_abs_ini)
            print('df_abs',df_abs)
            print('difference',difference)
            print('*****************')
            print(df_abs<eps)
            print(eps)
    #print('xyzbar',xyzbar)
    #print('cmf_xyz',cmf_xyz)   
    cmf_graph()
    plot_DF_vector(f_abs_ini,difference)