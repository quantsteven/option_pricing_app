import streamlit as st


def model_description():
    st.divider()
    st.markdown("在 **Black-Scholes** 模型下，加密货币价格的随机微分方程（stochastic differential equation，SDE）为：")

    st.latex(r"""
    \frac{dS(t)}{S(t)} = (r-q)dt+\sigma dW(t)
    """)

    st.markdown("其中：")
    st.markdown(r"""
    - $S(t)$：现货价格  
    - $r$：稳定币（USDⓈ）的利率  
    - $q$：非稳定币（BTC, ETH 等）的利率  
    - $\sigma$：现货波动率  
    - $W(t)$：布朗运动  
    """)


def european_option_pricing_formula():
    st.divider()
    st.markdown("欧式期权的解析解公式为：")

    st.latex(r"""
    V = \omega\left[e^{-qT}S_0\Phi(\omega d_+) - e^{-rT}K\Phi(\omega d_-)\right]
    """)

    st.latex(r"""
    d_\pm = \frac{1}{\sigma\sqrt{T}}\ln\left(\frac{S_0e^{(r-q)T}}{K}\right)\pm\frac{\sigma\sqrt{T}}{2}
    """)

    st.markdown(r"其中 $\omega = 1$ 表示看涨期权，$\omega = -1$ 表示看跌期权，$\Phi(\cdot)$ 是高斯分布的累计概率函数。")


def european_option_greeks():
    pass


def single_touch_option_pricing_formula():
    st.divider()

    st.markdown("用 $g_{\eta}(0)$ 分别代表先触碰下障碍 $L$ 的概率（当 $\eta = 1$）和先触碰上障碍 $L$ 的概率（当 $\eta = -1$）")
    st.markdown("在 PaE 返还支付下，四种单触碰期权的现值表达式为:")

    st.latex(r"""
        \begin{equation}
        \begin{aligned}
            &V_{\text{OTU}}=R e^{-rT} \cdot g_{-1}(0) \\
            &V_{\text{OTD}}=R e^{-rT} \cdot g_{1}(0) \\ 
            &V_{\text{NTU}}=R e^{-rT} -V_{\text{OTU}} = R e^{-rT} \cdot [1-g_{-1}(0)] \\
            &V_{\text{NTD}}=R e^{-rT} - V_{\text{NTU}} = R e^{-rT} \cdot [1-g_{1}(0)] \\ 
        \end{aligned}
        \end{equation}
    """)

    st.markdown("其中")

    st.latex(r"""
        \begin{equation}
            g_\eta(\phi)=e_{\phi}\left(2 x_{L}\right) \cdot \Phi\left(\eta \frac{x_{L}+m_{\phi}}{v}\right)+\Phi\left(\eta \frac{x_{L}-m_{\phi}}{v}\right)
        \end{equation}
    """)

    st.latex(r"""
        \begin{equation}
        \begin{array}{ll}
            \phi= \begin{cases}0, & \mathrm{PaE} \\
                                1, & \mathrm{PaH}\end{cases} &
            \eta= \begin{cases}-1, & \mathrm{Upper\;Barrier} \\
                                1, & \mathrm{Lower\;Barrier}\end{cases} \\
            e_{\phi}(u) = \text{exp}\left(\frac{\mu_{\phi}}{\sigma^2}u\right)\\
            \hat{\mu}=(r-q)-0.5 \sigma^2, & v=\sigma \sqrt{T} \\
            \mu_{\phi}=\sqrt{\hat{\mu}^2+\phi \cdot 2 r \sigma^2}, & m_{\phi}=\mu_{\phi} T \\
            x_L=\ln \left(\frac{L}{S}\right) &  \\
        \end{array}
        \end{equation}
    """)

    st.markdown("在 PaH 返还支付下，两种单触碰期权 (OTU, OTD) 的现值表达式为 (注意 NTU 和 NTD 只能 PaE，因此只有在到期日才能知道障碍是否被触碰过):")

    st.latex(r"""
        \begin{equation}
        \begin{aligned}
            &V_{\text{OTU}}=R \cdot e_0(x_B) \cdot e_1(-x_B) \cdot g_{-1}(1) \\
            &V_{\text{OTD}}=R \cdot e_0(x_B) \cdot e_1(-x_B) \cdot g_{1}(1) \\ 
        \end{aligned}
        \end{equation}
    """)


