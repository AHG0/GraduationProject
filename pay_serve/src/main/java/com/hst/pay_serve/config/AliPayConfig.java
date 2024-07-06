package com.hst.pay_serve.config;

import lombok.Data;
import org.springframework.context.annotation.Configuration;

@Configuration
@Data
public class AliPayConfig {
    //APPID
    private String appId="9021000134640303";
    //商户私钥, 即PKCS8格式RSA2私钥
    private String privateKey = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCZNJ1V6lAU+uoRBBNh1NDNGBLIqypjmQSCW6Jw9/5qnQqHZjwwhPwhWb+UyV7kl+LzU3R8FnrJ6Z4s+NQh0eF03Vc5q/MO4vzqVmgZTwLv9wpO2EzynAL2HoLlZj/EOALpYIx4PmjwX/8DnOQcbVaof7alCKqcv44bVg5gYa4vfw1DL0zs0AyLO2iXr7M3QcWQ2Wm8axXZp1IHArZ84UsctNy4rPTt9tADEZ6N3Szf2th5GCvetq4/syilC+4oyfXTo+SEf4lOx4qaiCQSOGsaI21xbSvY+EYXLoyoU3U/BmPeoaaCiLzVMpH4Rlga8wSY7dUNi/dNDpVNOyuhjDNBAgMBAAECggEBAIEGP47wk1rn6aJE9XHJwcNIB+G5zSwt3Q9PzuEm6but4AUhw4T1KkWICQFsCZ+ojrhvy0UJxYUwW0byk+ybji1WjzQBrOQXo/pSpL7TvNyNB8BZB4y2eQP/tCsvznoY1dLnvcUygjwWDHVldvK93mJvlEkuoEj8Rdidw+PFv+U84e6KtqzTlYymvMT1P1Lpf4SazJHivZLg7+5otrz5JJeAE/L1gQ+JptXiptpS4lmJVtpDCwMk7s4fvvBfhXDWyukIxic+PSE/i0qq93XqGrzVLyKDi9hOfh3j6OEpJdfVTdixt182gTHllEKvsXTFGPI2dmU9E3i8lxxMT/EGleUCgYEA3t3cm+RNa9R4F6VGbMn+7ip8cA419Lgf32LSfnFQO6MKhEHS4bQkaUVrhp26kCwgZ4xcHo/0sHWaha7Wzzpb6ouSChKprfKnBDxAzKhBSNAEXSiLbueXcHZdH5TYnx4KkTm/q0+LQXPQa9eG6Kt/bpdp9rSFP8yhXtiJAR6iBc8CgYEAr/uAprEpQrDCe+dBkMlrcVyyEEU0d/mdSlG8SOIwbvN3yB3T08deiR8vSRNyk9AtHao+1zOMyTgSWfbQH5VszotP6/fM+j082SkQB42BfGEBxelUjVdMS1TvlJ30ijuhPllt7ULyRiUm4WIFukRdMscp7f+olG/tkXkecNJDie8CgYAvsLosgcYvdN/d73gKf48V1/GY6PGS1HO9kaAJfqX0nQb7FjrSIYJJJJnFzKrHfynP/rEXuSZbPE88nBVLcumIXyV5ElVM68fhmCMlqDuQITNN3Ac6TESTxEBZKbjRE9SfDwR83CCoeOf4q74qu8ghGjWKnUaGSHufmCZ5Htz88QKBgBoaax3On3kl8OMiDUalqcs53auuKDc3jk4sy4ngCyEZ+gVz7yy1oN8kAgaL3O3x7g89Zm7TVamvKIGxq3NT3bzRSzyMGBpyJOltPtRv9+n0Fag+kO0aKtXttk/MEi7C44r1BuoviPJApoC94m2boFtc0WpdBqtl4s42Mf64IY5/AoGBAILSTNH9PJlAn7KG/5hXeFMwV6N39nkBcqvo11F+Utbja8j5O1DE9f9eny1oWgqtoIM0Ba3fmgkx7LBUwi7+J4q1IER8IkweQqDDlk/liNyzccm5ezoxL3qUVf0VPAIMxCZCY8N87VD6WTyUi9arQ3zSZ6wNbtVOQ/UTVSsSVhxF";
    //应用公钥
    private String publicKey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmTSdVepQFPrqEQQTYdTQzRgSyKsqY5kEgluicPf+ap0Kh2Y8MIT8IVm/lMle5Jfi81N0fBZ6yemeLPjUIdHhdN1XOavzDuL86lZoGU8C7/cKTthM8pwC9h6C5WY/xDgC6WCMeD5o8F//A5zkHG1WqH+2pQiqnL+OG1YOYGGuL38NQy9M7NAMiztol6+zN0HFkNlpvGsV2adSBwK2fOFLHLTcuKz07fbQAxGejd0s39rYeRgr3rauP7MopQvuKMn106PkhH+JTseKmogkEjhrGiNtcW0r2PhGFy6MqFN1PwZj3qGmgoi81TKR+EZYGvMEmO3VDYv3TQ6VTTsroYwzQQIDAQAB";
    //支付宝公钥
    private String aLiPublicKey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2zkYznWt4dV+Ox4KSdRtMUL8NOiqEByueCFEEFylcJZ0q2veB04Dx4ns9d4pa0F8ffVcrE8DW1GLDxUAuWpW/whNYS2gzYJ9/zHZgfENxDhUmzg6aHONfZOh5Hh/xIPKFFbXemgqsl+6OW7oEpLfOOXKy54P0oRtQ/V2QbzJiTpCao2rgNUQMQU/4b352TJ6DNW5/pUY528AqnXa09zckBidPxgzPvvzGmcgSd8gk3gQft0hAbqDYz0BWu4jhrDlbUZEGPWa14fO2PaLXLGGuMCzpvpCEgmIpikSbrxnagAZNlsSqDLZIWs603Nqv2P855r1uvZVfG9Zz9hcSrca2QIDAQAB";
    //服务器异步通知页面路径路，要http://格式的完整路径（需要内网穿透[*.natappfree.cc->localhost:8091]，D盘启动natapp）
    private String notifyUrl= "http://agsyvy.natappfree.cc/notify";
    //页面跳转同步通知页面路径，需http://格式的完整路径
    private String returnUrl= "http://localhost:8080/file_home2";
    //签名方式
    private String signType="RSA2";
    //字符编码格式
    private String charset="utf-8";
    //订单超时时间
    private String timeout_express = "10m";
    //产品编号
    private String product_code = "FAST_INSTANT_TRADE_PAY";
    //支付宝网关
    private String gatewayUrl="https://openapi-sandbox.dl.alipaydev.com/gateway.do";
    //日志打印地址
    private String logPath;


}
