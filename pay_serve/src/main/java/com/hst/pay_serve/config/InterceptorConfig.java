package com.hst.pay_serve.config;

import com.hst.pay_serve.interceptor.CorsInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class InterceptorConfig implements WebMvcConfigurer {


    @Bean
    public CorsInterceptor corsInterceptor() {
        return new CorsInterceptor();
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 跨域拦截器注册(注意：跨域拦截器注册要放在最上方)
        registry.addInterceptor(corsInterceptor()).addPathPatterns("/**");

        WebMvcConfigurer.super.addInterceptors(registry);
    }
}