def double_touch_option_pricing_formula():
    st.divider()
    st.markdown("用 $G_l(0)$ 和 $G_h(0)$ 分别代表先触碰下障碍 $L_l$ 的概率和先触碰上障碍 $L_h$ 的概率")
    st.markdown("在 PaE 返还支付下，四种双触碰期权的现值表达式为:")
    st.latex(r"""
        \begin{equation}
            \begin{aligned}
                &V_{\text{OTUNTD}}=R e^{-rT} \cdot G_h(0) \\
                &V_{\text{OTDNTU}}=R e^{-rT} \cdot G_l(0) \\ 
                &V_{\text{DOT}}=V_{\text{OTUNTD}}+V_{\text{OTDNTU}}=R e^{-rT} \cdot\left[G_h(0)+G_l(0)\right] \\
                &V_{\text{DNT}}=R e^{-rT} - V_{\text{DOT}} = R e^{-rT} \cdot\left[1-G_h(0)-G_l(0)\right] \\ 
            \end{aligned}
        \end{equation}
    """)

    st.latex(r"""
        \begin{equation}
            G_Y(\varphi)=\left\{\begin{array}{l}
            \sum_{k=0}^6\left[\exp \left(\frac{\mu_{\varphi}}{\sigma^2} u_Y\right) \Phi\left(\frac{-u_Y-m_{\varphi}}{v}\right)-\exp \left(-\frac{\mu_{\varphi}}{\sigma^2} u_Y\right) \Phi\left(\frac{-u_Y+m_{\varphi}}{v}\right)\right] \\
            -\sum_{k=-6}^{-1}\left[\exp \left(\frac{\mu_{\varphi}}{\sigma^2} u_Y\right) \Phi\left(\frac{u_Y+m_{\varphi}}{v}\right)+\exp \left(-\frac{\mu_{\varphi}}{\sigma^2} u_Y\right) \Phi\left(\frac{u_Y-m_{\varphi}}{v}\right)\right]
            \end{array}\right\} \cdot \exp \left(\frac{\mu_{\varphi}}{\sigma^2} x_Y\right)
        \end{equation}
    """)

    st.latex(r"""
        \begin{equation}
            \begin{array}{ll}
                \varphi= \begin{cases}0, & \mathrm{PaE} \\
                1, & \mathrm{PaH}\end{cases} \\
                Y=l \text { or } h & \\
                \hat{\mu}=(r-q)-0.5 \sigma^2, & v=\sigma \sqrt{T} \\
                \mu_{\varphi}=\sqrt{\hat{\mu}^2+\varphi \cdot 2 r \sigma^2}, & m_{\varphi}=\mu_{\varphi} T \\
                x_l=\ln \left(\frac{L_l}{S}\right), & x_h=\ln \left(\frac{L_h}{S}\right) \\
                u_l=-x_l+2 k\left(x_h-x_l\right), & u_l=x_h+2 k\left(x_h-x_l\right)
            \end{array}
        \end{equation}
    """)

    st.markdown("上面公式也可以处理在 PaH 返还支付下四种触碰期权的现值表达式，只需设置 $\phi$ 为 1，然后再加一些项。")
    st.markdown("在 PaE 返还支付下，三种双触碰期权（OTUNTD, OTDNTU, DOT）的现值表达式为（注意 DNT 只能 PaE，因此只有在到期日才能知道障碍是否被触碰过）:")

    st.latex(r"""
        \begin{equation}
            \begin{aligned}
                &V_{\text{OTUNTD}}=R \cdot \exp \left(\frac{\mu_0-\mu_1}{\sigma^2} u_h\right) \cdot G_h(1) \\
                &V_{\text{OTDNTU}}=R \cdot \exp \left(\frac{\mu_0-\mu_1}{\sigma^2} u_l\right) \cdot G_l(1) \\
                &V_{\text{DOT}}=R \cdot\left[\exp \left(\frac{\mu_0-\mu_1}{\sigma^2} u_h\right) \cdot G_h(1)+\exp 
                \left(\frac{\mu_0-\mu_1}{\sigma^2} u_l\right) \cdot G_l(1)\right] \\
            \end{aligned}
        \end{equation}
    """)


