package com.hst.login_serve.jwt;

import com.alibaba.fastjson.JSONObject;
import com.auth0.jwt.exceptions.AlgorithmMismatchException;
import com.auth0.jwt.exceptions.SignatureVerificationException;
import com.auth0.jwt.exceptions.TokenExpiredException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.PrintWriter;
import java.util.HashMap;

@Component
public class JWTInterceptors implements HandlerInterceptor {
    private static final Logger logger = LoggerFactory.getLogger(JWTInterceptors.class);
    JwtUtil jwtUtil = new JwtUtil();
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String token = request.getHeader("token");
        HashMap<String, Object> map = new HashMap<>();
        try {
            jwtUtil.verifyToken(token);
            return true;
        } catch (SignatureVerificationException e) {
            logger.error(e.getMessage());
            map.put("msg", "无效的签名");
        } catch (TokenExpiredException e) {
            logger.error(e.getMessage());
            map.put("msg", "该令牌已过期");
        } catch (AlgorithmMismatchException e) {
            logger.error(e.getMessage());
            map.put("msg", "算法不匹配");
        } catch (Exception e) {
            logger.error(e.getMessage());
            map.put("msg", "token无效！");
        }
        map.put("status", false);
        String errorMsg = JSONObject.toJSONString(map);
        response.setContentType("application/json; charset=UTF-8");
        PrintWriter writer = response.getWriter();
        writer.print(errorMsg);
        writer.close();
        return false;
    }
}
