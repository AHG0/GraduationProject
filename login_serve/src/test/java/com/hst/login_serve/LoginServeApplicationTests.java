package com.hst.login_serve;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@SpringBootTest
class LoginServeApplicationTests {

	private static final String SECRET = "my_secret";
	private static final long EXPIRATION = 1800L;//单位为秒
	@Test
	void contextLoads() {
		//过期时间
		Date expireDate = new Date(System.currentTimeMillis() + EXPIRATION * 1000);
		Map<String, Object> map = new HashMap<>();
		map.put("alg", "HS256");
		map.put("typ", "JWT");
		String token = JWT.create()
				.withHeader(map)// 添加头部
				//可以将基本信息放到claims中
				.withClaim("id", 1)//userId
				.withClaim("userName", "1")//userName
				.withClaim("password", "1")//password
				.withExpiresAt(expireDate) //超时设置,设置过期的日期
				.withIssuedAt(new Date()) //签发时间
				.sign(Algorithm.HMAC256(SECRET)); //SECRET加密
		System.out.println(token);
	}

}