def single_barrier_option_pricing_formula():
    st.divider()
    st.markdown("八种单障碍期权的现值表达式为:")

    st.latex(r"""
        \begin{equation}
            V_{\mathrm{DOC}} = \left\{\begin{array}{ll}
                                  0,       & S \leq L           \\
                                  I_1-I_3, & S \geq L, K \geq L \\
                                  I_2-I_4, & S \geq L, K \leq L
                                  \end{array}\right.
        \end{equation}
    """)

    st.latex(r"""
        \begin{equation}
            V_{\mathrm{UOC}} = \left\{\begin{array}{ll}
                                  0,               & S \geq L           \\
                                  0,               & S \leq L, K \geq L \\
                                  I_1-I_2+I_3-I_4, & S \leq L, K \leq L
                                  \end{array}\right.
        \end{equation}
    """)

    st.latex(r"""        
        \begin{equation}
            V_{\mathrm{DOP}} = \left\{\begin{array}{ll}
                                  0,               & S \leq L           \\
                                  I_1-I_2+I_3-I_4, & S \geq L, K \geq L \\
                                  0,               & S \geq L, K \leq L
                                  \end{array}\right.
        \end{equation}
    """)

    st.latex(r"""        
        \begin{equation}
            V_{\mathrm{UOP}} = \left\{\begin{array}{ll}
                                  0,       & S \geq L           \\
                                  I_2-I_4, & S \leq L, K \geq L \\
                                  I_1-I_3, & S \leq L, K \leq L
                                  \end{array}\right.
        \end{equation}
    """)

    st.latex(r"""        
        \begin{equation}
            V_{\mathrm{DIC}} = I_1-V_{\mathrm{DOC}} 
                         = I_1-\left\{\begin{array}{ll}
                                       0,       & S \leq L           \\
                                       I_1-I_3, & S \geq L, K \geq L \\
                                       I_2-I_4, & S \geq L, K \leq L
                                      \end{array}
                         = \begin{cases}
                            I_1,         & S \leq L           \\
                            I_3,         & S \geq L, K \geq L \\
                            I_1-I_2+I_4, & S \geq L, K \leq L
                           \end{cases}\right.
        \end{equation}
    """)

    st.latex(r"""    
        \begin{equation}
            V_{\mathrm{UIC}} = I_1-V_{\mathrm{UOC}} 
                             = I_1-\left\{\begin{array}{ll}
                                      0,               & S \geq L           \\
                                      0,               & S \leq L, K \geq L \\
                                      I_1-I_2+I_3-I_4, & S \leq L, K \leq L
                                      \end{array}
                             = \begin{cases}
                                I_1,         & S \geq L           \\
                                I_1,         & S \leq L, K \geq L \\
                                I_2-I_3+I_4, & S \leq L, K \leq L
                               \end{cases}\right.
        \end{equation}
    """)

    st.latex(r"""    
        \begin{equation}
            V_{\mathrm{DIP}} = I_1-V_{\mathrm{DOP}} 
                             = I_1-\left\{\begin{array}{ll}
                                      0,               & S \leq L           \\
                                      I_1-I_2+I_3-I_4, & S \geq L, K \geq L \\
                                      0,               & S \geq L, K \leq L
                                      \end{array}
                             = \begin{cases}
                                I_1,         & S \leq L           \\
                                I_1-I_2+I_4, & S \geq L, K \geq L \\
                                I_1,         & S \geq L, K \leq L
                               \end{cases}\right.
        \end{equation}
    """)

    st.latex(r"""        
        \begin{equation}
            V_{\mathrm{UIP}} = I_1-V_{\mathrm{UOP}} 
                             = I_1-\left\{\begin{array}{ll}
                                      0,       & S \geq L           \\
                                      I_2-I_4, & S \leq L, K \geq L \\
                                      I_1-I_3, & S \leq L, K \leq L
                                      \end{array}
                             = \begin{cases}
                                I_1,         & S \geq L           \\
                                I_1-I_2+I_4, & S \leq L, K \geq L \\
                                I_3,         & S \leq L, K \leq L
                               \end{cases}\right.
        \end{equation}  
    """)

    st.markdown("其中")

    st.latex(r"""
        \begin{equation}
            \begin{aligned}
                &I_1=\omega \cdot\left[e^{-qT} S \cdot \Phi\left(\omega \frac{-x_{K}+m_{+}}{v}\right)-e^{-rT} K \cdot \Phi\left(\omega \frac{-x_{K}+m_{-}}{v}\right)\right] \\
                &I_2=\omega \cdot\left[e^{-qT} S \cdot \Phi\left(\omega \frac{-x_{L}+m_{+}}{v}\right)-e^{-rT} K \cdot \Phi\left(\omega \frac{-x_{L}+m_{-}}{v}\right)\right] \\
                &I_3=\omega \cdot\left[e^{-qT} S \cdot e^{2 x_{L} \lambda_{+}} \cdot \Phi\left(\eta \frac{x_{L_2}+m_{+}}{v}\right)-e^{-r_{T}} K \cdot e^{2 x_{L} \lambda_{-}} \cdot \Phi\left(\eta \frac{x_{L_2}+m_{-}}{v}\right)\right] \\
                &I_4=\omega \cdot\left[e^{-qT} S \cdot e^{2 x_{L} \lambda_{+}} \cdot \Phi\left(\eta \frac{x_{L}+m_{+}}{v}\right)-e^{-r_{T}} K \cdot e^{2 x_{L} \lambda_{-}} \cdot \Phi\left(\eta \frac{x_{L}+m_{-}}{v}\right)\right] \\
                &I_5=Re^{-rT} \cdot\left[1-g_\eta\left(u_0\right)\right]=Re^{-rT} \cdot \left[\Phi\left(\eta \frac{-x_{L}+u_0T}{v}\right)-e_0\left(2 x_{L}\right) \cdot \Phi\left(\eta \frac{x_{L}+u_0T}{v}\right)\right] \\
                &I_6(\phi)=R \cdot g_\eta\left(u_{\phi}\right) \cdot \begin{cases}e^{-r T_d} & \text { if } \phi=0 \\
                e_0\left(x_L\right) \cdot e_1\left(-x_L\right) & \text { if } \phi=1\end{cases} \\
            \end{aligned}
        \end{equation}
    """)

    st.latex(r"""
        \begin{equation}
            \begin{array}{lll}
                \phi= \begin{cases}0, & \mathrm{PaE} \\
                                   1, & \mathrm{PaH}\end{cases} &
                \eta= \begin{cases}-1, & \mathrm{upper\;barrier} \\
                                    1, & \mathrm{lower\;barrier} \end{cases} \\
                e_{\phi}(u) = \text{exp}\left(\frac{\mu_{\phi}}{\sigma^2}u\right)\\
                \hat{\mu}=(r-q)-0.5 \sigma^2, & v=\sigma \sqrt{T} \\
                \mu_{\phi}=\sqrt{\hat{\mu}^2+\phi \cdot 2 r \sigma^2}, & m_{\phi}=\mu_{\phi} T \\
                x_K=\ln \left(\frac{K}{S}\right) & x_L=\ln \left(\frac{L}{S}\right) & x_{L_2}=\ln \left(\frac{L^2}{SK}\right) \\
            \end{array}
        \end{equation}
    """)


