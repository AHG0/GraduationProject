package com.hst.user_serve.jwt;

import com.alibaba.fastjson.JSONObject;
import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.hst.user_serve.entity.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * @description: Jwt工具类，生成JWT和认证
 */
@Component
public class JwtUtil {
    private static final Logger logger = LoggerFactory.getLogger(JwtUtil.class);
    //密钥
    private static final String SECRET = "my_secret";
    //过期时间
    private static final long EXPIRATION = 1800L;//单位为秒

    //生成用户token,设置token超时时间
    public String createToken(User user) {
        //过期时间
        Date expireDate = new Date(System.currentTimeMillis() + EXPIRATION * 1000);
        Map<String, Object> map = new HashMap<>();
        map.put("alg", "HS256");
        map.put("typ", "JWT");
        return JWT.create()
                .withHeader(map)// 添加头部
                //可以将基本信息放到claims中
                .withClaim("userid", user.getUserid())//userid
                .withClaim("username", user.getUsername())//username
                .withClaim("password", user.getPassword())//password
                .withClaim("usertype", user.getUsertype())//usertype
                .withClaim("queries_num", user.getQueries_num())//queries_num
                .withExpiresAt(expireDate) //超时设置,设置过期的日期
                .withIssuedAt(new Date()) //签发时间
                .sign(Algorithm.HMAC256(SECRET)); //SECRET加密
    }

    //校验token并解析token
    public JSONObject verifyToken(String token) {
        DecodedJWT jwt;
        JSONObject json = new JSONObject();
        JWTVerifier verifier = JWT.require(Algorithm.HMAC256(SECRET)).build();
        jwt = verifier.verify(token);
        logger.info("token解码成功。");
        logger.info(String.format("用户名为：%s，用户ID为：%d", jwt.getClaim("username").asString(), jwt.getClaim("userid").asInt()));
        //decodedJWT.getClaim("属性").asString()  获取负载中的属性值
        json.put("verify", true);
        json.put("userid", jwt.getClaim("userid").asInt());
        json.put("usertype", jwt.getClaim("usertype").asInt());
        json.put("queries_num", jwt.getClaim("queries_num").asInt());
        return json;
    }
}