def double_barrier_option_pricing_formula():
    st.divider()
    st.markdown("四种不带返还的触碰期权的表达式如下：")
    st.latex(r"""
        \begin{equation}
            \begin{aligned}
                &V_{\text{DKOC}}=R e^{-rT} \cdot [S\cdot F(1,x_K,x_H) - K\cdot F(0,x_K,x_H)] \\
                &V_{\text{DKOP}}=R e^{-rT} \cdot [K\cdot F(0,x_L,x_K) - S\cdot F(1,x_L,x_K)] \\ 
                &V_{\text{DKIC}}=V_{\text{call}} - V_{\text{DKOC}} \\
                &V_{\text{DKIP}}=V_{\text{put}} - V_{\text{DKOP}} \\
            \end{aligned}
        \end{equation}
    """)

    st.markdown("其中")

    st.latex(r"""
        \begin{equation}
            F\left(\nu, z_1, z_2\right)=\sum_{k=-6}^6\left\{e_0(-u) \cdot\left[f\left(a_1, a_2, u-m_0, v, \nu\right)+e_0\left(2 x_H\right) \cdot f\left(a_1, a_2, u-m_0-2 x_H, v, \nu\right)\right]\right\}
        \end{equation} 
    """)

    st.latex(r"""
        \begin{equation}
            f\left(a_1, a_2, \beta, v, \nu\right)=\exp \left(\frac{\nu}{2}\left(\nu v^2-2 \beta\right)\right) \cdot\left[\Phi\left(v \nu-\frac{\beta+a_1}{v}\right)-\Phi\left(v \nu-\frac{\beta+a_2}{v}\right)\right]
        \end{equation}
    """)

    st.latex(r"""
        \begin{equation}
            \begin{array}{lll}
                a_1 = \max(z_1, x_L), & a_1 = \max(z_2, x_H) \\
                \hat{\mu}=(r-q)-0.5 \sigma^2, & v=\sigma \sqrt{T} \\
                \mu_{\phi}=\sqrt{\hat{\mu}^2+\phi \cdot 2 r \sigma^2}, & m_{\phi}=\mu_{\varphi} T \\
                x_K=\ln \left(\frac{K}{S}\right), & x_l=\ln \left(\frac{L_l}{S}\right), & x_h=\ln \left(\frac{L_h}{S}\right) \\
                u_l=-x_l+2 k\left(x_h-x_l\right), & u_l=x_h+2 k\left(x_h-x_l\right)
            \end{array}
        \end{equation}
    """)

    st.markdown("四种带返还的触碰期权的表达式如下：")

    st.latex(r"""
        \begin{equation}
            \begin{aligned}
                &V_{\text{DKOC}}(R_L,R_H,\phi_L,\phi_H) = V_{\text{DKOC}} + V_{\text{OTUNTD}}(R_H,\phi_H) + V_{\text{OTDNTU}}(R_L,\phi_L) \\
                &V_{\text{DKOP}}(R_L,R_H,\phi_L,\phi_H) = V_{\text{DKOP}} + V_{\text{OTUNTD}}(R_H,\phi_H) + V_{\text{OTDNTU}}(R_L,\phi_L) \\
                &V_{\text{DKIC}}(R)=V_{\text{DKIC}} + V_{\text{DNT}}(R) \\
                &V_{\text{DKIP}}(R)=V_{\text{DKIP}} + V_{\text{DNT}}(R) \\
            \end{aligned}
        \end{equation}
    """)

    st.markdown("其中")

    st.latex(r"""
        \begin{equation}
            \begin{aligned}
                &V_{\text{OTUNTD}}(R,\phi) = R \cdot G_H(\phi) 
                    \cdot \begin{cases}e^{-rT}                                        & \text{if } \phi=0, PaH \\
                                   e_0\left(x_H\right) \cdot e_1\left(-x_H\right) & \text{if } \phi=1, PaE \end{cases}\\
                &V_{\text{OTDNTU}}(R,\phi) = R \cdot G_L(\phi) 
                    \cdot \begin{cases}e^{-rT}                                        & \text{if } \phi=0, PaH \\
                                   e_0\left(x_L\right) \cdot e_1\left(-x_L\right) & \text{if } \phi=1, PaE \end{cases}\\
                &V_{\text{DNT}}(R) = R \cdot e^{-rT} \cdot [1-G_H(0)-G_L(0)]
                    \end{aligned}
        \end{equation}
    """)
